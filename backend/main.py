from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.routes.info import router as info_router
from app.routes.health import router as health_router
try:
    from app.routes.metrics import router as metrics_router
except Exception:
    metrics_router = None

app = FastAPI(title="AI Factory")

# Static assets
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

# CORS (safe defaults; adjust if you add a separate frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Landing page (root)
@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("backend/app/static/index.html")

# Optional friendly shortcuts for static subpages
@app.get("/builder", response_class=HTMLResponse)
async def builder_page():
    return FileResponse("backend/app/static/builder.html")

@app.get("/store", response_class=HTMLResponse)
async def store_page():
    return FileResponse("backend/app/static/store.html")

# API routes
app.include_router(health_router)
app.include_router(info_router)
if metrics_router:
    app.include_router(metrics_router)
