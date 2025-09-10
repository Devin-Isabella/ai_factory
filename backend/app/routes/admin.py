from fastapi import APIRouter
from typing import Dict, List

router = APIRouter(prefix="/admin", tags=["admin"])

# Fake review queue
REVIEW_QUEUE: List[Dict] = []

@router.get("/review/queue")
def review_queue():
    """Return all bots waiting for admin approval (placeholder)."""
    return {"queue": REVIEW_QUEUE}

@router.post("/review/approve/{bot_id}")
def approve_bot(bot_id: str):
    """Approve a bot by ID (placeholder)."""
    return {"msg": f"Bot {bot_id} approved"}
