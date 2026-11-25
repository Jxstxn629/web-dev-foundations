"""Provided storage helpers. Routes do not need to know SQL."""

import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "data" / "notes.db"


def initialize() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS notes "
                "(id TEXT PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL)"
            )


def save_note(note_id: str, title: str, content: str) -> dict[str, str]:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute(
                "INSERT INTO notes (id, title, content) VALUES (?, ?, ?)",
                (note_id, title, content),
            )
    return {"id": note_id, "title": title, "content": content}


def list_notes() -> list[dict[str, str]]:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT id, title, content FROM notes ORDER BY rowid"
        ).fetchall()
    return [dict(row) for row in rows]


def find_note(note_id: str) -> dict[str, str] | None:
    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT id, title, content FROM notes WHERE id = ?", (note_id,)
        ).fetchone()
    return dict(row) if row is not None else None
