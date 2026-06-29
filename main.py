import yaml
import requests
import os
from checker import check_ticketmaster

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "2127560202"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)

with open("concerts.yaml", "r") as f:
    data = yaml.safe_load(f)

concerts = data["concerts"]

for concert in concerts:
    nom = concert["nom"]
    url = concert["url"]

    available = check_ticketmaster(url)

    if available:
        message = f"🚨 Billets détectés !\n\n🎟 {nom}\n{url}"
        send_telegram(message)
        print(f"{nom} disponible")
    else:
        print(f"{nom} indisponible")
