# import requests
# from app.config import (
#     SWABI_API_BASE_URL,
#     BOOKING_LIST_ENDPOINT,
#     BOOKING_DETAIL_ENDPOINT,
#     DEFAULT_VENDOR_ID,
#     BOOKING_STATUS
# )

# def get_booking_list():
#     r = requests.get(
#         f"{SWABI_API_BASE_URL}{BOOKING_LIST_ENDPOINT}",
#         params={
#             "pageNumber": -1,
#             "pageSize": -1,
#             "search": "",
#             "bookingStatus": BOOKING_STATUS,
#             "sortBy": "bookingId",
#             "sortDirection": "desc",
#             "vendorId": DEFAULT_VENDOR_ID
#         },
#         timeout=20
#     )
#     r.raise_for_status()
#     return r.json()["data"]

# def get_booking_detail(package_booking_id: int):
#     r = requests.get(
#         f"{SWABI_API_BASE_URL}{BOOKING_DETAIL_ENDPOINT}",
#         params={"packageBookingId": package_booking_id},
#         timeout=20
#     )
#     r.raise_for_status()
#     return r.json()["data"]



import httpx
from app.config import (
    BOOKING_LIST_ENDPOINT,
    BOOKING_DETAIL_ENDPOINT,
    DEFAULT_VENDOR_ID,
    BOOKING_STATUS
)

async def get_booking_list():
    params = {
        "pageNumber": -1,
        "pageSize": -1,
        "vendorId": DEFAULT_VENDOR_ID,
        "bookingStatus": BOOKING_STATUS,
        "sortBy": "bookingId",
        "sortDirection": "desc"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BOOKING_LIST_ENDPOINT, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

async def get_booking_detail(booking_id):
    url = f"{BOOKING_DETAIL_ENDPOINT}?packageBookingId={booking_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json().get("data", {})
