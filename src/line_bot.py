import requests
import os
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")


def send_line(message: str, to: str = None):
    """發送訊息到 LINE Bot"""
    if not CHANNEL_ACCESS_TOKEN:
        raise ValueError("❌ LINE_CHANNEL_TOKEN not found in environment variables")
    if not USER_ID and not to:
        raise ValueError("❌ LINE_USER_ID not found in environment variables")

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }

    payload = {
        "to": to or USER_ID,
        "messages": [{"type": "text", "text": message}],
    }

    r = requests.post(url, headers=headers, json=payload)
    return r.status_code, r.text
