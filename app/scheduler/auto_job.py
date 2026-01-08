# from app.services.swabi_api import get_booking_list, get_booking_detail
# from app.services.itinerary_generator import generate_itinerary_if_needed

# def auto_itinerary_job():
#     bookings = get_booking_list()

#     for b in bookings:
#         booking = get_booking_detail(b["packageBookingId"])
#         generate_itinerary_if_needed(booking)



import asyncio
from app.services.itinerary_generator import generate_itineraries

def auto_itinerary_job():
    """
    This function is called by APScheduler every interval.
    """
    print("Scheduler running: generating itineraries...")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_itineraries())
    print("Scheduler finished.")
