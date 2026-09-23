from __future__ import annotations

from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.connection import get_database_status

app = FastAPI(title="DDOS Sentinel", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "backend",
        "version": "0.1.0",
        "timestamp": "2026-09-23T00:00:00Z",
    }


@app.get("/api/status")
def project_status() -> dict[str, Any]:
    db_status = get_database_status()
    return {
        "project": "DDOS Sentinel",
        "phase": "stage_a_scaffold",
        "status": "initializing",
        "backend": "online",
        "database": db_status,
        "kafka": "pending",
        "spark": "pending",
        "ml_model": "pending",
        "demo_mode": "available",
    }


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "DDOS Sentinel backend is running"}
