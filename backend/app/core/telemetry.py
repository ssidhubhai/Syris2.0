import logging
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("syris.telemetry")
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s", "name":"%(name)s", "level":"%(levelname)s", "message":"%(message)s"}',
)


class TelemetryMiddleware(BaseHTTPMiddleware):
    """
    Captures request tracing telemetry:
    - Extracts or generates X-Request-ID
    - Attaches request_id to request state and response headers
    - Records latency in milliseconds
    - Emits structured log entries
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Extract or generate Request ID
        request_id = request.headers.get("X-Request-ID") or f"req-{uuid.uuid4().hex[:12]}"
        request.state.request_id = request_id
        
        start_time = time.perf_counter()
        
        status_code = 500
        error_category = None
        
        try:
            response = await call_next(request)
            status_code = response.status_code
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as exc:
            error_category = exc.__class__.__name__
            raise
        finally:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            # Sanitized path without query parameters if they contain sensitive data
            path = request.url.path
            method = request.method
            
            log_data = {
                "request_id": request_id,
                "method": method,
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "error_category": error_category,
            }
            
            if status_code >= 500:
                logger.error(f"HTTP Request Failed: {log_data}")
            elif status_code >= 400:
                logger.warning(f"HTTP Client Warning: {log_data}")
            else:
                logger.info(f"HTTP Request: {log_data}")
