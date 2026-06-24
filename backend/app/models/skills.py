from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Skills(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True)
    skill_name = Column(Text, unique=True)
    
    skill_missing = relationship(
        "MissingSkills",
        back_populates = "skill"
    )
    
    user_skills = relationship(
        "UserSkills",
        back_populates="skill"
    )