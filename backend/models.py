from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
from database import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key =True, index=True)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    created_at = Column(DateTime)

class UserCategories(Base):
    __tablename__ = 'usercategories'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

class UserSubategories(Base):
    __tablename__ = 'usersubcategories'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))

class Recomendations(Base):
    __tablename__ = 'recomendations'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    event_id = Column(Integer, ForeignKey("events.id"))


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    name = Column(String)

class Subcategories(Base):
    __tablename__ = 'subcategories'
    id = Column (Integer, primary_key=True, index=True)
    name = Column (String)

class Events(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    url = Column(String)
    # image = Column()
    location = Column(String)
    description = Column(String)
    name = Column (String)
    DateTime = Column(DateTime)
