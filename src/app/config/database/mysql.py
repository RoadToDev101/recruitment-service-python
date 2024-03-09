from src.app.config.logging.logging_config import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv
import urllib

load_dotenv()


DATASOURCE_USER = os.getenv("MYSQL_USER")
DATASOURCE_PASSWORD = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD"))
DATASOURCE_DB = os.getenv("MYSQL_DATABASE")
DATASOURCE_HOST = os.getenv("MYSQL_HOST", "localhost")
DATASOURCE_PORT = os.getenv("MYSQL_PORT", 3306)

DB_URL = f"mysql+mysqlconnector://{DATASOURCE_USER}:{DATASOURCE_PASSWORD}@{DATASOURCE_HOST}:{DATASOURCE_PORT}/{DATASOURCE_DB}"
try:
    engine = create_engine(
        DB_URL,
        pool_pre_ping=True,
        echo=os.getenv("ENV") == "Development",
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Try to connect to the database
    connection = engine.connect()
    logger.info(f"Connected to MySQL server on port {DATASOURCE_PORT}")
    connection.close()
except Exception as e:
    logger.error("Error connecting to database: ", exc_info=True)
    exit(1)

Base = declarative_base()

from src.app.api.models.user_model import User

Base.metadata.create_all(bind=engine)
