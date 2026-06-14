import requests

YAD2_URL = "https://gw.yad2.co.il/recommendations/items/realestate?type=home&count=20&categoryId=2&roomValues=2,2.5&propertyValues=1&cityValues=3000&subCategoriesIds=2"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Referer": "https://www.yad2.co.il/realestate/rent/jerusalem-area"
}

def fetch_listings():
    response = requests.get(YAD2_URL, headers=HEADERS)
    response.raise_for_status()

    data = response.json().get("data", [])

    listings = []

    for group in data:
        for item in group:
            address = item.get("address", {})
            details = item.get("additionalDetails", {})
            meta = item.get("metaData", {})

            listing = {
                "ad_number": item.get("adNumber"),
                "token": item.get("token"),
                "price": item.get("price"),
                "rooms": details.get("roomsCount"),
                "sqm": details.get("squareMeter"),
                "neighborhood": address.get("neighborhood", {}).get("text"),
                "city": address.get("city", {}).get("text"),
                "lat": address.get("coords", {}).get("lat"),
                "lon": address.get("coords", {}).get("lon"),
                "description": meta.get("description", ""),
                "image": meta.get("coverImage"),
                "url": f"https://www.yad2.co.il/item/{item.get('token')}",
                "ad_type": item.get("adType"),
            }

            listings.append(listing)

    return listings


if __name__ == "__main__":
    from filters import is_good_listing

    listings = fetch_listings()
    good_listings = [l for l in listings if is_good_listing(l)]

    print(f"Total annonces: {len(listings)}")
    print(f"Annonces intéressantes: {len(good_listings)}")

    for l in good_listings:
        print("----")
        print(l)