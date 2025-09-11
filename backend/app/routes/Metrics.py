from fastapi import APIRouter
import psutil

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/system")
def system_metrics():
    """Very basic system metrics."""
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()._asdict()
    return {"cpu_percent": cpu, "memory": mem}
