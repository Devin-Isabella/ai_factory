from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.routes.bots import router as bots_router
from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.routes.metrics import router as metrics_router

# Paths
ROOT = Path(__file__).resolve().parent
STATIC_DIR = ROOT / "app" / "static"
INDEX_FILE = STATIC_DIR / "index.html"

app = FastAPI(title="AI Factory")

# /static -> backend/app/static
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Landing page (hide from OpenAPI)
@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    return FileResponse(str(INDEX_FILE))

# API routers
app.include_router(health_router)
app.include_router(info_router)
app.include_router(bots_router)
app.include_router(metrics_router)

# ---- SPA fallback -----------------------------------------------------------
# Any non-API, non-static, non-docs path will serve index.html so
# deep links like /builder or /store work without a 404.
DOC_PATHS = {"/docs", "/redoc", "/openapi.json"}
API_PREFIXES = ("/health", "/info", "/bots", "/metrics", "/static")

@app.middleware("http")
async def spa_fallback(request: Request, call_next):
    path = request.url.path

    # Pass through for known API/static/docs
    if path == "/" or path in DOC_PATHS or path.startswith(API_PREFIXES):
        return await call_next(request)

    # If the file exists under /static, let StaticFiles handle it
    candidate = STATIC_DIR / path.lstrip("/")
    if candidate.exists() and candidate.is_file():
        return await call_next(request)

    # Otherwise serve the SPA entry (index.html)
    if INDEX_FILE.exists():
        return FileResponse(str(INDEX_FILE), media_type="text/html")

    # If index.html somehow missing, return clear JSON instead of generic 404
    return JSONResponse({"detail": "landing index.html missing"}, status_code=500)
# ---------------------------------------------------------------------------
