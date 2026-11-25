"""A notes application that remembers saved data across restarts."""

from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

import storage


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.initialize()
    yield


app = FastAPI(title="Persistent Notes", lifespan=lifespan)
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


@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=NoteCreatedResponse)
def create_note(note: NoteCreate) -> NoteCreatedResponse:
    saved = storage.save_note(str(uuid4()), note.title, note.content)
    created_note = NoteResponse(**saved)
    return NoteCreatedResponse(message="Note created", data=created_note)


@app.get("/notes", response_model=list[NoteResponse])
def list_notes() -> list[NoteResponse]:
    return [NoteResponse(**note) for note in storage.list_notes()]


@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: str) -> NoteResponse:
    note = storage.find_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(**note)
