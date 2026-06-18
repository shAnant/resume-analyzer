from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class UserSkills(Base):
    __tablename__ = "user_skills"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
    
    user = relationship(
        "Users",
        back_populates="user_skills"
    )
    
    skill = relationship(
        "Skills",
        back_populates="user_skills"
    )