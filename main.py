"""Completed example for Tutorial 2: Returning HTML from a GET Endpoint."""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="HTML Response Example")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to your first API!"}


@app.get("/page", response_class=HTMLResponse)
def read_page() -> str:
    return """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My First Web Page</title>
</head>
<body>
    <main>
        <h1>Hello from the server!</h1>
        <p>This HTML was returned by a GET endpoint.</p>
        <ul>
            <li>The browser requests a page.</li>
            <li>The server responds with HTML.</li>
            <li>The browser renders the HTML.</li>
        </ul>
        <p><a href="/">Compare with a JSON response</a></p>
    </main>
</body>
</html>"""
