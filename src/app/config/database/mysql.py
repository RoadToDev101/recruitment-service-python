from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config.database.base import Base
import os
from dotenv import load_dotenv
import urllib
from src.app.config.logging.logging_config import logger

load_dotenv()


class MySQL:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQL, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        DATASOURCE_USER = os.getenv("MYSQL_USER")
        DATASOURCE_PASSWORD = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD"))
        DATASOURCE_DB = os.getenv("MYSQL_DATABASE")
        DATASOURCE_HOST = os.getenv("MYSQL_HOST", "localhost")
        DATASOURCE_PORT = os.getenv("MYSQL_PORT", 3306)
        DB_URL = f"mysql+mysqlconnector://{DATASOURCE_USER}:{DATASOURCE_PASSWORD}@{DATASOURCE_HOST}:{DATASOURCE_PORT}/{DATASOURCE_DB}"

        try:
            self.engine = create_engine(
                DB_URL,
                pool_pre_ping=True,
                echo=os.getenv("ENV") == "Development",
            )
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            # Try to connect to the database
            connection = self.engine.connect()
            logger.info(f"Connected to MySQL server on port {DATASOURCE_PORT}")
            connection.close()
        except Exception as e:
            logger.error("Error connecting to database: ", exc_info=True)
            exit(1)

        from src.app.api.models.user_model import User

        Base.metadata.create_all(bind=self.engine)


# Usage
db = MySQL()
