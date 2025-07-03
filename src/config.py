"""Configuration for TODO API"""

from logging.config import dictConfig

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for TODO App"""

    title: str = "Todo API"
    summary: str = "FastAPI Todos"
    host: str = "localhost"
    port: int = 8000
    environment: str = "dev"

    @property
    def is_prod(self) -> bool:
        return self.environment.lower() == "prod"


class LogConfig:
    """Logging config"""

    LOGGER_NAME = "todo_app"
    LOG_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"
    LOG_LEVEL = "INFO"

    def __init__(self):
        self.dict_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": self.LOG_FORMAT,
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stderr",
                },
            },
            "loggers": {
                self.LOGGER_NAME: {
                    "handlers": ["default"],
                    "level": self.LOG_LEVEL,
                    "propagate": False,
                },
            },
        }

    def configure(self):
        dictConfig(self.dict_config)
