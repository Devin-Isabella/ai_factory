from fastapi import APIRouter
import psutil

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/system")
def system_metrics():
    vm = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    return {
        "cpu_percent": cpu_percent,
        "memory": {
            "total": vm.total,
            "available": vm.available,
            "percent": vm.percent,
            "used": vm.used,
            "free": vm.free,
        },
    }
