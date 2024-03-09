from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from src.app.config.database.mysql import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    employer_id = Column(BigInteger, ForeignKey("employer.id"), nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    fields = Column(String, nullable=False)
    provinces = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    expired_at = Column(DateTime, nullable=False)

    employer_data = relationship("Employer", back_populates="jobs_data")
