# import requests
# from app.config import GEOCODING_BASE_URL

# def geocode_address(address: str):
#     r = requests.get(
#         f"{GEOCODING_BASE_URL}/search",
#         params={"q": address, "format": "json", "limit": 1},
#         headers={"User-Agent": "auto-itinerary"},
#         timeout=10
#     )
#     r.raise_for_status()
#     data = r.json()

#     if not data:
#         raise ValueError(f"Geocoding failed: {address}")

#     return float(data[0]["lat"]), float(data[0]["lon"])







import requests
from app.config import GEOCODING_BASE_URL

HEADERS = {
    "User-Agent": "auto-itinerary/1.0"
}

def _call_geocode(query: str):
    response = requests.get(
        f"{GEOCODING_BASE_URL}/search",
        params={
            "q": query,
            "format": "json",
            "limit": 1
        },
        headers=HEADERS,
        timeout=10
    )
    response.raise_for_status()
    return response.json()

def geocode_address(address: str):
    if not address:
        raise ValueError("Pickup address is empty")

    # Try full address
    data = _call_geocode(address)
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])

    #  Retry with simplified address (remove POI parts)
    simplified = address.split("-")[0].strip()
    if simplified != address:
        data = _call_geocode(simplified)
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])

    #  Last fallback: extract city/country keywords
    tokens = address.split(",")
    if len(tokens) >= 2:
        fallback = ",".join(tokens[-2:]).strip()
        data = _call_geocode(fallback)
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])

    # Final failure
    raise ValueError(f"Geocoding failed after retries: {address}")
