import json
import os

from scraper import fetch_listings
from notifier import send_message
from transport import nearest_tram_station
from scoring import calculate_score

SEEN_FILE = "seen_ads.json"


def format_summary(listings):
    message = f"🏠 Scan Yad2 terminé\n\n{len(listings)} annonces analysées :\n"

    for i, l in enumerate(listings, start=1):
        message += f"""

{i}. ⭐ {l.get('score')}/100
📍 {l.get('neighborhood')}, {l.get('city')}
💰 {l.get('price')} ₪
🚪 {l.get('rooms')} חדרים
📐 {l.get('sqm')} m²
🚋 {l.get('tram_station')} — {l.get('tram_distance_m')} m
🔗 {l.get('url')}
"""

    return message


def scan_once():
    listings = fetch_listings()

    scored_listings = []

    for listing in listings:
        station, distance = nearest_tram_station(
            listing.get("lat"),
            listing.get("lon")
        )

        listing["tram_station"] = station
        listing["tram_distance_m"] = distance
        listing["score"] = calculate_score(listing)

        scored_listings.append(listing)

    scored_listings.sort(key=lambda x: x.get("score", 0), reverse=True)

    print(f"Annonces trouvées: {len(scored_listings)}")

    send_message(format_summary(scored_listings))


def main():
    print("Scan Yad2...")
    scan_once()
    print("Scan terminé.")


if __name__ == "__main__":
    main()