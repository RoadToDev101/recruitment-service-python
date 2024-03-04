from sqlalchemy import (
    Enum as SQLAlchemyEnum,
    func,
    Column,
    BigInteger,
    String,
    DateTime,
)
from app.config.database.mysql import Base
from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), nullable=True, unique=True, index=True)
    # email = Column(String(120), nullable=False, unique=True, index=True)
    hashed_password = Column(String(200), nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
