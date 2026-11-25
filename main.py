"""Completed example for Tutorial 2: Returning HTML from a GET Endpoint."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="HTML Response Example")
PAGE_PATH = Path(__file__).resolve().parent / "pages" / "index.html"


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to your first API!"}


@app.get("/page", response_class=FileResponse)
def read_page() -> FileResponse:
    return FileResponse(PAGE_PATH, media_type="text/html")
