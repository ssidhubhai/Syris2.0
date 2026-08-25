from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.db.session import get_db

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as exc:
        db_status = f"unhealthy: {str(exc)}"

    return {
        "status": "online",
        "service": "syris-backend",
        "database": db_status,
    }
