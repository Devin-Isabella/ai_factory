from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.routes.info import router as info_router
from app.routes.health import router as health_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")

@app.get("/")
async def root():
    return FileResponse("backend/app/static/index.html")

app.include_router(info_router)
app.include_router(health_router)
