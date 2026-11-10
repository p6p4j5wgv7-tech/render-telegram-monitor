
import os
import urllib.request
import urllib.parse
from datetime import datetime

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = "1196075247"
SITE = "https://kindergarten-absence-1.onrender.com/"

def send_message(message):
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": message
    }).encode()

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data=data
    )

    urllib.request.urlopen(req, timeout=30)

try:
    req = urllib.request.Request(
        SITE,
        headers={"User-Agent": "WebsiteMonitor/1.0"}
    )

    response = urllib.request.urlopen(req, timeout=60)

    send_message(
        f"✅ موقعك يستجيب!\nHTTP: {response.status}\n{datetime.now()}"
    )

except Exception as error:
    send_message(
        f"❌ مشكلة في الموقع!\n{str(error)[:300]}"
    )
