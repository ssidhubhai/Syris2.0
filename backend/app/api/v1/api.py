from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    dev,
    explanations,
    health,
    messages,
    sessions,
    study,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(sessions.router, tags=["Sessions"])
api_router.include_router(messages.router, tags=["Messages"])
api_router.include_router(explanations.router, tags=["Explanations"])
api_router.include_router(study.router, prefix="/study", tags=["Study"])
api_router.include_router(dev.router, prefix="/dev", tags=["Dev"])


