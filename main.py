"""A small notes API for learning POST requests."""

from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="My First POST Endpoint")


class NoteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(default="", max_length=1000)


class Note(NoteCreate):
    id: str


notes: list[Note] = []


@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=Note)
def create_note(note: NoteCreate) -> Note:
    created_note = Note(id=str(uuid4()), title=note.title, content=note.content)
    notes.append(created_note)
    return created_note


@app.get("/notes", response_model=list[Note])
def list_notes() -> list[Note]:
    return notes
