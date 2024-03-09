from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from src.app.common.custom_exception import CredentialsException

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")  # Import from environment variables for production
ALGORITHM = "HS256"


class TokenCreationError(Exception):
    pass


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        # Set expiration time for token
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)

        # Ensure the 'sub' claim is a string
        data["sub"] = str(data["sub"])

        data.update({"exp": expire})  # Add expiration time to token

        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)  # Create token
        return encoded_jwt
    except:
        raise CredentialsException("Failed to create token")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise CredentialsException("Token has expired")
    except jwt.JWTError:
        raise CredentialsException("Invalid token")
    except Exception as e:
        raise CredentialsException(f"Error decoding token. Error: {e}")
