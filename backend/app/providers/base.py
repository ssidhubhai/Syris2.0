from abc import ABC, abstractmethod
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, ConfigDict, Field


# ============================================================================
# 1. Normalized Error Hierarchy
# ============================================================================

class ProviderErrorCode(str, Enum):
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"       # HTTP 503 / network transient
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"         # HTTP 429 / quota
    INVALID_PAYLOAD = "INVALID_PAYLOAD"                 # HTTP 400 / bad client request
    AUTH_FAILURE = "AUTH_FAILURE"                       # HTTP 401 / 403
    MODEL_NOT_FOUND = "MODEL_NOT_FOUND"                 # HTTP 404
    MODEL_NOT_CERTIFIED = "MODEL_NOT_CERTIFIED"         # Registry certification failure
    MALFORMED_OUTPUT = "MALFORMED_OUTPUT"               # Schema parsing failure
    TIMEOUT = "TIMEOUT"                                 # Gateway timeout
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class ProviderException(Exception):
    """Base class for all provider-neutral errors."""
    def __init__(
        self,
        message: str,
        provider: str = "unknown",
        error_code: ProviderErrorCode = ProviderErrorCode.UNKNOWN_ERROR,
        status_code: Optional[int] = None,
        is_transient: bool = False,
        model_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.provider = provider
        self.error_code = error_code
        self.status_code = status_code
        self.is_transient = is_transient
        self.model_id = model_id
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "error_code": self.error_code.value,
            "status_code": self.status_code,
            "is_transient": self.is_transient,
            "model_id": self.model_id,
            "message": self.message,
            "details": self.details,
        }


class ProviderUnavailableException(ProviderException):
    """HTTP 503 / service outage / connectivity issues (Transient)."""
    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int = 503,
        model_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            provider=provider,
            error_code=ProviderErrorCode.PROVIDER_UNAVAILABLE,
            status_code=status_code,
            is_transient=True,
            model_id=model_id,
            details=details,
        )


class ProviderRateLimitException(ProviderException):
    """HTTP 429 / quota limit exceeded (Transient / Quota)."""
    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int = 429,
        model_id: Optional[str] = None,
        retry_after_seconds: Optional[float] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        all_details = details or {}
        if retry_after_seconds is not None:
            all_details["retry_after_seconds"] = retry_after_seconds
        super().__init__(
            message=message,
            provider=provider,
            error_code=ProviderErrorCode.RATE_LIMIT_EXCEEDED,
            status_code=status_code,
            is_transient=True,
            model_id=model_id,
            details=all_details,
        )


class ProviderInvalidPayloadException(ProviderException):
    """HTTP 400 / invalid arguments / malformed request (Permanent client error)."""
    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int = 400,
        model_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            provider=provider,
            error_code=ProviderErrorCode.INVALID_PAYLOAD,
            status_code=status_code,
            is_transient=False,
            model_id=model_id,
            details=details,
        )


class ProviderAuthenticationException(ProviderException):
    """HTTP 401/403 / invalid or missing API key / forbidden (Permanent auth error)."""
    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int = 401,
        model_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            provider=provider,
            error_code=ProviderErrorCode.AUTH_FAILURE,
            status_code=status_code,
            is_transient=False,
            model_id=model_id,
            details=details,
        )


class ProviderModelNotFoundException(ProviderException):
    """HTTP 404 / deprecated or non-existent model ID (Permanent model error)."""
    def __init__(
        self,
        message: str,
        provider: str,
        status_code: int = 404,
        model_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            message=message,
            provider=provider,
            error_code=ProviderErrorCode.MODEL_NOT_FOUND,
            status_code=status_code,
            is_transient=False,
            model_id=model_id,
            details=details,
        )


