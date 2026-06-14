import time
import json
import os

from scraper import fetch_listings
from filters import is_good_listing
from notifier import send_message
from transport import nearest_tram_station
from scoring import calculate_score

SEEN_FILE = "seen_ads.json"


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()

    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def format_listing(l):
    return f"""
🏠 Nouvelle dira intéressante

📍 {l.get('neighborhood')}, {l.get('city')}
💰 {l.get('price')} ₪
🚪 {l.get('rooms')} חדרים
📐 {l.get('sqm')} m²

🚋 Tram le plus proche : {l.get('tram_station')}
📏 Distance tram : {l.get('tram_distance_m')} m

⭐ Score : {l.get('score')}/100

🔗 {l.get('url')}
"""


def scan_once():
    seen = load_seen()

    listings = fetch_listings()
    good_listings = [l for l in listings if is_good_listing(l)]

    print(f"Annonces trouvées: {len(listings)}")
    print(f"Annonces intéressantes: {len(good_listings)}")

    for listing in good_listings:
        token = listing.get("token")

        if token in seen:
            continue

        station, distance = nearest_tram_station(
            listing.get("lat"),
            listing.get("lon")
        )

        listing["tram_station"] = station
        listing["tram_distance_m"] = distance
        listing["score"] = calculate_score(listing)

        send_message(format_listing(listing))

        seen.add(token)
        save_seen(seen)


def main():
    while True:
        print("Scan Yad2...")
        scan_once()
        print("Pause 2 minutes...")
        time.sleep(120)


if __name__ == "__main__":
    main()