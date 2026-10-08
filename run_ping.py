import os
import sys
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("::error::Missing required GEMINI_API_KEY in environment/secrets.")
    sys.exit(1)

def send_ping_message():
    """使用最轻量的 Gemini 3.8 Flash 模型发送短消息触发额度活跃"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": "hi"}
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 1
        }
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code == 200:
            print("✅ Keep-Alive Ping successful! Google AI response received and quota active.")
        else:
            print(f"::warning::Request returned status code {resp.status_code}: {resp.text}")
            sys.exit(1)
    except Exception as e:
        print(f"::error::Request exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Starting scheduled keep-alive ping...")
    send_ping_message()
    print("Done.")
