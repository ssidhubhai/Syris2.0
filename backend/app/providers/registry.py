from datetime import datetime, timezone
from typing import Dict, List, Optional
from backend.app.providers.base import (
    ModelMetadata,
    ModelNotCertifiedException,
)


# Standard Certification Status Constants
CERTIFIED_FOR_DEV = "CERTIFIED_FOR_DEV"
CERTIFIED_FOR_PROD = "CERTIFIED_FOR_PROD"
CANDIDATE = "CANDIDATE"
UNCERTIFIED = "UNCERTIFIED"
DEPRECATED = "DEPRECATED"
BLOCKED = "BLOCKED"


class ModelRegistry:
    """Thread-safe catalog of certified and candidate AI models."""

    def __init__(self, populate_defaults: bool = True):
        self._models: Dict[str, ModelMetadata] = {}
        if populate_defaults:
            self._register_default_certified_models()

    def _register_default_certified_models(self) -> None:
        """
        Registers the certified development candidate models verified on 2026-08-25.
        None of these are hardcoded as universal application-wide defaults.
        """
        now = datetime(2026, 8, 25, 0, 0, 0, tzinfo=timezone.utc)

        # 1. Gemini 3.5 Flash Lite (High-throughput, fast student responses)
        self.register(
            ModelMetadata(
                provider="google",
                model_id="gemini-3.5-flash-lite",
                api_version="v1",
                display_name="Gemini 3.5 Flash Lite",
                description="High-throughput, cost-effective multimodal model for JEE study workflows.",
                input_token_limit=1048576,
                output_token_limit=65536,
                supported_modalities=["text", "image"],
                supports_structured_output=True,
                supports_tools=True,
                supports_streaming=True,
                lifecycle_status="active",
                availability_status="available",
                certification_status=CERTIFIED_FOR_DEV,
                benchmark_status="passed_dev_smoke",
                last_verified_at=now,
            )
        )

        # 2. Gemini 3.5 Flash (Balanced quality/latency candidate)
        self.register(
            ModelMetadata(
                provider="google",
                model_id="gemini-3.5-flash",
                api_version="v1",
                display_name="Gemini 3.5 Flash",
                description="Balanced multimodal reasoning model for comprehensive JEE problem solving.",
                input_token_limit=1048576,
                output_token_limit=65536,
                supported_modalities=["text", "image"],
                supports_structured_output=True,
                supports_tools=True,
                supports_streaming=True,
                lifecycle_status="active",
                availability_status="available",
                certification_status=CERTIFIED_FOR_DEV,
                benchmark_status="passed_dev_smoke",
                last_verified_at=now,
            )
        )

        # 3. Gemini 2.5 Flash (Stable proven fallback candidate)
        self.register(
            ModelMetadata(
                provider="google",
                model_id="gemini-2.5-flash",
                api_version="v1",
                display_name="Gemini 2.5 Flash",
                description="Stable multimodal fallback model for JEE derivation validation.",
                input_token_limit=1048576,
                output_token_limit=65536,
                supported_modalities=["text", "image"],
                supports_structured_output=True,
                supports_tools=True,
                supports_streaming=True,
                lifecycle_status="active",
                availability_status="available",
                certification_status=CERTIFIED_FOR_DEV,
                benchmark_status="passed_dev_smoke",
                last_verified_at=now,
            )
        )

    def register(self, metadata: ModelMetadata) -> None:
        """Registers or updates model metadata in the registry."""
        self._models[metadata.model_id] = metadata

    def get(self, model_id: str) -> Optional[ModelMetadata]:
        """Retrieves model metadata by model ID."""
        return self._models.get(model_id)

    def is_certified(self, model_id: str, required_status: str = CERTIFIED_FOR_DEV) -> bool:
        """Checks if a model is registered and meets the required certification status."""
        model = self.get(model_id)
        if not model:
            return False
        # If looking for DEV, both DEV and PROD qualify
        if required_status == CERTIFIED_FOR_DEV:
            return model.certification_status in (CERTIFIED_FOR_DEV, CERTIFIED_FOR_PROD)
        return model.certification_status == required_status

    def list_models(
        self,
        provider: Optional[str] = None,
        certified_only: bool = False,
    ) -> List[ModelMetadata]:
        """Lists models filtered by provider and certification state."""
        results = list(self._models.values())
        if provider:
            results = [m for m in results if m.provider == provider]
        if certified_only:
            results = [m for m in results if m.certification_status in (CERTIFIED_FOR_DEV, CERTIFIED_FOR_PROD)]
        return results

    def validate_eligibility(
        self,
        model_id: str,
        provider: str = "google",
        required_status: str = CERTIFIED_FOR_DEV,
    ) -> ModelMetadata:
        """
        Validates model eligibility against the certified registry.
        Fails closed with ModelNotCertifiedException if unknown or uncertified.
        """
        model = self.get(model_id)
        if not model:
            raise ModelNotCertifiedException(
                model_id=model_id,
                provider=provider,
                message=f"Model '{model_id}' is not registered in the certified model catalog.",
                details={"model_id": model_id, "provider": provider},
            )
        if not self.is_certified(model_id, required_status=required_status):
            raise ModelNotCertifiedException(
                model_id=model_id,
                provider=provider,
                message=f"Model '{model_id}' has certification status '{model.certification_status}', which does not satisfy '{required_status}'.",
                details={
                    "model_id": model_id,
                    "provider": provider,
                    "certification_status": model.certification_status,
                    "required_status": required_status,
                },
            )
        return model


# Default singleton instance for application use
default_registry = ModelRegistry()
