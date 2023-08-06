import logging
import sys
import traceback
from abc import ABC, abstractmethod
from pylog.level import level_to_str, str_to_level

from pylog.settings import BaseLoggerSettings


class Logger(ABC):
    def __init__(self, base_settings: BaseLoggerSettings | None):
        sys.excepthook = self.exception_handler
        base_settings = base_settings or BaseLoggerSettings()
        
        level: str | int = base_settings.level or logging.DEBUG
        self.level(level_to_str(level) if isinstance(level, int) else level)

    @abstractmethod
    def debug(self, message: str):
        pass

    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def warning(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def critical(self, message: str):
        pass

    @abstractmethod
    def shutdown(self):
        pass

    @abstractmethod
    def level(self, level: str):
        pass

    def exception_handler(self, exc_type, exc_value, exc_traceback):
        self.critical(f"Exception: \n {str(exc_value)} \n {''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))}")
