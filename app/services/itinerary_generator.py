from datetime import datetime, timedelta
from app.services.swabi_api import get_booking_list, get_booking_detail
from app.database import SessionLocal
from app.models.itinerary import Itinerary
from app.services.geocoding import geocode_address
from app.services.routing import get_travel_time_minutes
from app.services.time_utils import calculate_pickup_time

# from app.utils.activity_utils import get_first_activity_date

async def generate_itineraries(force=False, booking_id=None):
    """
    Generate itineraries automatically:
    - If force=True, ignores 2-day rule.
    - If booking_id provided, only generate for that booking.
    """

    created_itineraries = []

    # Fetch all bookings
    bookings = await get_booking_list()
    if booking_id:
        bookings = [b for b in bookings if b["packageBookingId"] == booking_id]

    db = SessionLocal()

    for booking in bookings:
        if not booking.get("pkg") or not booking["pkg"].get("packageActivities"):
            continue

        # first_activity_date = get_first_activity_date(booking)
        first_activity_date = datetime.strptime(
        booking["bookingDate"], "%d-%m-%Y"
        ).date()
    




        # Skip if not 2 days before first activity, unless forced
        today = datetime.today().date()
        if not force and today != (first_activity_date - timedelta(days=2)):
            continue

        # Skip if itinerary already exists
        if db.query(Itinerary).filter_by(package_booking_id=booking["packageBookingId"]).first():
            continue

        # Pickup location


        # pickup_address = booking.get("pickupLocation", {}).get(str(first_activity_date), "")
        pickup_locations = booking.get("pickupLocation", {})

        date_key = first_activity_date.strftime("%d-%m-%Y")

        pickup_address = pickup_locations.get(date_key)

# fallback: pick any available pickup
        if not pickup_address and pickup_locations:
      
            pickup_address = list(pickup_locations.values())[0]

        if not pickup_address:
            raise Exception("Pickup location not found")


        pickup_lat, pickup_lng = geocode_address(pickup_address)

        # Sort activities by start time
        activities = booking["pkg"]["packageActivities"]
        activities.sort(key=lambda x: x["activity"]["startTime"])

        # Calculate total travel time from pickup through all activities
        total_travel_minutes = 0
        prev_lat, prev_lng = pickup_lat, pickup_lng
        for a in activities:
            lat, lng = geocode_address(a["activity"]["address"])
            total_travel_minutes += get_travel_time_minutes(prev_lat, prev_lng, lat, lng)
            prev_lat, prev_lng = lat, lng




        # Calculate pickup time

        # pickup_time = calculate_pickup_time(activities[0]["activity"]["startTime"], total_travel_minutes)

        

        # pickup_time_only = calculate_pickup_time(
        # activities[0]["activity"]["startTime"],
        # total_travel_minutes)

        activity = activities[0]["activity"]

        pickup_datetime = calculate_pickup_time(
        activity_date=first_activity_date,
        opening_time=activity["startTime"],     # e.g. 10:00
        closing_time=activity["endTime"],       # e.g. 18:00
        activity_duration_minutes=activity["activityHours"] * 60,
        total_travel_minutes=total_travel_minutes)





        # pickup_datetime = datetime.combine(
        #     first_activity_date,
        #     pickup_time_only
        # )

        # Create and store itinerary
        db_itinerary = Itinerary(
            package_booking_id=booking["packageBookingId"],
            pickup_address=pickup_address,
            pickup_lat=pickup_lat,
            pickup_lng=pickup_lng,
            pickup_time=pickup_datetime,
            activities=activities,  # stored as JSON
            first_activity_date=first_activity_date
        )

        db.add(db_itinerary)
        db.commit()
        db.refresh(db_itinerary)

        # created_itineraries.append({
        #     "package_booking_id": booking["packageBookingId"],
        #     "pickup_time": pickup_datetime.isoformat(),
        #     "activities": activities
        # })
        created_itineraries.append(db_itinerary)

    db.close()
    return created_itineraries
