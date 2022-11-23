from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,index=True)
    hashed_password = Column(String)   

class Anime(Base):
    __tablename__ = "anime"
    id = Column(Integer, primary_key=True, index=True)
    currEpisode = Column(Integer, index=True)
    title = Column(String, index=True)
    recurring = Column(String, index=True)
    caughtUp = Column(Boolean, index=True)
    notes = Column(String, index=True)
    
class Manga(Base):
    __tablename__ = "manga"
    id = Column(Integer, primary_key=True, index=True)
    currChapter = Column(Integer, index=True)
    title = Column(String, index=True)
    recurring = Column(String, index=True)
    caughtUp = Column(Boolean, index=True)
    notes = Column(String, index=True)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("Users")
    
    

