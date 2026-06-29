import requests

def check_ticketmaster(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    text = response.text.lower()
    final_url = response.url.lower()

    if "wait.ticketmaster" in final_url or "file d'attente" in text or "queue-it" in text:
        return {
            "available": False,
            "status": "queue"
        }

    unavailable_words = [
        "complet",
        "indisponible",
        "aucun billet",
        "sold out"
    ]

    available_words = [
        "réserver",
        "reserver",
        "acheter",
        "billets disponibles",
        "places disponibles"
    ]

    found_available = any(word in text for word in available_words)
    found_unavailable = any(word in text for word in unavailable_words)

    return {
        "available": found_available and not found_unavailable,
        "status": "available" if found_available and not found_unavailable else "unavailable"
    }
