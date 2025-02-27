from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key= True, index= True) #primary key
    username = Column(String)
    email = Column(String)
    phone = Column(String)
    password = Column(String)
    favorites = relationship("Favorites", back_populates="user")



class Favorites(Base):
    __tablename__ = 'Favorites'
    id = Column(Integer, primary_key= True, index= True)
    company = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship("User", back_populates="favorites")