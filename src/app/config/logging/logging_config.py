import os
import logging.config

if not os.path.exists("log"):
    os.makedirs("log")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
        },
        "simple": {
            "format": "%(asctime)s - %(levelname)s: %(message)s",
        },
        "color_simple": {
            "format": "%(log_color)s%(asctime)s - %(levelname)s: %(message)s",
            "class": "colorlog.ColoredFormatter",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "color_simple",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "log/runtime.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "formatter": "json",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": "log/error.log",
            "level": "ERROR",
            "formatter": "json",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "WARNING",
        },
        "debugger": {
            "handlers": [
                "console",
                "file",
                "error_file",
            ],
            "level": "DEBUG",
        },
    },
}

logging.config.dictConfig(LOGGING)

logger = logging.getLogger("debugger")
