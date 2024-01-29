from sqlalchemy import Column, String, Integer
from database.database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)