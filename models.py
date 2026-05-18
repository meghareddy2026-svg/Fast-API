from sqlalchemy import Column, Integer, String, Float
from database import Base

# USER TABLE
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)

# PRODUCT TABLE
class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
