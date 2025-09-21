import requests
import os
import logging
from dotenv import load_dotenv

# 載入 .env
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_TOKEN")
USER_ID = os.getenv("LINE_USER_ID")


def send_line(message: str, to: str = None):
    """發送訊息到 LINE Bot"""
    if not CHANNEL_ACCESS_TOKEN:
        logging.error("❌ LINE_CHANNEL_TOKEN not found in environment variables")
        return 400, "Missing LINE_CHANNEL_TOKEN"
    if not USER_ID and not to:
        logging.error("❌ LINE_USER_ID not found in environment variables")
        return 400, "Missing LINE_USER_ID"

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }

    payload = {
        "to": to or USER_ID,
        "messages": [{"type": "text", "text": message}],
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        if r.status_code != 200:
            logging.error(f"❌ LINE API Error {r.status_code}: {r.text}")
        return r.status_code, r.text
    except Exception as e:
        logging.error(f"❌ Failed to send LINE message: {e}")
        return 500, str(e)
