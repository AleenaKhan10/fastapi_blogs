from sqlalchemy import Column, String, Integer, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship


    
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="creator")

class Blog(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    creator = relationship("User", back_populates="blogs", cascade="all, delete")