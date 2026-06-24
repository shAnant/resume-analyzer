from sqlalchemy import Column, Integer, ForeignKey, DOUBLE_PRECISION
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class RoleSkills(Base):
    __tablename__ = "role_skills"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
    importance = Column(DOUBLE_PRECISION)
    
    role = relationship(
        "Roles",
        back_populates=""
    )
    
    skill = relationship(
        "Skills",
        back_populates="role_skill"
    )