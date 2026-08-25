import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.api.v1.api import api_router
from backend.app.core.config import settings
from backend.app.core.errors import AppException, ErrorCode
from backend.app.core.security import verify_payload_size
from backend.app.core.telemetry import TelemetryMiddleware
from backend.app.providers.base import ProviderErrorCode, ProviderException

logger = logging.getLogger("syris.app")

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 1. Telemetry Middleware (Request IDs & Logging)
app.add_middleware(TelemetryMiddleware)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_payload_middleware(request: Request, call_next):
    # Verify request payload size limit before processing
    await verify_payload_size(request)
    return await call_next(request)


# Global Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            "request_id": request_id,
        },
    )


@app.exception_handler(ProviderException)
async def provider_exception_handler(request: Request, exc: ProviderException):
    request_id = getattr(request.state, "request_id", None)
    status_code = exc.status_code or (
        status.HTTP_400_BAD_REQUEST
        if exc.error_code in (ProviderErrorCode.MODEL_NOT_CERTIFIED, ProviderErrorCode.INVALID_PAYLOAD)
        else status.HTTP_502_BAD_GATEWAY
        if exc.error_code == ProviderErrorCode.MALFORMED_OUTPUT
        else status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": exc.error_code.value,
                "message": exc.message,
                "details": exc.details,
            },
            "request_id": request_id,
        },
    )



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": ErrorCode.INVALID_PAYLOAD,
                "message": "The submitted payload failed schema validation.",
                "details": exc.errors(),
            },
            "request_id": request_id,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    logger.exception(f"Unhandled server error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": ErrorCode.INTERNAL_SERVER_ERROR,
                "message": "An unexpected internal server error occurred. Please try again later.",
                "details": None,
            },
            "request_id": request_id,
        },
    )


# Include API V1 Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": "0.1.0",
        "api_v1_docs": f"{settings.API_V1_STR}/docs",
    }
