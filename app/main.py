""" app entrypoint """
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import get_settings
from app.config.logging import setup_logging, get_logger
from app.config.tracing import setup_tracing, instrument_app, instrument_db
from app.internal.interfaces.api.user_handler import router as user_router
from app.internal.infrastructure.database.connection import engine

setup_logging()
setup_tracing()
logger = get_logger("main")

settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    try:
        instrument_db(engine)
        logger.info("Application startup completed")
    except Exception as e:
        logger.error(f"Application startup failed: {str(e)}")
        raise
    
    yield
    
    logger.info("Application shutdown")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


@app.get("/", tags=["health"])
def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }

