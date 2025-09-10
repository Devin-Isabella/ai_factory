# backend/app/routes/info.py
from __future__ import annotations

import datetime as _dt
import os
import platform
import socket
from typing import Any, Dict, List

from fastapi import APIRouter, Request
import psycopg2  # For health check (DB)

router = APIRouter(prefix="/info", tags=["info"])


def _safe_env() -> Dict[str, str]:
    """Return a small safe subset of environment info (no secrets)."""
    allow = {
        "OS",
        "PROCESSOR_ARCHITECTURE",
        "NUMBER_OF_PROCESSORS",
        "COMPUTERNAME",
        "USERNAME",
    }
    out: Dict[str, str] = {}
    for k in allow:
        v = os.environ.get(k)
        if v:
            out[k] = v
    return out


@router.get("/ping")
def ping() -> Dict[str, Any]:
    return {"ok": True, "time_utc": _dt.datetime.utcnow().isoformat() + "Z"}


@router.get("/env")
def env() -> Dict[str, Any]:
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "hostname": socket.gethostname(),
        "safe_env": _safe_env(),
    }


@router.get("/routes")
def routes(request: Request) -> Dict[str, List[Dict[str, Any]]]:
    items: List[Dict[str, Any]] = []
    for r in request.app.routes:
        items.append(
            {
                "path": getattr(r, "path", None),
                "name": getattr(r, "name", None),
                "methods": sorted(getattr(r, "methods", []) or []),
            }
        )
    return {"routes": items}


@router.get("/version")
def version() -> Dict[str, Any]:
    """Read VERSION file (if present)."""
    version_file = "VERSION"
    if os.path.exists(version_file):
        with open(version_file) as f:
            ver = f.read().strip()
    else:
        ver = "0.0.0-dev"
    return {"version": ver}


@router.get("/health")
def health() -> Dict[str, Any]:
    """Check DB connectivity."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return {"db": "skipped (no DATABASE_URL set)"}

    try:
        conn = psycopg2.connect(db_url, connect_timeout=3)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        return {"db": "ok"}
    except Exception as e:
        return {"db": f"error: {e}"}
