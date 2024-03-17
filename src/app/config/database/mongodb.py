import os
import urllib
from pymongo import MongoClient
from dotenv import load_dotenv
from src.app.config.logging.logging_config import logger

load_dotenv()


class MongoDBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        host = os.getenv("MONGODB_HOST", "localhost")
        port = int(os.getenv("MONGODB_PORT", "27017"))
        username = os.getenv("MONGODB_USERNAME", "")
        password = urllib.parse.quote_plus(os.getenv("MONGODB_PASSWORD", ""))
        db_name = os.getenv("MONGODB_DATABASE", "test")
        auth_source = os.getenv("MONGODB_AUTH_SOURCE", "admin")

        try:
            # Create a URI string for MongoClient.
            if username and password:
                uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_source}"
            else:
                uri = f"mongodb://{host}:{port}/{db_name}"

            self._client = MongoClient(uri)
            self._db = self._client[db_name]
            logger.info(f"Connected to MongoDB at {host} on port {port}")
        except Exception:
            logger.error("Error connecting to MongoDB: ", exc_info=True)
            exit(1)

    @property
    def db(self):
        return self._db


# Usage
mongo_connection = MongoDBConnection()
mongo_db = mongo_connection.db
