from loguru import logger as loguru_logger
from pylog.settings import BaseLoggerSettings

from pylog.level import level_to_str
from pylog.logger_base import Logger
from pylog.settings import LoguruLoggerSettings


class LoguruLogger(Logger):
    def __init__(self, base_settings: BaseLoggerSettings | None = None, settings: LoguruLoggerSettings | None = None):
        self.settings = settings or LoguruLoggerSettings()
        self.logger = loguru_logger
        super().__init__(base_settings=base_settings)

    def debug(self, message: str) -> None:
        self.logger.debug(message)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def critical(self, message: str) -> None:
        self.logger.critical(message)

    def shutdown(self) -> None:
        pass

    def level(self, level: str | int):
        if isinstance(level, int):
            level = level_to_str(level)
        self.logger.level(level)
