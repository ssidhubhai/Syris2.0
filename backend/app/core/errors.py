from typing import Any, Optional
from fastapi import HTTPException, status


class ErrorCode:
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    INVALID_SESSION = "INVALID_SESSION"
    INVALID_PAYLOAD = "INVALID_PAYLOAD"
    INVALID_EXPLANATION_DOCUMENT = "INVALID_EXPLANATION_DOCUMENT"
    IDEMPOTENCY_CONFLICT = "IDEMPOTENCY_CONFLICT"
    DUPLICATE_REQUEST = "DUPLICATE_REQUEST"
    PAYLOAD_TOO_LARGE = "PAYLOAD_TOO_LARGE"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Any] = None,
    ):
        self.code = code
        self.message = message
        self.details = details
        super().__init__(status_code=status_code, detail=message)


class SessionNotFoundException(AppException):
    def __init__(self, session_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code=ErrorCode.SESSION_NOT_FOUND,
            message=f"Session '{session_id}' was not found.",
            details={"session_id": session_id},
        )


class InvalidExplanationDocumentException(AppException):
    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code=ErrorCode.INVALID_EXPLANATION_DOCUMENT,
            message=message,
            details=details,
        )


class IdempotencyConflictException(AppException):
    def __init__(self, key: str, message: str = "Idempotency key was reused with a different request payload."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code=ErrorCode.IDEMPOTENCY_CONFLICT,
            message=message,
            details={"idempotency_key": key},
        )


class PayloadTooLargeException(AppException):
    def __init__(self, max_size_bytes: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            code=ErrorCode.PAYLOAD_TOO_LARGE,
            message=f"Request payload exceeds maximum allowed limit of {max_size_bytes} bytes.",
            details={"max_size_bytes": max_size_bytes},
        )
