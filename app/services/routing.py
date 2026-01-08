import requests
from app.config import ROUTING_BASE_URL

def get_travel_time_minutes(src_lat, src_lng, dst_lat, dst_lng):
    url = f"{ROUTING_BASE_URL}/route/v1/driving/{src_lng},{src_lat};{dst_lng},{dst_lat}"
    r = requests.get(url, params={"overview": "false"}, timeout=10)
    r.raise_for_status()
    return int(r.json()["routes"][0]["duration"] / 60)
