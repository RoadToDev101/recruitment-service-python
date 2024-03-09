from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.app.config.database.mysql import Base


class Resume(Base):
    __tablename__ = "resume"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    seeker_id = Column(BigInteger, ForeignKey("seeker.id"), nullable=False)
    career_obj = Column(String, nullable=False)
    title = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    fields = Column(String, nullable=False)
    provinces = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    seeker_data = relationship("Seeker", back_populates="resume_data")
