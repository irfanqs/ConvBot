# 🎵 Spotify Auto-Play Setup Guide

## Prerequisites
- ✅ Spotify Premium account (required for Development Mode API)
- ✅ Spotify app installed on your computer

## Step-by-Step Setup

### 1️⃣ Create Spotify Developer App

1. **Login ke Spotify Developer**
   - Buka: https://developer.spotify.com/dashboard
   - Login dengan akun Spotify Premium kamu

2. **Create New App**
   - Klik tombol **"Create app"** (hijau)

3. **Fill App Information**
   ```
   App name: ConvBot
   App description: Voice-controlled Spotify assistant
   Website: http://localhost (atau kosongkan)
   Redirect URI: http://localhost:8888/callback
   ```
   
   ⚠️ **PENTING:** Redirect URI harus **PERSIS** `http://localhost:8888/callback`

4. **Accept Terms**
   - Centang "I understand and agree with Spotify's Developer Terms of Service and Design Guidelines"
   - Klik **"Save"**

### 2️⃣ Get API Credentials

1. Klik app yang baru dibuat (ConvBot)
2. Klik **"Settings"** di pojok kanan atas
3. Copy credentials:
   - **Client ID** - langsung terlihat
   - **Client Secret** - klik "View client secret" untuk lihat

### 3️⃣ Update .env File

Buka file `.env` di root project dan tambahkan:

```env
# Groq API (sudah ada)
GROQ_API_KEY=gsk_your_groq_key_here

# Spotify API Credentials (tambahkan ini)
SPOTIFY_CLIENT_ID=paste_client_id_disini
SPOTIFY_CLIENT_SECRET=paste_client_secret_disini
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

**Contoh:**
```env
GROQ_API_KEY=gsk_abc123xyz...
SPOTIFY_CLIENT_ID=1a2b3c4d5e6f7g8h9i0j
SPOTIFY_CLIENT_SECRET=9z8y7x6w5v4u3t2s1r0q
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

### 4️⃣ First Run Authentication

1. **Jalankan bot:**
   ```bash
   python main.py
   ```

2. **Browser akan terbuka otomatis** untuk login Spotify
   - Jika tidak terbuka, copy URL dari terminal dan paste di browser

3. **Login dan Authorize**
   - Login dengan akun Spotify Premium kamu
   - Klik **"Agree"** untuk authorize ConvBot

4. **Redirect ke localhost**
   - Setelah authorize, akan redirect ke `http://localhost:8888/callback?code=...`
   - **NORMAL** jika halaman error "Unable to connect" - kode sudah tersimpan!

5. **Bot siap digunakan!**
   - Terminal akan show: `✅ Spotify API Connected!`
   - Token tersimpan di `.cache` - tidak perlu login lagi

## 🎯 Usage Examples

Setelah setup, kamu bisa:

### Auto-Play Commands:
- **"Play Perfect by Ed Sheeran"** → Langsung putar lagu
- **"Play Shape of You"** → Auto search dan play
- **"Putar lagu Dua Lipa"** → Cari dan putar

### Requirements:
- Spotify app harus **terbuka di background**
- Harus ada **active device** (desktop app, phone, web player)

## ⚠️ Troubleshooting

### Problem: "No active device found"
**Solution:**
- Buka Spotify app di komputer/phone
- Play lagu apapun sekali (bisa langsung pause)
- Coba lagi command voice

### Problem: "Spotify API not configured"
**Solution:**
- Pastikan `.env` sudah diisi dengan benar
- Check Client ID & Secret tidak ada spasi di awal/akhir
- Restart `python main.py`

### Problem: Browser tidak terbuka saat first run
**Solution:**
- Copy URL dari terminal
- Paste di browser manual
- Login dan authorize

### Problem: "Invalid client" error
**Solution:**
- Double check Client ID dan Secret di `.env`
- Pastikan tidak ada typo
- Pastikan Redirect URI sama persis: `http://localhost:8888/callback`

## 🔄 Without Spotify API

Jika tidak setup API atau tidak punya Premium:
- Bot tetap berfungsi!
- Gunakan mode **search** (bukan auto-play)
- Command: "Play Perfect on Spotify" → Buka search page
- Kamu harus klik play manual

## 📝 Notes

- **Development Mode Limits (Feb 2026):**
  - Wajib Spotify Premium
  - Max 1 Client ID per developer
  - Max 5 authorized users
  - Limited API endpoints

- **Token Storage:**
  - File `.cache` menyimpan auth token
  - Jangan share file ini (add to `.gitignore`)
  - Token auto-refresh, tidak perlu login berulang

- **Scope yang Digunakan:**
  - `user-modify-playback-state` - Control playback
  - `user-read-playback-state` - Read current state
  - `user-read-currently-playing` - See current track

## 🎉 Success!

Kalau sudah setup dengan benar, kamu akan lihat di terminal:
```
✅ Spotify API Connected!
🤖 ConvBot - READY
```

Selamat menikmati auto-play! 🎵✨
