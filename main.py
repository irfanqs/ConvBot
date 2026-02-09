import os
import json
import asyncio
import webbrowser
import speech_recognition as sr
from groq import Groq
from AppOpener import open as open_app
import edge_tts
from datetime import datetime
import pygame
import subprocess
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# 1. SETUP AUDIO & ENV 
try:
    pygame.mixer.init()
except pygame.error:
    print("⚠️ Warning: Audio device error")

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback")

if not API_KEY or "gsk_" not in API_KEY:
    print("❌ ERROR: API Key tidak valid. Cek file .env kamu!")
    exit()

client = Groq(api_key=API_KEY)

# Setup Spotify (optional - jika credentials tersedia)
spotify_client = None
if SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET:
    try:
        sp_oauth = SpotifyOAuth(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            redirect_uri=SPOTIFY_REDIRECT_URI,
            scope="user-modify-playback-state user-read-playback-state user-read-currently-playing"
        )
        spotify_client = spotipy.Spotify(auth_manager=sp_oauth)
        print("✅ Spotify API Connected!")
    except Exception as e:
        print(f"⚠️ Spotify API not configured: {e}")
else:
    print("⚠️ Spotify credentials not found - using URI fallback")

# 2. CONFIGURATION 
SYSTEM_PROMPT = """
You are ConvBot. Current time: {time}
Your Goal: Identify intention (OPEN apps, SEARCH content, CONTROL system, CHAT).
Output ONLY JSON.

JSON Formats:
- Action: {{"type": "action", "target": "target_name", "content": "search_query", "category": "web/app/sys/playback", "reply": "Confirmation"}}
- Chat: {{"type": "chat", "reply": "Response"}}
- Close: {{"type": "close", "reply": "Closing text"}}

Rules:
- PLAYBACK: target="spotify"/"youtube", content="song/video name". category="playback".
- SYSTEM: target="wifi_off"/"wifi_on".
- WEB: Must use FULL URL (https://...).
- APP: App name only.
- REPLY: Short conversational Indonesian.
"""

HALLUCINATION_FILTER = [
    "terima kasih", "thank you", "subtitle", "copyright", 
    "amara.org", "subtitles", "caption"
]

# 3. FUNCTIONS
async def speak(text):
    """Mouth: EdgeTTS + Pygame"""
    print(f"🗣️  ConvBot: {text}")
    filename = "temp_voice.mp3"
    
    if os.path.exists(filename):
        try:
            pygame.mixer.music.unload()
            os.remove(filename)
        except:
            pass 

    try:
        communicate = edge_tts.Communicate(text, "id-ID-ArdiNeural")
        await communicate.save(filename)
        
        if not pygame.mixer.get_init(): pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
            
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Error Speak: {e}")

