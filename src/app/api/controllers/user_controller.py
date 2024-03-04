from typing import List
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from app.api.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.api.models.user_model import User as UserModel
from app.utils.jwt import create_access_token
import logging
from app.utils.utils import remove_private_attributes
from app.common.custom_exception import (
    CredentialsException,
    NotFoundException,
    BadRequestException,
)
from app.api.schemas.access_token_schema import Payload
from app.common.pagination import Pagination


logging.getLogger("passlib").setLevel(logging.ERROR)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserController:
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Payload:
        user = db.query(UserModel).filter(UserModel.username == username).first()

        if not user:
            raise NotFoundException("User not found. Please register")
        if not verify_password(password, user.hashed_password):
            raise CredentialsException("Incorrect username or password")

        access_token = create_access_token(data={"sub": user.id})
        token_data = Payload(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            role=user.role,
        )
        return token_data

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> UserOut:
        # Hash the password
        hashed_password = get_password_hash(user.password)

        # Create the user
        new_user = UserModel(
            username=user.username,
            # email=user.email,
            hashed_password=hashed_password,
        )

        # Add the user to the database
        db.add(new_user)

        try:
            db.commit()
            db.refresh(new_user)
        except IntegrityError as e:
            raise BadRequestException("User already exists")
        except SQLAlchemyError as e:
            raise BadRequestException(f"Database error while creating user. Error: {e}")
        except Exception as e:
            raise BadRequestException(f"Error creating user. Error: {e}")

        user_dict = remove_private_attributes(
            new_user
        )  # Remove private attributes from the user object

        user_out = UserOut.model_validate(user_dict)

        return user_out

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> UserOut:
        try:
            user = db.query(UserModel).get(user_id)
            if user is None:
                raise NotFoundException("User not found")
            user_dict = remove_private_attributes(user)
            user_out = UserOut.model_validate(user_dict)
            return user_out
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve user")
        except Exception as e:
            raise BadRequestException(f"Failed to retrieve user: {e}")

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10) -> Pagination[UserOut]:
        try:
            users = db.query(UserModel).offset(skip).limit(limit).all()
            total_users = db.query(UserModel).count()
            users_out = []
            for user in users:
                user_dict = remove_private_attributes(user)
                user_out = UserOut.model_validate(user_dict)
                users_out.append(user_out)
            return Pagination[UserOut].create(users_out, skip, limit, total_users)
        except SQLAlchemyError:
            raise BadRequestException("Failed to retrieve users")
        except Exception as e:
            raise BadRequestException(f"Failed to retrieve users: {e}")

    @staticmethod
    def update_user_by_id(db: Session, user_id: int, user: UserUpdate) -> str:
        try:
            db_user = db.query(UserModel).get(user_id)

            if db_user is None:
                raise NotFoundException("User not found")

            # Update the user attributes
            if user.username:
                db_user.username = user.username
            # if user.email:
            #     db_user.email = user.email
            if user.role and (db_user.role != "user"):
                db_user.role = user.role

            db.commit()
            db.refresh(db_user)
        except SQLAlchemyError:
            raise BadRequestException("Failed to update user")
        except Exception as e:
            raise BadRequestException(f"Failed to update user: {e}")

        return "User updated successfully"

    @staticmethod
    def delete_user_by_id(db: Session, user_id: int) -> str:
        user = db.query(UserModel).get(user_id)
        if user is None:
            raise NotFoundException("User not found")

        db.delete(user)
        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            raise BadRequestException("Failed to delete user")
        except Exception as e:
            raise BadRequestException(f"Failed to delete user: {e}")

        return "User deleted successfully"
