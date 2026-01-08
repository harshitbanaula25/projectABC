# # main.py
# from fastapi import FastAPI, HTTPException
# from apscheduler.schedulers.background import BackgroundScheduler
# from app.scheduler.auto_job import auto_itinerary_job
# from app.database import Base, engine
# from app.config import SCHEDULER_INTERVAL_MINUTES
# from app.services.itinerary_generator import generate_itineraries

# # Create database tables
# Base.metadata.create_all(bind=engine)

# # Initialize FastAPI
# app = FastAPI(title="Auto Itinerary Service")

# # ---------------- Scheduler Setup ----------------
# scheduler = BackgroundScheduler()
# scheduler.add_job(
#     auto_itinerary_job,              # this is the scheduled job
#     "interval",
#     minutes=SCHEDULER_INTERVAL_MINUTES
# )
# scheduler.start()
# # ------------------------------------------------

# # ---------------- Manual Trigger API ----------------
# @app.post("/trigger-itinerary")
# async def trigger_itinerary(booking_id: int = None):
#     """
#     Manually trigger itinerary creation.
#     Optional query param:
#     - booking_id: create itinerary for a specific booking
#     """
#     try:
#         created_itineraries = await generate_itineraries(force=True, booking_id=booking_id)
#         return {
#             "status": "success",
#             "created_count": len(created_itineraries),
#             "itineraries": created_itineraries
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# # ----------------------------------------------------




# from fastapi import FastAPI, HTTPException
# from apscheduler.schedulers.background import BackgroundScheduler
# from app.scheduler.auto_job import auto_itinerary_job
# from app.database import Base, engine
# from app.config import SCHEDULER_INTERVAL_MINUTES
# from app.services.itinerary_generator import generate_itineraries

# # Create DB tables
# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Auto Itinerary Service")

# # Scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(auto_itinerary_job, "interval", minutes=SCHEDULER_INTERVAL_MINUTES)
# scheduler.start()

# # Manual trigger endpoint
# @app.post("/trigger-itinerary")
# async def trigger_itinerary(booking_id: int = None):
#     try:
#         created_itineraries = await generate_itineraries(force=True, booking_id=booking_id)
#         return {
#             "status": "success",
#             "created_count": len(created_itineraries),
#             "itineraries": created_itineraries
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



from fastapi import FastAPI, HTTPException, Query
from app.services.itinerary_generator import generate_itineraries
from fastapi.responses import JSONResponse
from app.database import Base, engine
import asyncio
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auto Itinerary Service", version="0.1.0")


# @app.post("/trigger-itinerary")
# async def trigger_itinerary(booking_id: int = Query(None, description="Booking ID to generate itinerary for")):

@app.post("/trigger-itinerary")
async def trigger_itinerary(
    booking_id: int = Query(None, description="Booking ID to generate itinerary for"),
    force: bool = Query(False, description="Force generate itinerary (ignore date rule)")
):
    
    """
    Trigger itinerary generation.
    - If booking_id is provided, generates for that booking only.
    - Otherwise, generates for all bookings that are 2 days before the first activity.
    """
    try:
        # created_itineraries = await generate_itineraries(booking_id=booking_id)
        created_itineraries = await generate_itineraries(
            booking_id=booking_id,
            force=force
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "created_count": len(created_itineraries),
                "itineraries": created_itineraries
            }
        )
    except Exception as e:
        # Catch all exceptions and return a JSON error
        raise HTTPException(status_code=500, detail=str(e))
