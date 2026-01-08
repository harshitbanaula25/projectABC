# from datetime import datetime, timedelta
# from app.config import PICKUP_BUFFER_MINUTES

# def calculate_pickup_time(first_activity_start, total_travel_minutes):
#     start = datetime.strptime(first_activity_start, "%H:%M")
#     pickup = start - timedelta(
#         minutes=total_travel_minutes + PICKUP_BUFFER_MINUTES
#     )
#     return pickup.time()



# from datetime import datetime, timedelta
# from app.config import PICKUP_BUFFER_MINUTES

# def calculate_pickup_datetime(
#     first_activity_date,     # date object (YYYY-MM-DD)
#     first_activity_start,    # "HH:MM"
#     total_travel_minutes
# ):
#     activity_datetime = datetime.strptime(
#         f"{first_activity_date} {first_activity_start}",
#         "%Y-%m-%d %H:%M"
#     )

#     pickup_datetime = activity_datetime - timedelta(
#         minutes=total_travel_minutes + PICKUP_BUFFER_MINUTES
#     )

#     return pickup_datetime


from datetime import datetime, timedelta
from app.config import PICKUP_BUFFER_MINUTES

def calculate_pickup_time(
    activity_date,
    opening_time,
    closing_time,
    activity_duration_minutes,
    total_travel_minutes
):
    """
    Calculates pickup datetime so that:
    - Activity finishes before closing time
    - Travel + buffer is respected
    """

    opening_dt = datetime.strptime(
        f"{activity_date} {opening_time}", "%Y-%m-%d %H:%M"
    )
    closing_dt = datetime.strptime(
        f"{activity_date} {closing_time}", "%Y-%m-%d %H:%M"
    )

    # Latest possible activity start
    latest_activity_start = closing_dt - timedelta(
        minutes=activity_duration_minutes
    )

    pickup_dt = latest_activity_start - timedelta(
        minutes=total_travel_minutes + PICKUP_BUFFER_MINUTES
    )

    # Safety rule: no night pickup
    if pickup_dt.hour < 5:
        pickup_dt = pickup_dt.replace(hour=7, minute=0)

    return pickup_dt
