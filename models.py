from sqlalchemy import Column, Integer, String, Float
from database import db

class Cars(db):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(50), index=True)
    mark_name = Column(String(50), index=True)
    fuel = Column(Integer)
    grade = Column(Float)
    start_year = Column(Integer)
    age = Column(Integer)
