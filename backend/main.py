from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.bots import router as bots_router
from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.routes.metrics import router as metrics_router

app = FastAPI(title="AI Factory")

# Serve /static if present
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    try:
        return FileResponse("static/index.html")
    except Exception:
        return {"status": "ok", "app": "AI Factory"}


# Routers
app.include_router(health_router)
app.include_router(info_router)
app.include_router(bots_router)
app.include_router(metrics_router)
