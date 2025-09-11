from typing import Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/bots", tags=["bots"])


@router.get("/", response_model=List[Dict[str, str]])
def list_bots():
    # Placeholder data; replace with real store later.
    return [
        {"id": "demo-1", "name": "Calendar Assistant"},
        {"id": "demo-2", "name": "FAQ Helper"},
    ]
