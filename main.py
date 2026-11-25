"""Serve a notes form and its JSON API from the same application."""

from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="HTML Form and API")
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", response_class=FileResponse)
def read_page() -> FileResponse:
    return FileResponse(BASE_DIR / "pages" / "index.html", media_type="text/html")


class NoteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(default="", max_length=1000)


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str


class NoteCreatedResponse(BaseModel):
    message: str
    data: NoteResponse


notes: list[NoteResponse] = []


@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=NoteCreatedResponse)
def create_note(note: NoteCreate) -> NoteCreatedResponse:
    created_note = NoteResponse(id=str(uuid4()), title=note.title, content=note.content)
    notes.append(created_note)
    return NoteCreatedResponse(message="Note created", data=created_note)


@app.get("/notes", response_model=list[NoteResponse])
def list_notes() -> list[NoteResponse]:
    return notes
