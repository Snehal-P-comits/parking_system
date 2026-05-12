"""FastAPI application composition root.

This module wires the app instance, startup lifecycle, exception mapping,
and route registration in one place.
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.modules.parking.routes import router as parking_router
from app.modules.vehicle.routes import router as vehicle_router
from app.shared.exceptions.base import AppError
from app.shared.responses.base import error_response


def create_app() -> FastAPI:
    # Initialize the FastAPI app with env-driven metadata.
    app = FastAPI(title=settings.app_name, debug=settings.app_debug)

    @app.on_event("startup")
    def on_startup() -> None:
        # For this project stage, create tables automatically at startup.
        # In production migrations, this is typically replaced by Alembic.
        Base.metadata.create_all(bind=engine)

    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        # Convert domain/application exceptions into a stable API error envelope.
        return JSONResponse(status_code=exc.status_code, content=error_response(exc.message, exc.code))

    # Register module routers under a common API prefix.
    app.include_router(parking_router, prefix=settings.api_prefix)
    app.include_router(vehicle_router, prefix=settings.api_prefix)

    return app


app = create_app()
