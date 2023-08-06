import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

from pylog.level import level_to_str
from pylog.settings import BaseLoggerSettings, OpenTelemetryLoggerSettings


def open_telemetry_logger_setup(base_settings: BaseLoggerSettings, settings: OpenTelemetryLoggerSettings):
    trace.set_tracer_provider(TracerProvider())
    logger_provider = LoggerProvider(
        resource=Resource.create(
            {
                "service.name": settings.service_name,
                "service.instance.id": settings.instance_id,
            },
        ),
    )
    set_logger_provider(logger_provider)
    exporter = OTLPLogExporter(insecure=True, endpoint=settings.endpoint)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.basicConfig(level=level_to_str(base_settings.level), format=base_settings.msg_format, datefmt=base_settings.date_format, handlers=[handler])
