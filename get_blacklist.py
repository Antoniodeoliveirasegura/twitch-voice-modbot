import requests
from dotenv import load_dotenv
import os

load_dotenv()

NIGHTBOT_TOKEN = os.getenv("NIGHTBOT_TOKEN")
NIGHTBOT_API = "https://api.nightbot.tv/1/spam_protection/blacklist"

def fetch_blacklist():
    headers = {
        "Authorization": f"Bearer {NIGHTBOT_TOKEN}"
    }
    response = requests.get(NIGHTBOT_API, headers=headers)

    if response.status_code == 200:
        print("Raw response:", response.text)
        data = response.json()["filter"]["blacklist"]
        print("📋 Current Nightbot Blacklisted Words:")
        print("-" * 40)
        for word in data.split("\\n"):
            if word.strip():
                print(f"- {word}")

    else:
        print("❌ Failed to fetch blacklist:", response.status_code, response.text)

if __name__ == "__main__":
    fetch_blacklist()
