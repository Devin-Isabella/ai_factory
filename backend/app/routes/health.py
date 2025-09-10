# backend/app/routes/health.py
from __future__ import annotations
import time
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter(prefix="", tags=["health"])

_STARTED = time.time()

@router.get("/health")
def health() -> Dict[str, Any]:
    """Liveness endpoint — tiny and fast."""
    return {
        "status": "ok",
        "uptime_seconds": round(time.time() - _STARTED, 2),
    }

@router.get("/ready")
def ready() -> Dict[str, Any]:
    """Readiness endpoint — expand later if you add checks."""
    return {"ready": True}
