""" app entrypoint """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import get_settings
from app.internal.interfaces.api.user_handler import router as user_router
from app.internal.infrastructure.database.connection import populate

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    """ populate database on startup"""
    populate()


@app.get("/", tags=["health"])
def health():
    """ health check """
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }

