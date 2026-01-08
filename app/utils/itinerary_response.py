from datetime import datetime

def build_itinerary_response(itinerary):
    now_ts = int(datetime.now().timestamp() * 1000)

    itinerary_details = []

    for index, wrapper in enumerate(itinerary.activities, start=1):
        activity = wrapper["activity"]

        itinerary_details.append({
            "itineraryDetailsId": index,  # temp id
            "day": index,
            "date": itinerary.first_activity_date.strftime("%d-%m-%Y"),
            "activity": activity,
            "createdDate": now_ts,
            "modifiedDate": now_ts,
            "dayStatus": "PENDING",
            "startTimestamp": None,
            "endTimestamp": None,
            "completedBy": None,
            "pickupTime": activity.get("startTime")
        })

    return {
        "status": {
            "httpCode": "200",
            "success": True,
            "message": "Success"
        },
        "data": {
            "itineraryId": itinerary.id,
            "itineraryDetails": itinerary_details,
            "packageBookingId": itinerary.package_booking_id,
            "createdDate": now_ts,
            "modifiedDate": now_ts,
            "isMailSend": False
        }
    }
