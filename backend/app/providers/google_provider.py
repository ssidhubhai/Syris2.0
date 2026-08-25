import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, ValidationError

# Google GenAI official SDK
from google import genai
from google.genai import errors as genai_errors
from google.genai import types as genai_types

from backend.app.providers.base import (
    BaseModelProvider,
    ImageContent,
    ModelMetadata,
    ModelNotCertifiedException,
    ProviderAuthenticationException,
    ProviderErrorCode,
    ProviderException,
    ProviderHealthResult,
    ProviderInvalidPayloadException,
    ProviderMalformedOutputException,
    ProviderMessage,
    ProviderModelNotFoundException,
    ProviderRateLimitException,
    ProviderResponse,
    ProviderStructuredRequest,
    ProviderTextRequest,
    ProviderTokenUsage,
    ProviderUnavailableException,
    SUPPORTED_IMAGE_MIME_TYPES,
)
from backend.app.providers.registry import ModelRegistry, default_registry

logger = logging.getLogger("syris.providers.google")


class GoogleProvider(BaseModelProvider):
    """
    Google GenAI provider adapter.
    Encapsulates all Google GenAI SDK specifics (client, types, errors).
    Google SDK types NEVER escape this module.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        registry: Optional[ModelRegistry] = None,
        client: Optional[genai.Client] = None,
    ):
        self._registry = registry or default_registry
        self._api_key = api_key
        self._client = client

    @property
    def client(self) -> genai.Client:
        """Lazily initialize Google GenAI client if not already initialized."""
        if self._client is not None:
            return self._client
        
        resolved_key = (
            self._api_key
            or os.environ.get("GEMINI_API_KEY")
            or os.environ.get("GOOGLE_API_KEY")
        )
        if not resolved_key:
            raise ProviderAuthenticationException(
                message="GEMINI_API_KEY environment variable is not configured.",
                provider=self.provider_name,
                status_code=401,
            )
        self._client = genai.Client(api_key=resolved_key)
        return self._client

    @property
    def provider_name(self) -> str:
        return "google"


    # =========================================================================
    # Error Normalization
    # =========================================================================

    def _normalize_error(
        self,
        exc: Exception,
        model_id: Optional[str] = None,
    ) -> ProviderException:
        """
        Maps provider-specific exceptions to normalized ProviderException hierarchy.
        503 -> ProviderUnavailableException (transient)
        429 -> ProviderRateLimitException (transient)
        400 -> ProviderInvalidPayloadException (permanent)
        401 / 403 -> ProviderAuthenticationException (permanent)
        404 -> ProviderModelNotFoundException (permanent)
        """
        if isinstance(exc, ProviderException):
            return exc

        msg = str(exc)
        code: Optional[int] = None
        details: Dict[str, Any] = {"raw_exception_type": type(exc).__name__}

        if isinstance(exc, genai_errors.APIError):
            code = exc.code
            msg = exc.message or msg
            details["api_code"] = exc.code
            details["api_message"] = exc.message

        if code == 503:
            return ProviderUnavailableException(
                message=f"Google Gemini service unavailable (503): {msg}",
                provider=self.provider_name,
                status_code=503,
                model_id=model_id,
                details=details,
            )
        elif code == 429:
            return ProviderRateLimitException(
                message=f"Google Gemini quota/rate limit exceeded (429): {msg}",
                provider=self.provider_name,
                status_code=429,
                model_id=model_id,
                details=details,
            )
        elif code == 400:
            return ProviderInvalidPayloadException(
                message=f"Invalid payload for Google Gemini (400): {msg}",
                provider=self.provider_name,
                status_code=400,
                model_id=model_id,
                details=details,
            )
        elif code in (401, 403):
            return ProviderAuthenticationException(
                message=f"Google Gemini authentication/permission error ({code}): {msg}",
                provider=self.provider_name,
                status_code=code,
                model_id=model_id,
                details=details,
            )
        elif code == 404:
            return ProviderModelNotFoundException(
                message=f"Google Gemini model not found ({code}): {msg}",
                provider=self.provider_name,
                status_code=404,
                model_id=model_id,
                details=details,
            )

        # Check for transient connection errors or timeouts
        err_type_lower = type(exc).__name__.lower()
        if "timeout" in err_type_lower or "connect" in err_type_lower or "unavailable" in msg.lower():
            return ProviderUnavailableException(
                message=f"Google Gemini connectivity error: {msg}",
                provider=self.provider_name,
                status_code=code or 503,
                model_id=model_id,
                details=details,
            )

        return ProviderException(
            message=f"Google Gemini error: {msg}",
            provider=self.provider_name,
            error_code=ProviderErrorCode.UNKNOWN_ERROR,
            status_code=code,
            is_transient=False,
            model_id=model_id,
            details=details,
        )

    # =========================================================================
    # Request Building & Content Mapping
    # =========================================================================

    def _build_contents_payload(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[ProviderMessage]] = None,
        images: Optional[List[ImageContent]] = None,
    ) -> List[Any]:
        """
        Converts provider-neutral prompt, messages, and images into Google SDK contents.
        Validates image data and MIME types strictly.
        """
        contents: List[Any] = []

        # 1. Process standalone images
        if images:
            for idx, img in enumerate(images):
                img.validate_content()
                part = genai_types.Part.from_bytes(
                    data=img.data,
                    mime_type=img.mime_type,
                )
                contents.append(part)

        # 2. Process standalone prompt
        if prompt:
            contents.append(prompt)

        # 3. Process structured conversation messages if present
        if messages:
            for msg in messages:
                msg_parts: List[Any] = []
                if msg.images:
                    for img in msg.images:
                        img.validate_content()
                        msg_parts.append(
                            genai_types.Part.from_bytes(
                                data=img.data,
                                mime_type=img.mime_type,
                            )
                        )
                if msg.content:
                    msg_parts.append(msg.content)

                if len(msg_parts) == 1:
                    contents.append(msg_parts[0])
                elif len(msg_parts) > 1:
                    contents.extend(msg_parts)

        if not contents:
            raise ProviderInvalidPayloadException(
                message="Generation request must contain at least a prompt, messages, or image content.",
                provider=self.provider_name,
            )

        return contents

    def _normalize_token_usage(self, usage_metadata: Any) -> ProviderTokenUsage:
        """
        Safely extracts token usage from Google SDK response.
        Never fabricates tokens; defaults missing fields to null/zero.
        """
        if not usage_metadata:
            return ProviderTokenUsage()

        return ProviderTokenUsage(
            input_tokens=getattr(usage_metadata, "prompt_token_count", 0) or 0,
            output_tokens=getattr(usage_metadata, "candidates_token_count", 0) or 0,
            total_tokens=getattr(usage_metadata, "total_token_count", 0) or 0,
            cached_tokens=getattr(usage_metadata, "cached_content_token_count", None),
        )

    # =========================================================================
    # Generation Methods
    # =========================================================================

    async def generate_text(self, request: ProviderTextRequest) -> ProviderResponse:
        """
        Executes text or multimodal generation with a certified Gemini model.
        Fails closed if the model is uncertified.
        """
        # 1. Validate certification against registry
        self._registry.validate_eligibility(request.model_id, provider=self.provider_name)

        # 2. Build SDK contents
        contents = self._build_contents_payload(
            prompt=request.prompt,
            messages=request.messages,
            images=request.images,
        )

        # 3. Build SDK config
        config_kwargs: Dict[str, Any] = {}
        if request.temperature is not None:
            config_kwargs["temperature"] = request.temperature
        if request.max_tokens is not None:
            config_kwargs["max_output_tokens"] = request.max_tokens
        if request.system_instruction:
            config_kwargs["system_instruction"] = request.system_instruction

        config = genai_types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

        # 4. Execute via AsyncClient
        start_time = time.perf_counter()
        try:
            resp = await self.client.aio.models.generate_content(
                model=request.model_id,
                contents=contents,
                config=config,
            )
        except Exception as exc:
            raise self._normalize_error(exc, model_id=request.model_id) from exc

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        # 5. Extract response text and metadata
        response_text = resp.text if hasattr(resp, "text") else None
        usage = self._normalize_token_usage(getattr(resp, "usage_metadata", None))
        
        finish_reason = None
        if hasattr(resp, "candidates") and resp.candidates:
            finish_reason = getattr(resp.candidates[0], "finish_reason", None)

        return ProviderResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model_id=request.model_id,
            text=response_text,
            structured_output=None,
            token_usage=usage,
            latency_ms=latency_ms,
            finish_reason=str(finish_reason) if finish_reason else None,
            raw_metadata={
                "model_version": getattr(resp, "model_version", None),
                "response_id": getattr(resp, "response_id", None),
            },
        )

    async def generate_structured(self, request: ProviderStructuredRequest) -> ProviderResponse:
        """
        Executes structured output generation.
        Passes Pydantic schema to Gemini and validates returned JSON strictly.
        Fails closed on schema violation or malformed JSON.
        """
        # 1. Validate certification against registry
        self._registry.validate_eligibility(request.model_id, provider=self.provider_name)

        # 2. Build SDK contents
        contents = self._build_contents_payload(
            prompt=request.prompt,
            messages=request.messages,
            images=request.images,
        )

        # 3. Configure structured output schema
        config_kwargs: Dict[str, Any] = {
            "response_mime_type": "application/json",
            "response_schema": request.response_schema,
        }
        if request.temperature is not None:
            config_kwargs["temperature"] = request.temperature
        if request.max_tokens is not None:
            config_kwargs["max_output_tokens"] = request.max_tokens
        if request.system_instruction:
            config_kwargs["system_instruction"] = request.system_instruction

        config = genai_types.GenerateContentConfig(**config_kwargs)

        # 4. Execute via AsyncClient
        start_time = time.perf_counter()
        try:
            resp = await self.client.aio.models.generate_content(
                model=request.model_id,
                contents=contents,
                config=config,
            )
        except Exception as exc:
            raise self._normalize_error(exc, model_id=request.model_id) from exc

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        # 5. Extract text and strictly parse JSON / Pydantic schema
        raw_text = resp.text if hasattr(resp, "text") else ""
        if not raw_text:
            raise ProviderMalformedOutputException(
                message="Gemini returned an empty structured response.",
                provider=self.provider_name,
                model_id=request.model_id,
                raw_output=raw_text,
            )

        try:
            # Strict Pydantic validation (never silently coerce invalid state)
            structured_data = request.response_schema.model_validate_json(raw_text)
        except (ValidationError, json.JSONDecodeError) as err:
            raise ProviderMalformedOutputException(
                message=f"Failed to parse or validate structured JSON response against schema '{request.response_schema.__name__}': {err}",
                provider=self.provider_name,
                model_id=request.model_id,
                raw_output=raw_text,
                details={"validation_error": str(err)},
            ) from err

        usage = self._normalize_token_usage(getattr(resp, "usage_metadata", None))

        finish_reason = None
        if hasattr(resp, "candidates") and resp.candidates:
            finish_reason = getattr(resp.candidates[0], "finish_reason", None)

        return ProviderResponse(
            request_id=request.request_id,
            provider=self.provider_name,
            model_id=request.model_id,
            text=raw_text,
            structured_output=structured_data,
            token_usage=usage,
            latency_ms=latency_ms,
            finish_reason=str(finish_reason) if finish_reason else None,
            raw_metadata={
                "model_version": getattr(resp, "model_version", None),
                "response_id": getattr(resp, "response_id", None),
            },
        )

    # =========================================================================
    # Model Metadata & Listing
    # =========================================================================

    async def list_models(self) -> List[ModelMetadata]:
        """Lists models from registry or query live discovery."""
        return self._registry.list_models(provider=self.provider_name)

    async def get_model(self, model_id: str) -> ModelMetadata:
        """Retrieves normalized metadata for a model from registry or live metadata."""
        model = self._registry.get(model_id)
        if model:
            return model
        
        # If not in local registry, query Google metadata
        try:
            m = await self.client.aio.models.get(model=model_id)
            normalized_id = m.name.replace("models/", "") if m.name else model_id
            return ModelMetadata(
                provider=self.provider_name,
                model_id=normalized_id,
                api_version="v1",
                display_name=getattr(m, "display_name", None),
                description=getattr(m, "description", None),
                input_token_limit=getattr(m, "input_token_limit", None),
                output_token_limit=getattr(m, "output_token_limit", None),
                supported_modalities=["text", "image"],
                supports_structured_output=True,
                supports_tools=True,
                supports_streaming=True,
                lifecycle_status="active",
                availability_status="available",
                certification_status="UNCERTIFIED",
            )
        except Exception as exc:
            raise self._normalize_error(exc, model_id=model_id) from exc

    # =========================================================================
    # Lightweight Health Check
    # =========================================================================

    async def health_check(self) -> ProviderHealthResult:
        """
        Lightweight provider health check.
        Queries live model metadata without generating text or burning quota.
        """
        start_time = time.perf_counter()
        try:
            # Query candidate model metadata (e.g. gemini-3.5-flash-lite)
            await self.client.aio.models.get(model="gemini-3.5-flash-lite")

            latency_ms = int((time.perf_counter() - start_time) * 1000)
            return ProviderHealthResult(
                provider=self.provider_name,
                is_healthy=True,
                latency_ms=latency_ms,
                details={
                    "checked_model": "gemini-3.5-flash-lite",
                    "status": "connected",
                },
            )
        except Exception as exc:
            latency_ms = int((time.perf_counter() - start_time) * 1000)
            norm_err = self._normalize_error(exc, model_id="gemini-3.5-flash-lite")
            return ProviderHealthResult(
                provider=self.provider_name,
                is_healthy=False,
                latency_ms=latency_ms,
                details={
                    "error_code": norm_err.error_code.value,
                    "is_transient": norm_err.is_transient,
                },
                error_message=norm_err.message,
            )
