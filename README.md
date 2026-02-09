# ConvBot 🤖

A voice-controlled conversational AI assistant that can open apps, search the web, control your system, and chat with you in Indonesian.

## Features

- **Voice Input Recognition** - Speak to interact with ConvBot
- **Text-to-Speech Output** - Responses delivered via EdgeTTS with audio playback
- **App Opening** - Open applications on your system by voice command
- **Web Search** - Search the internet through voice commands
- **System Control** - Control WiFi and other system features
- **Media Playback Control** - Control Spotify and YouTube playback
- **Natural Chat** - Have conversations in Indonesian
- **Groq AI Integration** - Powered by Groq's fast API

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lexiiyz/ConvBot.git
   cd convbot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   Create a `.env` file in the root directory and add your Groq API key:
   ```
   GROQ_API_KEY=gsk_your_api_key_here
   ```
   
   Get your API key from [Groq Console](https://console.groq.com)

6. **[Optional] Setup Spotify Auto-Play**
   For automatic song playback (requires Spotify Premium):
   
   a. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   
   b. Create a new app:
      - App name: `ConvBot`
      - App description: `Voice-controlled Spotify bot`
      - Redirect URI: `http://localhost:8888/callback`
   
   c. Get your credentials from Settings:
      - Client ID
      - Client Secret (click "View client secret")
   
   d. Add to your `.env` file:
      ```
      SPOTIFY_CLIENT_ID=your_client_id_here
      SPOTIFY_CLIENT_SECRET=your_client_secret_here
      SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
      ```
   
   e. First run will open browser for authentication - login and authorize the app
   
   **Note:** Without Spotify API setup, bot will use basic search (no auto-play)

## Usage

Run the bot:
```bash
python main.py
```

Then speak your commands! Examples:
- "Play Perfect by Ed Sheeran" (auto-play with API, search without)
- "Open Spotify"
- "Search Python tutorials"
- "Turn off WiFi"
- "Play Levitating on Spotify"
- "Chat: How are you today?"

## Requirements

- Python 3.8+
- Groq API key
- Microphone for voice input
- Audio output device
- **[Optional]** Spotify Premium account (for auto-play feature)

## Dependencies

- `groq` - Groq API client
- `SpeechRecognition` - Voice input
- `AppOpener` - Open applications
- `edge-tts` - Text-to-speech
- `pygame` - Audio playback
- `python-dotenv` - Environment variable management
- `spotipy` - Spotify API integration
- `PyAudio` - Microphone audio capture

## License

MIT
