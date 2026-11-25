"""Completed example for Tutorial 1: Creating Your First API."""

from fastapi import FastAPI, Query

app = FastAPI(title="My First API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to your first API!"}


@app.get("/hello")
def greet(name: str = Query(default="world", min_length=1, max_length=50)) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
