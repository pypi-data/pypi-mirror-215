import logging
from rich.logging import RichHandler
from pylog.level import level_to_str
from pylog.settings import BaseLoggerSettings

def rich_logger_setup(base_settings: BaseLoggerSettings):
  logging.basicConfig(
      level=level_to_str(base_settings.level),
      format=base_settings.msg_format,
      datefmt=base_settings.date_format,
      handlers=[RichHandler(rich_tracebacks=True)]
  )
