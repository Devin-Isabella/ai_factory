from typing import Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/bots", tags=["bots"])


@router.get("/", response_model=List[Dict])
def list_bots():
    return [
        {"id": "demo-1", "name": "Calendar Helper", "status": "published"},
        {"id": "demo-2", "name": "Email Draft Pro", "status": "draft"},
    ]
