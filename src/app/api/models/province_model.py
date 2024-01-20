from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.config.database.mysql import Base


class Province(Base):
    __tablename__ = "job_province"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)

    employers = relationship("Employer", back_populates="province_data")
    seekers = relationship("Seeker", back_populates="province_data")

    # jobs = relationship("Job", back_populates="province", cascade="all, delete-orphan")
