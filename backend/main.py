from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount(
    "/static",
    StaticFiles(directory="backend/app/static"),
    name="static"
)

# Serve landing page
@app.get("/")
async def root():
    return FileResponse("backend/app/static/index.html", media_type="text/html")