from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class Roles(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    role_name = Column(Text)
    
    role_gap_analysis = relationship(
        "GapAnalysis",
        back_populates="role"
    )
    
    role_missing_skills = relationship(
        "MissingSkills",
        back_populates="role"
    )
    
    role_skill = relationship(
        "RoleSkills",
        back_populates="skill"
    )