class ProviderMalformedOutputException(ProviderException):
    """Model generated output that does not match expected JSON or Pydantic schema."""
    def __init__(
        self,
        message: str,
        provider: str,
        model_id: Optional[str] = None,
        raw_output: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        all_details = details or {}
        if raw_output is not None:
            # Truncate raw output safely to avoid log bloat
            all_details["raw_output_snippet"] = raw_output[:500]
        super().__init__(
            message=message,
            provider=provider,
            error_code=ProviderErrorCode.MALFORMED_OUTPUT,
            status_code=None,
            is_transient=False,
            model_id=model_id,
            details=all_details,
        )


class ModelNotCertifiedException(ProviderException):
    """Attempted to use a model that has not passed certification."""
    def __init__(
        self,
        model_id: str,
        provider: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        msg = message or f"Model '{model_id}' is not certified for use in provider '{provider}'."
        super().__init__(
            message=msg,
            provider=provider,
            error_code=ProviderErrorCode.MODEL_NOT_CERTIFIED,
            status_code=None,
            is_transient=False,
            model_id=model_id,
            details=details,
        )


# ============================================================================
# 2. Content & Image Models
# ============================================================================

SUPPORTED_IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/heic",
    "image/heif",
}


class ImageContent(BaseModel):
    """Provider-neutral container for multimodal image data."""
    data: bytes
    mime_type: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def validate_content(self) -> None:
        if not self.data or len(self.data) == 0:
            raise ProviderInvalidPayloadException(
                message="Image content data cannot be empty.",
                provider="neutral",
            )
        if self.mime_type.lower() not in SUPPORTED_IMAGE_MIME_TYPES:
            raise ProviderInvalidPayloadException(
                message=f"Unsupported image MIME type: '{self.mime_type}'. Supported: {sorted(SUPPORTED_IMAGE_MIME_TYPES)}",
                provider="neutral",
            )


class ProviderMessage(BaseModel):
    """Provider-neutral conversation message."""
    role: str  # "user", "assistant", "system"
    content: str
    images: Optional[List[ImageContent]] = None


# ============================================================================
# 3. Token Telemetry & Requests
# ============================================================================

class ProviderTokenUsage(BaseModel):
    """Normalized token accounting."""
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cached_tokens: Optional[int] = None


class ProviderTextRequest(BaseModel):
    """Provider-neutral text / multimodal generation request."""
    request_id: str
    model_id: str
    prompt: Optional[str] = None
    messages: Optional[List[ProviderMessage]] = None
    system_instruction: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    images: Optional[List[ImageContent]] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ProviderStructuredRequest(BaseModel):
    """Provider-neutral structured JSON generation request."""
    request_id: str
    model_id: str
    prompt: Optional[str] = None
    messages: Optional[List[ProviderMessage]] = None
    system_instruction: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    images: Optional[List[ImageContent]] = None
    response_schema: Type[BaseModel]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ProviderResponse(BaseModel):
    """Provider-neutral standardized AI response."""
    request_id: str
    provider: str
    model_id: str
    text: Optional[str] = None
    structured_output: Optional[Any] = None
    token_usage: ProviderTokenUsage = Field(default_factory=ProviderTokenUsage)
    latency_ms: int = 0
    finish_reason: Optional[str] = None
    raw_metadata: Optional[Dict[str, Any]] = None


class ModelMetadata(BaseModel):
    """Provider-neutral metadata describing a model's capabilities and certification status."""
    provider: str
    model_id: str
    api_version: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    input_token_limit: Optional[int] = None
    output_token_limit: Optional[int] = None
    supported_modalities: List[str] = Field(default_factory=lambda: ["text"])
    supports_structured_output: bool = False
    supports_tools: bool = False
    supports_streaming: bool = False
    lifecycle_status: str = "active"             # "active", "preview", "deprecated"
    availability_status: str = "available"       # "available", "restricted", "unavailable"
    certification_status: str = "UNCERTIFIED"    # "CERTIFIED_FOR_DEV", "CERTIFIED_FOR_PROD", "UNCERTIFIED"
    benchmark_status: Optional[str] = None       # "passed_dev_smoke", "pending", etc.
    last_verified_at: Optional[datetime] = None


class ProviderHealthResult(BaseModel):
    """Provider health check status."""
    provider: str
    is_healthy: bool
    latency_ms: int
    details: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None


# ============================================================================
# 4. Abstract Provider Interface
# ============================================================================

class BaseModelProvider(ABC):
    """Abstract base class for all AI model provider adapters."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name identifier for this provider (e.g., 'google', 'mistral')."""
        pass

    @abstractmethod
    async def generate_text(self, request: ProviderTextRequest) -> ProviderResponse:
        """Executes plain text or multimodal generation."""
        pass

    @abstractmethod
    async def generate_structured(self, request: ProviderStructuredRequest) -> ProviderResponse:
        """Executes structured generation parsed into the requested Pydantic schema."""
        pass

    @abstractmethod
    async def list_models(self) -> List[ModelMetadata]:
        """Lists available models from live metadata or approved registry."""
        pass

    @abstractmethod
    async def get_model(self, model_id: str) -> ModelMetadata:
        """Retrieves normalized metadata for a specific model."""
        pass

    @abstractmethod
    async def health_check(self) -> ProviderHealthResult:
        """Performs a lightweight connectivity and credential validation."""
        pass
