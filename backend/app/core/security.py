import re
from fastapi import Request
from backend.app.core.config import settings
from backend.app.core.errors import AppException, ErrorCode, PayloadTooLargeException

# Safe alphanumeric/hyphen/underscore identifier pattern
ID_PATTERN = re.compile(r"^[a-zA-Z0-9_\-\.]{1,128}$")


def validate_identifier(value: str, field_name: str = "id") -> str:
    """Validates that a string is a safe identifier without injection vectors."""
    if not value or not ID_PATTERN.match(value):
        raise AppException(
            status_code=400,
            code=ErrorCode.INVALID_PAYLOAD,
            message=f"Invalid {field_name} format. Must be 1-128 alphanumeric characters, hyphens, underscores, or dots.",
            details={"field": field_name, "value": value},
        )
    return value


async def verify_payload_size(request: Request) -> None:
    """Ensures request body size does not exceed the maximum configured threshold."""
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.MAX_PAYLOAD_SIZE_BYTES:
        raise PayloadTooLargeException(max_size_bytes=settings.MAX_PAYLOAD_SIZE_BYTES)
