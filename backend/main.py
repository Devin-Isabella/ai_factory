from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.routes.Metrics import router as metrics_router  # capital M to match file name
from app.routes.bots import router as bots_router

app = FastAPI(title="AI Factory")

# Routers
app.include_router(health_router)
app.include_router(info_router)
app.include_router(metrics_router)
app.include_router(bots_router)

# Static files (if you have a ./static folder)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/index")
def get_index():
    # If you have static/index.html, serve it. Otherwise returns 404.
    return FileResponse("static/index.html")
