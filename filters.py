WATCHED_NEIGHBORHOODS_HE = [
    "גבעת שאול",
    "בית זית",
    "קרית משה",
    "בית הכרם",
    "בית וגן",
    "קרית היובל",
    "רמת דניה",
    "הר נוף",
    "קרית מנחם",
]

MAX_PRICE = 4000
MIN_ROOMS = 2
MAX_ROOMS = 2.5


def is_good_listing(listing):
    price = listing.get("price") or 0
    rooms = listing.get("rooms") or 0
    neighborhood = listing.get("neighborhood") or ""
    description = listing.get("description") or ""

    text = neighborhood + " " + description

    if price > MAX_PRICE:
        return False

    if rooms < MIN_ROOMS or rooms > MAX_ROOMS:
        return False

    if not any(area in text for area in WATCHED_NEIGHBORHOODS_HE):
        return False

    return True