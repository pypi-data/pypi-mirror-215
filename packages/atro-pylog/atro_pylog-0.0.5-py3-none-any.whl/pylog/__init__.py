import logging
import os

from pylog.level import str_to_level
from pylog.logger_base import Logger
from pylog.logger_type import LoggerType, str_to_logger_type
from pylog.loguru_logger import LoguruLogger
from pylog.opentelemetry_logger import OpenTelemetryLogger
from pylog.settings import BaseLoggerSettings, LoguruLoggerSettings, OpenTelemetryLoggerSettings


def get_logger(base_settings: BaseLoggerSettings | None = None, open_telemetry_settings: OpenTelemetryLoggerSettings | None = None, loguru_settings: LoguruLoggerSettings | None = None) -> Logger:
    base_settings = base_settings or BaseLoggerSettings()
    base_settings.type = base_settings.type or LoggerType.LOGURU
    if isinstance(base_settings.type, str):
        base_settings.type = str_to_logger_type(base_settings.type)

    match base_settings.type:
        case LoggerType.LOGURU:
            return LoguruLogger(base_settings, loguru_settings) 
        case LoggerType.OPENTELEMETRY:
            return OpenTelemetryLogger(base_settings, open_telemetry_settings) 
        case _:
            raise Exception(f"Unknown logger type: {type}")

    return logger
