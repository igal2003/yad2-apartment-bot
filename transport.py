from geopy.distance import geodesic

TRAM_STATIONS = [
    {"name": "הר הרצל", "lat": 31.7736, "lon": 35.1794},
    {"name": "יפה נוף", "lat": 31.7772, "lon": 35.1853},
    {"name": "הרכבת הקלה בית הכרם", "lat": 31.7795, "lon": 35.1905},
    {"name": "קרית משה", "lat": 31.7861, "lon": 35.1994},
    {"name": "הטורים", "lat": 31.7892, "lon": 35.2058},
    {"name": "מחנה יהודה", "lat": 31.7857, "lon": 35.2128},
    {"name": "יפו מרכז", "lat": 31.7827, "lon": 35.2197},
    {"name": "העיר העתיקה", "lat": 31.7785, "lon": 35.2287},
    {"name": "שמעון הצדיק", "lat": 31.7931, "lon": 35.2299},
    {"name": "גבעת המבתר", "lat": 31.8058, "lon": 35.2338},
    {"name": "פסגת זאב מרכז", "lat": 31.8246, "lon": 35.2399},
]

def nearest_tram_station(lat, lon):
    if not lat or not lon:
        return None, None

    distances = []

    for station in TRAM_STATIONS:
        distance = geodesic(
            (lat, lon),
            (station["lat"], station["lon"])
        ).meters

        distances.append((station["name"], round(distance)))

    return min(distances, key=lambda x: x[1])