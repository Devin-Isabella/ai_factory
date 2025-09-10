# backend/main.py
from __future__ import annotations

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="AI Factory")

# Serve static files (CSS, JS, images)
app.mount(
    "/static",
    StaticFiles(directory="backend/app/static"),
    name="static",
)

# Include the Info router (works whether package root is 'app' or 'backend.app')
try:
    from app.routes.info import router as info_router  # type: ignore
except Exception:  # pragma: no cover
    from backend.app.routes.info import router as info_router  # type: ignore

app.include_router(info_router)

# Landing page
@app.get("/")
async def root():
    return FileResponse("backend/app/static/index.html")
