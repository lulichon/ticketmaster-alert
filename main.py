import yaml
import requests
import os
import json
from datetime import datetime, timezone
from checker import check_ticketmaster

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "2127560202"
STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload, timeout=20)


with open("concerts.yaml", "r") as f:
    data = yaml.safe_load(f)

concerts = data["concerts"]
state = load_state()

now = datetime.now(timezone.utc).isoformat()

state["_meta"] = {
    "last_global_check": now
}

for concert in concerts:
    nom = concert["nom"]
    url = concert["url"]

    result = check_ticketmaster(url)

    available = result["available"]
    status = result["status"]

    previous_data = state.get(nom, {})
    previous_available = previous_data.get("available", False)
    previous_last_available = previous_data.get("last_available_at", "Jamais détectée")

    print(f"{nom} : {'disponible' if available else 'indisponible'}")

    last_available_at = previous_last_available

    if available:
        last_available_at = now

    if available and not previous_available:
        message = f"🚨 Billets détectés !\n\n🎟 {nom}\n🔗 {url}"
        send_telegram(message)
        print(f"Alerte envoyée pour {nom}")

    state[nom] = {
        "available": available,
        "status": status,
        "last_checked": now,
        "last_available_at": last_available_at,
        "category": result.get("category", "Catégorie inconnue"),
        "url": url
    }

save_state(state)
