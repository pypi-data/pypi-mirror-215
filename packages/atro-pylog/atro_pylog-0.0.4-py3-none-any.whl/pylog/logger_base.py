import sys
import traceback
from abc import ABC, abstractmethod


class Logger(ABC):
    def __init__(self):
        sys.excepthook = self.exception_handler

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
