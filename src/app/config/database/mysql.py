import os
import urllib
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config.database.base_mysql import Base
from src.app.config.logging.logging_config import logger

load_dotenv()


class MySQLConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        host = os.getenv("MYSQL_HOST", "localhost")
        user = os.getenv("MYSQL_USER")
        password = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD"))
        db_name = os.getenv("MYSQL_DATABASE")
        port = os.getenv("MYSQL_PORT", 3306)
        DB_URL = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{db_name}"

        try:
            self.engine = create_engine(
                url=DB_URL,
                pool_pre_ping=True,
                echo=os.getenv("ENV") == "Development",
            )
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            # Try to connect to the database
            connection = self.engine.connect()
            logger.info(f"Connected to MySQL server at {host} on port {port}")
            connection.close()
        except Exception:
            logger.error("Error connecting to MySQL server: ", exc_info=True)
            exit(1)

        from src.app.api.models.user_model import User

        Base.metadata.create_all(bind=self.engine)


# Usage
db = MySQLConnection()
