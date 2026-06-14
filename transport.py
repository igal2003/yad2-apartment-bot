import os
import requests
from dotenv import load_dotenv
from geopy.distance import geodesic

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY")

TRAM_STATIONS = [
    {"name": "הר הרצל", "lat": 31.7736, "lon": 35.1794},
    {"name": "יפה נוף", "lat": 31.7772, "lon": 35.1853},
    {"name": "בית הכרם", "lat": 31.7795, "lon": 35.1905},
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
        return None, None, None

    nearest = min(
        TRAM_STATIONS,
        key=lambda s: geodesic((lat, lon), (s["lat"], s["lon"])).meters
    )

    walk_distance, walk_minutes = walking_distance_to_station(
        lat, lon,
        nearest["lat"], nearest["lon"]
    )

    return nearest["name"], walk_distance, walk_minutes


def walking_distance_to_station(lat, lon, station_lat, station_lon):
    if not ORS_API_KEY:
        straight = geodesic((lat, lon), (station_lat, station_lon)).meters
        estimated = round(straight * 1.35)
        return estimated, round(estimated / 80)

    url = "https://api.openrouteservice.org/v2/directions/foot-walking"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "coordinates": [
            [lon, lat],
            [station_lon, station_lat]
        ]
    }

    response = requests.post(url, json=payload, headers=headers, timeout=20)

    if response.status_code != 200:
        straight = geodesic((lat, lon), (station_lat, station_lon)).meters
        estimated = round(straight * 1.35)
        return estimated, round(estimated / 80)

    data = response.json()
    summary = data["routes"][0]["summary"]

    distance_m = round(summary["distance"])
    duration_min = round(summary["duration"] / 60)

    return distance_m, duration_min