"""Configuration for TODO API"""

from pydantic import BaseModel
from pydantic_settings import BaseSettings

from models import Tags


class Settings(BaseSettings):
    """Settings for TODO App"""

    app_title: str = "Todo API"
    app_summary: str = "A sample FastAPI for Todos"
    host: str = "localhost"
    port: int = 8000
    deploy_environment: str = "prod"

    if deploy_environment == "prod":
        IS_PROD: bool = True
    else:
        IS_PROD: bool = False


class LogConfig(BaseModel):
    """Logging config"""

    LOGGER_NAME: str = Tags.APP_NAME.value
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }
