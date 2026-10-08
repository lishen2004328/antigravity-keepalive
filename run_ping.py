import os
import sys
import time
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("::error::Missing required GEMINI_API_KEY in environment/secrets.")
    sys.exit(1)

# 按优先级轮询最轻量模型，防止单个模型遇到临时 503 拥堵
CANDIDATE_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-2.5-pro"
]

def ping_model(model_name):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
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
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        if resp.status_code == 200:
            print(f"✅ Keep-Alive Ping successful with model [{model_name}]! Google AI response received.")
            return True
        else:
            print(f"Model [{model_name}] returned {resp.status_code}: {resp.text[:150]}")
            return False
    except Exception as e:
        print(f"Model [{model_name}] connection exception: {e}")
        return False

def main():
    print("Starting scheduled keep-alive ping with fallback models...")
    for model in CANDIDATE_MODELS:
        if ping_model(model):
            print("Ping finished successfully.")
            return
        time.sleep(2)
        
    print("::error::All candidate models failed to respond.")
    sys.exit(1)

if __name__ == "__main__":
    main()