def listen_mic():
    """Ear: Whisper + Feedback Beep + Anti-Hallucination"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🔔 [TING] Silakan ngomong...")
        # Beep hanya untuk Windows
        if os.name == 'nt':
            try:
                import winsound
                winsound.Beep(1000, 200)
            except:
                pass
        
        r.dynamic_energy_threshold = True
        r.energy_threshold = 2000 
        r.pause_threshold = 0.8 
        
        try:
            audio = r.listen(source, timeout=None)
            
            print("🔒 [TUNG] Memproses...")
            if os.name == 'nt':
                try:
                    import winsound
                    winsound.Beep(700, 200)
                except:
                    pass

            with open("temp_input.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            with open("temp_input.wav", "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(file.name, file.read()), 
                    model="whisper-large-v3", 
                    language="id"
                )
            
            text_result = transcription.text.strip()
            
            # FILTER HALUSINASI 
            if not text_result: return None
            if len(text_result) < 3: return None

            for blocked in HALLUCINATION_FILTER:
                if blocked == text_result.lower():
                    print(f"🗑️ Filtered Noise: '{text_result}'")
                    return None

            return text_result

        except sr.WaitTimeoutError:
            return None 
        except Exception as e:
            return None

def brain_process(text):
    """Brain: Llama 3"""
    print(f"👤 User: {text}")
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(time=datetime.now())},
                {"role": "user", "content": text}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error Brain: {e}")
        return {"type": "chat", "reply": "Maaf, error memproses."}

def control_system(command):
    """Hand: System Control"""
    try:
        if "wifi_off" in command:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=disable', shell=True)
        elif "wifi_on" in command:
            subprocess.run('netsh interface set interface "Wi-Fi" admin=enable', shell=True)
    except Exception as e:
        print(f"Error Sys: {e}")

def play_spotify(song_name):
    """Spotify Auto-Play dengan API atau fallback ke URI"""
    if spotify_client:
        try:
            # Search lagu
            results = spotify_client.search(q=song_name, limit=1, type='track')
            
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                track_uri = track['uri']
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                
                print(f"🎵 Playing: {track_name} by {artist_name}")
                
                # Coba putar di active device
                try:
                    spotify_client.start_playback(uris=[track_uri])
                    return f"Memutar {track_name} oleh {artist_name}"
                except Exception as e:
                    # Jika tidak ada active device, buka di browser
                    print(f"⚠️ No active device, opening in browser: {e}")
                    webbrowser.open(track['external_urls']['spotify'])
                    return f"Membuka {track_name} di Spotify"
            else:
                return "Lagu tidak ditemukan"
                
        except Exception as e:
            print(f"Error Spotify API: {e}")
            # Fallback ke URI scheme
            if os.name == 'nt':
                os.system(f'start spotify:search:"{song_name}"')
            else:
                os.system(f'open "spotify:search:{song_name}"')
            return f"Mencari {song_name} di Spotify"
    else:
        # Fallback jika tidak ada API
        if os.name == 'nt':
            os.system(f'start spotify:search:"{song_name}"')
        else:
            os.system(f'open "spotify:search:{song_name}"')
        return f"Mencari {song_name} di Spotify"

# 4. MAIN LOOP
async def main():
    print("🤖 ConvBot - READY")
    print("Tunggu bunyi 'TING' baru ngomong.")
    print("Tip: Bilang 'Stop' atau 'Cukup' untuk mematikan.")
    
    while True:
        try:
            # 1. DENGAR
            user_text = listen_mic()
            if not user_text: continue

            # 2. MIKIR
            data = brain_process(user_text)

            # 3. BERTINDAK
            
            # Cek Close
            if data["type"] == "close":
                await speak(data["reply"])
                print("👋 Bye! (Voice Stop)")
                break

            # Cek Action
            if data["type"] == "action":
                target = data["target"].lower()
                content = data.get("content", "")
                category = data.get("category", "")
                
                print(f"⚙️ Execute: {category} -> {target}")

                if category == "playback":
                    if "youtube" in target:
                        print(f"🎬 Opening YouTube: {content}")
                        query = content.replace(" ", "+")
                        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                    
                    elif "spotify" in target:
                        print(f"🎵 Opening Spotify: {content}")
                        try:
                            open_app("Spotify", match_closest=True)
                            await asyncio.sleep(2)  
                            if os.name == 'nt':
                                os.system(f'start spotify:search:"{content}"')
                            else:
                                webbrowser.open(f"spotify:search:{content}")
                        except:
                            # Fallback: buka Spotify web
                            print("⚠️ Gagal akses desktop. Membuka Spotify Web...")
                            webbrowser.open(f"https://open.spotify.com/search/{content}")

                elif category == "web":
                    if not target.startswith("http"): target = f"https://{target}"
                    webbrowser.open(target)

                elif category == "app":
                    open_app(target, match_closest=True)

                elif category == "sys":
                    if "off" in target:
                        await speak(data["reply"]) 
                        control_system(target)
                        continue
                    else:
                        control_system(target)
                        await asyncio.sleep(4)

            # Cek Reply
            if "reply" in data and data["reply"]:
                await speak(data["reply"])
            
            await asyncio.sleep(0.5)

        except KeyboardInterrupt:
            print("\n👋 Bye! (Ctrl+C)")
            break
        except Exception as e:
            print(f"Critical Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())