import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.as_posix())
from pylog.rich_setup import rich_logger_setup
from pylog.settings import BaseLoggerSettings, OpenTelemetryLoggerSettings
from pylog.logger_type import LoggerType, str_to_logger_type
import logging
from pylog.opentelemetry_setup import open_telemetry_logger_setup


def get_logger(
    base_settings: BaseLoggerSettings = BaseLoggerSettings(), 
    open_telemetry_settings: OpenTelemetryLoggerSettings = OpenTelemetryLoggerSettings()
    ):
    logger = logging.getLogger(base_settings.name)
    
    match base_settings.type:
        case LoggerType.RICH:
            rich_logger_setup(base_settings)
        case LoggerType.OPENTELEMETRY:
            pass
            open_telemetry_logger_setup(base_settings, open_telemetry_settings)
        case _:
            raise Exception(f"Unknown logger type: {type}")

    return logger