from sqlalchemy import Column, Integer, BigInteger, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database.mysql import Base


class Employer(Base):
    __tablename__ = "employer"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    province = Column(Integer, ForeignKey("job_province.id"), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    from .job_model import Job

    jobs_data = relationship(
        "Job", back_populates="employer_data", cascade="all, delete-orphan"
    )
    province_data = relationship("Province", back_populates="employers")
