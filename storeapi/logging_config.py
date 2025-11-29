from logging.config import dictConfig
from storeapi.config import DevConfig, config
import logging
# from storeapi.logtail_handler import BetterStackHandler


def obfuscated(email: str, obfuscated_length: int) -> str:
    chars = email[:obfuscated_length]
    first, last = email.split("@")
    return chars + "*" * (len(first) - obfuscated_length) + last


class EmailObfuscationFilter(logging.Filter):
    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 2 if isinstance(config, DevConfig) else 0,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.json.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(correlation_id)s %(asctime)s %(msecs)s %(levelname)s %(name)s %(lineno)d %(message)s",
                    # "json_format": [
                    #     "correlation_id",
                    #     "asctime",
                    #     "msecs",
                    #     "levelname",
                    #     "name",
                    #     "lineno",
                    #     "message",
                    # ],
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "formatter": "file",
                    "filename": "storeapi.log",
                    "maxBytes": 2024 * 2024 * 2024,  # 1GB
                    "backupCount": 5,
                    "encoding": "utf8",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_abfuscation"],
                    "source_token": config.LOGTAIL_SOURCE_TOKEN,
                },
            },
            "loggers": {
                "": {"handlers": ["rotating_file"], "level": "INFO", "propagate": True},
                "uvicorn": {"handlers": ["default", "rotating_file"], "level": "INFO"},
                "databases": {"handlers": ["default"], "level": "WARNING"},
                "aiosqlite": {"handlers": ["default"], "level": "CRITICAL"},
                "storeapi": {
                    "handlers": ["default", "rotating_file"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,
                },
            },
        }
    )

    # LOGTAIL_ENDPOINT = "https://s1610174.eu-nbg-2.betterstackdata.com/v1/logs"
    # LOGTAIL_TOKEN = (
    #     "qpz5esoELmagLzkXcHtyTDCe"  # keep secret in env vars in real deployment!
    # )
    # service_name = "storeapi"  # use same SERVICE_NAME you set in OTel if any

    # bs_handler = BetterStackHandler(
    #     endpoint=LOGTAIL_ENDPOINT,
    #     source_token=LOGTAIL_TOKEN,
    #     service_name=service_name,
    # )
    # # Optionally set the formatter (uses jsonformatter internally)
    # bs_handler.setFormatter(logging.Formatter("%(message)s"))
    # # Add filter instances identical to rotated_file/default if you want
    # # For example, to use your existing filters, get them from loggers or create new ones
    # logging.getLogger().addHandler(bs_handler)
