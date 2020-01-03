from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, BigInteger 
from flask_login import UserMixin

Base = declarative_base()


class Restaurants(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact = Column(BigInteger, nullable=False)
    res_type = Column(String(50), nullable=True)
    minimum_order = Column(Integer, default=0)
    opening_time = Column(String(30), nullable=False)
    closing_time = Column(String(30), nullable=False)
            
    def __init__(self, name, contact, res_type, opening_time, closing_time, minimum_order = 0):
        self.name = name
        self.contact = contact
        self.res_type = res_type
        self.minimum_order = minimum_order
        self.opening_time = opening_time
        self.closing_time = closing_time

    def __repr__(self):
        return str(self.name) 


class Users(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(500), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(50), nullable=False)
    user_type = Column(Integer, default=0)
    address = Column(Text, nullable=True)
    contact = Column(BigInteger, nullable=True)

    def __init__(self, username, password, email, name, address="", contact="", user_type=0):
        self.username = username
        self.password = password
        self.email = email
        self.address = address
        self.contact = contact
        self.name = name
        self.user_type = user_type
    
    def __repr__(self):
        return self.name


class Recipes(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    origin = Column(String(30), nullable=True)

    def __init__(title, description, origin=None):
        self.title = title
        self.description = description
        self.origin = origin

    def __repr__(self):
        return self.title     


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    pincode = Column(Integer, nullable=False)
    city = Column(String(50), nullable=False)
    street = Column(String(200), nullable=False)
    area = Column(String(50), nullable=False)
    resturant_id = Column(ForeignKey('restaurants.id', ondelete="CASCADE"), nullable=False)
    longitude = Column(Integer, default=0)
    latitude = Column(Integer, default=0)

    def __init__(self, pincode, city, street, area, rest_id, latitude=0, longitude=0):
        self.pincode = pincode
        self.city = city
        self.street = street
        self.area = area
        self.resturant_id = rest_id
        self.longitude = longitude
        self.latitude = latitude
    
    def __repr__(self):
        return str(self.name)


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    category = Column(String(30), nullable=False)
    photoURL = Column(String(400), nullable=True)
    rest_id = Column(ForeignKey('restaurants.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, name, category, description, price, rest_id, photoURL=''):
        self.name = name 
        self.price = price
        self.category = category
        self.photoURL = photoURL
        self.description = description
        self.rest_id = rest_id

    def __repr__(self):
        return str(self.name)   


class Owner(Base):
    __tablename__ = 'owners'
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    rest_id = Column(ForeignKey('restaurants.id', ondelete="CASCADE"), nullable=False)
    
    def __init__(self, user_id, rest_id):
        self.user_id = user_id
        self.rest_id = rest_id
    
    def __repr__(self):
        return 'Owner'


def initialize_tables(engine):
   Base.metadata.create_all(engine)
