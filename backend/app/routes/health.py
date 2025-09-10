from fastapi import APIRouter
from datetime import datetime
import asyncpg
import os

router = APIRouter()

# Track server start time for uptime reporting
START_TIME = datetime.utcnow()

# Database connection settings (from environment or defaults)
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "aifactory")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

async def check_db():
    """Try connecting to Postgres; return True if healthy."""
    try:
        conn = await asyncpg.connect(
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            host=DB_HOST,
            port=DB_PORT,
        )
        await conn.close()
        return True
    except Exception:
        return False

@router.get("/health")
async def health():
    uptime = (datetime.utcnow() - START_TIME).total_seconds()
    db_ok = await check_db()
    return {
        "status": "ok",
        "uptime_seconds": int(uptime),
        "db": "ok" if db_ok else "down",
    }