from scraper import fetch_listings
from notifier import send_message
from transport import nearest_tram_station
from scoring import calculate_score


def format_summary(listings):
    message = f"🏠 Scan Yad2 terminé\n\n{len(listings)} annonces à moins de 4000₪ analysées :\n"

    for i, l in enumerate(listings, start=1):
        message += f"""

{i}. ⭐ {l.get('score')}/100
📍 {l.get('neighborhood')}, {l.get('city')}
💰 {l.get('price')} ₪
🚪 {l.get('rooms')} חדרים
📐 {l.get('sqm')} m²
🚋 {l.get('tram_station')} — {l.get('tram_distance_m')} m à pied ({l.get('tram_walk_minutes')} min)
🔗 {l.get('url')}
"""

    return message


def scan_once():
    listings = fetch_listings()

    listings = [
        l for l in listings
        if (l.get("price") or 999999) <= 4000
    ]

    scored_listings = []

    for listing in listings:
        station, distance, minutes = nearest_tram_station(
            listing.get("lat"),
            listing.get("lon")
        )

        listing["tram_station"] = station
        listing["tram_distance_m"] = distance
        listing["tram_walk_minutes"] = minutes
        listing["score"] = calculate_score(listing)

        scored_listings.append(listing)

    scored_listings.sort(key=lambda x: x.get("score", 0), reverse=True)

    print(f"Annonces trouvées à moins de 4000₪: {len(scored_listings)}")

    send_message(format_summary(scored_listings))


def main():
    print("Scan Yad2...")
    scan_once()
    print("Scan terminé.")


if __name__ == "__main__":
    main()