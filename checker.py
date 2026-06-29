import requests

def check_ticketmaster(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=20)
    text = response.text.lower()

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
        "billets",
        "places disponibles"
    ]

    found_available = any(word in text for word in available_words)
    found_unavailable = any(word in text for word in unavailable_words)

    if found_available and not found_unavailable:
        return True

    return False
