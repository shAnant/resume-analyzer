from sqlalchemy import Column, Integer, DOUBLE_PRECISION, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database.base import Base

class GapAnalysis(Base):
    __tablename__ = "gap_analysis"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    matching_score = Column(DOUBLE_PRECISION)
    
    user = relationship(
        "Users",
        back_populates="gap_analysis"
    )
    
    role = relationship(
        "Roles",
        back_populates="role_gap_analysis"
    )