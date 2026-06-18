from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    
    gap_analysis = relationship(
        "GapAnalysis",
        back_populates="user"
    )
    
    user_missing_skill = relationship(
        "MissingSkills",
        back_populates="user"
    )
    
    user_skills = relationship(
        "UserSkills",
        back_populates="user"
    )