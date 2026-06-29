import yaml
import requests
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "2127560202"

with open("concerts.yaml", "r") as f:
    data = yaml.safe_load(f)

concerts = data["concerts"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)

for concert in concerts:
    nom = concert["nom"]
    url = concert["url"]

    message = f"🎟 Test Ticketmaster Alert\n\nConcert surveillé : {nom}\n{url}"

    send_telegram(message)

print("Message envoyé.")
