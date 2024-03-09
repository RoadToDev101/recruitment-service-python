from sqlalchemy import Column, Integer, String
from src.app.config.database.mysql import Base


class JobField(Base):
    __tablename__ = "job_field"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False, unique=True)
    slug = Column(String, nullable=False, unique=True)
