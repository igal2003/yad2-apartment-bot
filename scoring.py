def calculate_score(listing):
    score = 0

    price = listing.get("price") or 0
    sqm = listing.get("sqm") or 0
    tram_distance = listing.get("tram_distance_m")

    if price <= 3500:
        score += 35
    elif price <= 3800:
        score += 30
    elif price <= 4000:
        score += 20

    if sqm >= 45:
        score += 20
    elif sqm >= 35:
        score += 10

    if tram_distance is not None:
        if tram_distance <= 300:
            score += 35
        elif tram_distance <= 600:
            score += 25
        elif tram_distance <= 900:
            score += 10

    if listing.get("neighborhood") in ["בית וגן", "בית הכרם", "קרית משה", "קרית היובל", "קרית מנחם"]:
        score += 10

    return min(score, 100)