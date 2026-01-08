# test_booking.py
import asyncio
from app.services.swabi_api import get_booking_list

async def main():
    bookings = await get_booking_list()
    print(bookings)

asyncio.run(main())
