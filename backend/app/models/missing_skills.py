from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class MissingSkills(Base):
    __tablename__ = "missing_skills"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), primary_key=True)
    
    user = relationship(
        "Users",
        back_populates="user_missing_skill"
    )

    role = relationship(
        "Roles",
        back_populates="role_missing_skills"
    )

    skill = relationship(
        "Skills",
        back_populates="skill_missing"
    )