from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routes.bots import router as bots_router
from app.routes.health import router as health_router
from app.routes.info import router as info_router
from app.routes.metrics import router as metrics_router

app = FastAPI(title="AI Factory")

# /static -> backend/app/static
app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

# Landing page (hide from OpenAPI)
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("backend/app/static/index.html")

# API routers
app.include_router(health_router)
app.include_router(info_router)
app.include_router(bots_router)
app.include_router(metrics_router)
