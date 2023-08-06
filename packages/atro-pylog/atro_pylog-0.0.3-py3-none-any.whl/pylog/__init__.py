import os
import logging 
from pylog.logger_base import Logger
from pylog.logger_type import LoggerType, str_to_logger_type
from pylog.loguru_logger import LoguruLogger
from pylog.opentelemetry_logger import OpenTelemetryLogger
from pylog.level import str_to_level
from pylog.settings import OpenTelemetryLoggerSettings, LoguruLoggerSettings


def get_logger(type: LoggerType | str | None = None, level: str | int = logging.DEBUG, open_telemetry_settings: OpenTelemetryLoggerSettings | None = None, loguru_settings: LoguruLoggerSettings | None = None) -> Logger:
    if type is None:
        type = os.getenv("ATRO_PYLOG_TYPE", default=LoggerType.LOGURU)
    if isinstance(type, str):
        type = str_to_logger_type(type)

    if level is None:
        level = os.getenv("ATRO_PYLOG_LEVEL", default=logging.DEBUG)
    elif isinstance(level, str):
        level = str_to_level(level)
        

    match type:
        case LoggerType.LOGURU:
            logger =  LoguruLogger(loguru_settings)
        case LoggerType.OPENTELEMETRY:
            logger = OpenTelemetryLogger(open_telemetry_settings)
        case _:
            raise Exception(f"Unknown logger type: {type}")

    logger.level(level)
    
    return logger
