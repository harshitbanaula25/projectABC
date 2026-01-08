from fastapi import FastAPI, HTTPException, Query
from app.services.itinerary_generator import generate_itineraries
from fastapi.responses import JSONResponse
from app.database import Base, engine
import asyncio
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auto Itinerary Service", version="0.1.0")


# # @app.post("/trigger-itinerary")
# # async def trigger_itinerary(booking_id: int = Query(None, description="Booking ID to generate itinerary for")):

# @app.post("/trigger-itinerary")
# async def trigger_itinerary(
#     booking_id: int = Query(None, description="Booking ID to generate itinerary for"),
#     force: bool = Query(False, description="Force generate itinerary (ignore date rule)")
# ):
    
#     """
#     Trigger itinerary generation.
#     - If booking_id is provided, generates for that booking only.
#     - Otherwise, generates for all bookings that are 2 days before the first activity.
#     """
#     try:
#         # created_itineraries = await generate_itineraries(booking_id=booking_id)
#         created_itineraries = await generate_itineraries(
#             booking_id=booking_id,
#             force=force
#         )

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "status": "success",
#                 "created_count": len(created_itineraries),
#                 "itineraries": created_itineraries
#             }
#         )
#     except Exception as e:
#         # Catch all exceptions and return a JSON error
#         raise HTTPException(status_code=500, detail=str(e))






from app.utils.itinerary_response import build_itinerary_response

@app.post("/trigger-itinerary")
async def trigger_itinerary(
    booking_id: int = Query(None),
    force: bool = Query(False)
):
    try:
        itineraries = await generate_itineraries(
            booking_id=booking_id,
            force=force
        )

        if not itineraries:
            return {
                "status": {
                    "httpCode": "200",
                    "success": True,
                    "message":  f"Itinerary already exists for booking ID {booking_id}. Duplicate itinerary creation is not allowed."
                },
                "data": None
            }

        # Swabi expects SINGLE itinerary response
        return build_itinerary_response(itineraries[0])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


