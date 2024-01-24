from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.config.database.mysql import Base


class Seeker(Base):
    __tablename__ = "seeker"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    birthday = Column(String, nullable=False)  # yyyy-MM-dd
    address = Column(String, nullable=False)
    province = Column(Integer, ForeignKey("job_province.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    from app.api.models.resume_model import Resume

    resume_data = relationship("Resume", back_populates="seeker_data")
    province_data = relationship("Province", back_populates="seekers")
