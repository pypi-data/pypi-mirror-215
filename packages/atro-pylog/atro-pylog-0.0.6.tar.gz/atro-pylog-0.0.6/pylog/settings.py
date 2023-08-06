from pydantic import BaseSettings
import logging

from pylog.logger_type import LoggerType


class BaseLoggerSettings(BaseSettings):
    name: str = "pylog"
    type: LoggerType  = LoggerType.RICH
    level: int | str  = logging.DEBUG
    msg_format: str = "%(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    
    class Config:
        env_prefix = "ATRO_PYLOG_"
        env_file = ".env"
        env_file_encoding = "utf-8"


class OpenTelemetryLoggerSettings(BaseSettings):
    service_name: str = "pylog"
    instance_id: str = "pylog"
    endpoint: str | None = None

    class Config:
        env_prefix = "ATRO_PYLOG_"
        env_file = ".env"
        env_file_encoding = "utf-8"