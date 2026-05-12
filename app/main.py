from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import Base, engine
from app.modules.parking.routes import router as parking_router
from app.modules.vehicle.routes import router as vehicle_router
from app.shared.exceptions.base import AppError
from app.shared.responses.base import error_response


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, debug=settings.app_debug)

    @app.on_event("startup")
    def on_startup() -> None:
        Base.metadata.create_all(bind=engine)

    @app.exception_handler(AppError)
    async def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=error_response(exc.message, exc.code))

    app.include_router(parking_router, prefix=settings.api_prefix)
    app.include_router(vehicle_router, prefix=settings.api_prefix)

    return app


app = create_app()
