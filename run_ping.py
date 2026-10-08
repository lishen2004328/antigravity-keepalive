import os
import sys
import time
import requests

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("::error::Missing required GEMINI_API_KEY in environment/secrets.")
    sys.exit(1)

# 使用当前可用且性价比最高的轻量级模型列表
CANDIDATE_MODELS = [
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-3.5-flash-lite",
    "gemini-3.7-flash",
    "gemini-2.5-flash-lite"
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
