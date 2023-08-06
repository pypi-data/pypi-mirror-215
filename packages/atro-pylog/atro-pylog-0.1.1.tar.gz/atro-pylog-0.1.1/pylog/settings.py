import logging

from pydantic import BaseSettings
from pathlib import Path

class BaseLoggerSettings(BaseSettings):
    name: str = "pylog"
    type: str = "rich"
    level: int | str = logging.DEBUG
    msg_format: str = "%(message)s"
    date_format: str = "%X"

    class Config:
        env_prefix = "ATRO_PYLOG_"
        env_file = (Path.home() / ".config" / "atro" / "pylog.env").as_posix(), ".env"
        env_file_encoding = "utf-8"


class OpenTelemetryLoggerSettings(BaseSettings):
    service_name: str = "pylog"
    instance_id: str = "pylog"
    endpoint: str | None = None

    class Config:
        env_prefix = "ATRO_PYLOG_"
        env_file = (Path.home() / ".config" / "atro" / "pylog.env").as_posix(), ".env", 
        env_file_encoding = "utf-8"
