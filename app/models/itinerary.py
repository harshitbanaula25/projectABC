from sqlalchemy import Column, Integer, String, Date,Float,JSON, DateTime
from app.database import Base

class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True)
    package_booking_id = Column(Integer, unique=True, nullable=False)

    pickup_address = Column(String)
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    pickup_time = Column(DateTime)
    activities = Column(JSON, nullable=True)


    first_activity_date = Column(Date)


# from sqlalchemy import Column, Integer, String, DateTime, JSON 

# class Itinerary(Base):
#     __tablename__ = "itineraries"

#     id = Column(Integer, primary_key=True, index=True)
#     package_booking_id = Column(Integer, nullable=False)
#     pickup_address = Column(String, nullable=False)
#     pickup_time = Column(DateTime, nullable=False)
