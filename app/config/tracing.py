""" tracing configuration """
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from app.config.config import get_settings
from app.config.logging import get_logger

logger = get_logger("tracing")
settings = get_settings()


def setup_tracing():
    """Configure basic tracing with console exporter"""
    
    resource = Resource.create({
        "service.name": settings.app_name,
        "service.version": settings.app_version,
    })
    
    provider = TracerProvider(resource=resource)
    
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    
    trace.set_tracer_provider(provider)
    
    logger.info("Tracing configured with console exporter")


def instrument_app(app):
    """Instrument FastAPI application"""
    FastAPIInstrumentor.instrument_app(app)
    logger.info("FastAPI instrumented for tracing")


def instrument_db(engine):
    """Instrument SQLAlchemy engine"""
    SQLAlchemyInstrumentor().instrument(engine=engine)
    logger.info("SQLAlchemy instrumented for tracing")
