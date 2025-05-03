import subprocess
import whisper
import re
import requests
import os
import time
from dotenv import load_dotenv

# === Load token from .env ===
load_dotenv()
NIGHTBOT_TOKEN = os.getenv("NIGHTBOT_TOKEN")

# === CONFIG ===
TWITCH_CHANNEL = os.getenv("TWITCH_USERNAME")
AUDIO_FILE = "stream_audio.wav"
WHISPER_MODEL = "tiny"
CHECK_INTERVAL = 5
NIGHTBOT_API = "https://api.nightbot.tv/1/spam_protection/blacklist"

# Track blacklist locally
blacklist = set()

def download_audio():
    print("Capturing Twitch stream audio...")
    command = f"streamlink https://www.twitch.tv/{TWITCH_CHANNEL} audio_only -O | ffmpeg -loglevel quiet -i - -t {CHECK_INTERVAL} -vn -acodec pcm_s16le -ar 16000 -ac 1 {AUDIO_FILE}"
    subprocess.call(command, shell=True)

def transcribe_audio():
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(AUDIO_FILE)
    return result.get("text", "")

def parse_commands(text):
    text = text.lower().replace(",", "").replace(".", "").strip()
    commands = []

    if "clear blacklist" in text:
        commands.append(("clear", None))
        return commands

    timeout_matches = re.findall(r"(?:timeout|time out)\s+(.+?)(?=timeout|time out|remove|clear blacklist|$)", text)
    for phrase in timeout_matches:
        clean = phrase.strip(".,!? ").strip()
        if clean:
            commands.append(("add", clean))

    remove_matches = re.findall(r"remove\s+(.+?)(?=timeout|time out|remove|clear blacklist|$)", text)
    for phrase in remove_matches:
        clean = phrase.strip(".,!? ").strip()
        if clean:
            commands.append(("remove", clean))

    return commands

def update_nightbot_blacklist(commands):
    headers = { "Authorization": f"Bearer {NIGHTBOT_TOKEN}" }
    resp = requests.get(NIGHTBOT_API, headers=headers)

    if resp.status_code != 200:
        print("Failed to fetch current blacklist.")
        return

    current_list = set(resp.json()["filter"]["blacklist"].split("\n"))

    for action, word in commands:
        if action == "clear":
            current_list.clear()
            print("Blacklist cleared.")
        elif action == "add":
            if word not in current_list:
                current_list.add(word)
                print(f"Added: '{word}'")
        elif action == "remove":
            if word in current_list:
                current_list.remove(word)
                print(f"Removed: '{word}'")

    payload = {
        "blacklist": "\n".join(current_list),
        "length": 60,
        "enabled": True
    }

    update_resp = requests.put(NIGHTBOT_API, json=payload, headers=headers)

    if update_resp.status_code == 200:
        print("Nightbot blacklist updated.")
        with open("banned_log.txt", "a") as log_file:
            for action, word in commands:
                if action in ("add", "remove"):
                    log_file.write(f"{action.upper()}: {word}\n")
    else:
        print("Update failed:", update_resp.text)

# === LIVE MODE LOOP ===
if __name__ == "__main__":
    print("Voice-controlled Twitch moderation bot started (LIVE MODE)")
    while True:
        download_audio()
        transcript = transcribe_audio()
        print("Transcript:", transcript)
        commands = parse_commands(transcript)
        if commands:
            update_nightbot_blacklist(commands)
        else:
            print("No moderation commands detected.")
        time.sleep(CHECK_INTERVAL)
