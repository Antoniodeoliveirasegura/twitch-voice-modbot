# 🎙️ Twitch Voice-Controlled Moderation Bot

NOT FULLY DONE, USING WHISPER FOR TRANSCRIBING DOES NOT FULLY WORK

This bot listens to your Twitch livestream audio, detects moderation phrases like “timeout [word]” or “remove [word]”, and updates your Nightbot blacklist in real-time. Perfect for streamers who want voice-only control over chat moderation.

## ✨ Features
- 🎧 Live audio capture from Twitch using Streamlink + FFmpeg
- 🧠 Speech-to-text transcription via OpenAI Whisper
- 🛡️ Auto-blacklisting of toxic words via Nightbot API
- 🗣 Supports commands: `timeout [word]`, `remove [word]`, `clear blacklist`
- 📝 Logs every moderation update to `banned_log.txt`

## 🚀 How It Works
1. Captures 5 seconds of audio from your Twitch channel
2. Transcribes it using Whisper
3. Parses voice commands
4. Updates Nightbot's blacklist accordingly
5. Repeats every 5 seconds

## 🔧 Setup Instructions

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/twitch-voice-modbot.git
    cd twitch-voice-modbot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file:
    ```env
    NIGHTBOT_TOKEN=your_nightbot_token
    TWITCH_USERNAME=your_twitch_channel_name
    ```

4. Run the bot:
    ```bash
    python run_bot.py
    ```

## 📂 File Overview
- `run_bot.py` – Main loop for audio capture, transcription, and blacklist updates
- `banned_log.txt` – History of added/removed blacklisted words
- `.env` – Contains Nightbot token and Twitch username

## ✅ Requirements
- Python 3.8+
- FFmpeg and Streamlink installed (`brew install ffmpeg streamlink` on macOS)
- Nightbot account with spam protection enabled
- Whisper (automatically downloaded)

## 🧪 Example Voice Commands
- `timeout cringe`
- `remove banana`
- `clear blacklist`

## 📄 License
MIT License – feel free to fork, use, and improve.
