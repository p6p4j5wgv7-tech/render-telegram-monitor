
import os
import time
import json
import urllib.request
import urllib.parse
import urllib.error

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "1196075247"
SITE_URL = "https://kindergarten-absence-1.onrender.com/"

API = f"https://api.telegram.org/bot{TOKEN}/"

running = False
next_check = 0
last_update_id = 0

def send_message(text):
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text
    }).encode()

    req = urllib.request.Request(
        API + "sendMessage", data=data
    )
    urllib.request.urlopen(req, timeout=30)

def check_site():
    try:
        req = urllib.request.Request(
            SITE_URL,
            headers={"User-Agent": "RenderMonitor/1.0"}
        )
        response = urllib.request.urlopen(req, timeout=60)
        return f"✅ الموقع يستجيب\nHTTP: {response.status}"
    except Exception as e:
        return f"❌ الموقع لا يستجيب\n{str(e)[:300]}"

def get_updates():
    global last_update_id

    url = API + "getUpdates?" + urllib.parse.urlencode({
        "offset": last_update_id + 1,
        "timeout": 0
    })

    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())

send_message("🤖 البوت جاهز! أرسل /start للتشغيل.")

while True:
    try:
        updates = get_updates()

        for update in updates.get("result", []):
            last_update_id = update["update_id"]

            msg = update.get("message", {})
            chat = msg.get("chat", {})
            text = msg.get("text", "")

            if str(chat.get("id")) != CHAT_ID:
                continue

            if text == "/start":
                running = True
                next_check = 0
                send_message("🚀 بدأت مراقبة موقعك كل 10 دقائق.")

            elif text == "/stop":
                running = False
                send_message("🛑 تم إيقاف المراقبة.")

            elif text == "/status":
                state = "شغالة ✅" if running else "متوقفة 🛑"
                send_message(f"حالة المراقبة: {state}")

            elif text == "/check":
                send_message("🔍 أفحص موقعك الآن...")
                send_message(check_site())

        if running and time.time() >= next_check:
            send_message(check_site())
            next_check = time.time() + 600

    except Exception as e:
        print("Error:", e)

    time.sleep(3)
