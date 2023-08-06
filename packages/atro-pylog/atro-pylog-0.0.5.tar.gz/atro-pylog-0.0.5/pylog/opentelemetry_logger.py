import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from pydantic import BaseSettings

from pylog.level import str_to_level
from pylog.logger_base import Logger
from pylog.settings import BaseLoggerSettings, OpenTelemetryLoggerSettings


class OpenTelemetryLogger(Logger):
    def __init__(self, base_settings:BaseLoggerSettings | None = None ,settings: OpenTelemetryLoggerSettings | None = None):
        self.settings = settings or OpenTelemetryLoggerSettings()
        trace.set_tracer_provider(TracerProvider())
        self.logger_provider = LoggerProvider(
            resource=Resource.create(
                {
                    "service.name": self.settings.service_name or "",
                    "service.instance.id": self.settings.instance_id or "",
                },
            ),
        )
        set_logger_provider(self.logger_provider)

        self.exporter = OTLPLogExporter(insecure=True, endpoint=self.settings.endpoint)
        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(self.exporter))
        self.handler = LoggingHandler(level=logging.NOTSET, logger_provider=self.logger_provider)

        # Attach OTLP handler to root logger
        logging.getLogger().addHandler(self.handler)
        self.logger = logging.getLogger(__name__)
        super().__init__(base_settings=base_settings)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)

    def shutdown(self):
        self.logger_provider.shutdown()

    def level(self, level: str | int):
        if isinstance(level, str):
            level = str_to_level(level)
        self.logger.setLevel(level)
