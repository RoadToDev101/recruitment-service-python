import logging
import logging.config
from pythonjsonlogger import jsonlogger

LOGGING = {
    "version": 1,  # Specify the version of the logging configuration
    "disable_existing_loggers": False,  # Keep existing loggers active
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        "simple": {
            "format": "%(asctime)s - %(levelname)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",  # Use a rotating file handler that creates a new log file at midnight
            "filename": "log/application.log",  # Specify the file name and path for the log file
            "when": "midnight",  # Rotate the log file at midnight
            "interval": 1,  # Rotate the log file every day
            "backupCount": 7,  # Keep up to 7 backup log files
            "formatter": "json",  # Use the "json" formatter defined above
        },
        "error_file": {
            "class": "logging.FileHandler",  # Use a file handler for error logs
            "filename": "log/error.log",  # Specify the file name and path for the error log file
            "level": "ERROR",  # Only log messages with ERROR level or higher
            "formatter": "json",  # Use the "json" formatter defined above
        },
    },
    "loggers": {
        "": {  # Root logger configuration
            "handlers": ["file"],  # Use the "file" handler for the root logger
            "level": "WARNING",  # Only log messages with WARNING level or higher
        },
        "controller": {  # Logger configuration for the "controller" module
            "handlers": [
                "console",
                "file",
                "error_file",
            ],  # Use "console", "file" and "error_file" handlers for the "controller" logger
            "level": "DEBUG",  # Log messages with DEBUG level or higher
        },
    },
}

logging.config.dictConfig(LOGGING)

g_logger = logging.getLogger("uvicorn")
c_logger = logging.getLogger("controller")
