# Tutorial 5: Making Your Notes App Remember Data

Create a note, restart the server, and find the same note again. Then retrieve one note by ID and handle a missing note gracefully.

This lesson focuses on application behavior. The storage setup is provided; you do not need to design a database or learn SQL to complete the exercises.

**Standalone:** all code is included. **Time:** 30–40 minutes. **Prerequisites:** Python 3.10+, Git, a browser, a text editor, and basic Python and HTML familiarity. Earlier tutorials are optional.

## 1. Get the project

```sh
git clone --branch tutorial-05-persistent-notes https://github.com/Jxstxn629/web-dev-foundations.git
cd web-dev-foundations
```

Already cloned? Save or commit your changes, stop the running server, then use:

```sh
git fetch origin
git switch tutorial-05-persistent-notes
```

This branch contains the complete working application. Run it first, then follow the experiments below.

| File | What it does |
| --- | --- |
| main.py | Serves the page, validates requests, and defines API responses. |
| storage.py | Provided helpers for saving and retrieving notes. |
| pages/index.html | Create-note form, saved-note list, and ID lookup form. |
| static/app.js | Sends requests and updates the page. |
| static/styles.css | Page styling. |
| data/notes.db | Local data file, created automatically on first startup. |

## 2. Run the application

Create an isolated environment. If .venv already exists, skip creating it.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

If activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python` for installation and server commands.

**macOS / Linux:**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Keep the terminal running and open <http://127.0.0.1:8000/>. Open the page through the server rather than double-clicking the HTML file. Interactive API documentation is at <http://127.0.0.1:8000/docs>.

SQLite support comes with Python; there is no separate database server to install. The supplied setup creates its local file and prepares storage without removing existing notes.

## 3. Save a note and read the response

Enter a title and some content, then select **Create note**.

The browser sends a JSON body:

```json
{"title": "Remember this", "content": "This note should survive a restart."}
```

POST /notes validates it, saves the note, and returns status **201 Created**:

```json
{
  "message": "Note created",
  "data": {
    "id": "a-server-generated-UUID",
    "title": "Remember this",
    "content": "This note should survive a restart."
  }
}
```

The ID above is a placeholder. Copy the actual ID shown under your note in the page.

The browser then calls GET /notes and displays the saved records. A successful POST response is sent only after the storage helper completes its save.

## 4. Prove the app remembers

1. Create a note with a distinctive title.
2. Record its ID and content.
3. Stop the server using Ctrl+C.
4. Start it again using the same command, from the same project copy.
5. Reload the page or select **Refresh notes**.
6. Confirm the title, content, and ID are unchanged.

A browser refresh is not a server restart. Test both so you can distinguish them.

A Python list in server memory disappears when that process ends. This version writes notes to data/notes.db, which remains on disk after the process exits. Reopening the page reads the saved records from the server; the browser is not storing them in localStorage.

The file belongs to this project copy. Running a different clone uses a different file. Deleting the file deletes its saved data.

## 5. Read the small change in the endpoint

The endpoint uses the provided helper:

```python
@app.post("/notes", status_code=status.HTTP_201_CREATED, response_model=NoteCreatedResponse)
def create_note(note: NoteCreate) -> NoteCreatedResponse:
    saved = storage.save_note(str(uuid4()), note.title, note.content)
    created_note = NoteResponse(**saved)
    return NoteCreatedResponse(message="Note created", data=created_note)
```

NoteCreate validates input. storage.save_note handles persistence. NoteResponse describes the public fields, and NoteCreatedResponse wraps them in message/data. The **saved syntax passes the dictionary's keys and values into the model.

The JSON contract stays the same even though storage has changed. The form can continue sending title and content without knowing how the server saves them.

The helper interface is deliberately small:

| Helper | Result |
| --- | --- |
| initialize() | Prepares storage at application startup. |
| save_note(id, title, content) | Saves and returns a note dictionary. |
| list_notes() | Returns all saved notes in insertion order. |
| find_note(id) | Returns one note dictionary, or None if absent. |

You can treat these as supplied building blocks. The implementation uses parameterized queries to keep values separate from SQL, commits successful writes, and closes connections. No SQL exercises are required here.

## 6. Retrieve one note by ID

Use **Find a note by ID** on the page. Paste an ID from the saved-note list and select **Find note**.

The browser calls GET /notes/{note_id}. In main.py:

```python
@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: str) -> NoteResponse:
    note = storage.find_note(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteResponse(**note)
```

The braces mark a path parameter. FastAPI passes that part of the URL into note_id. Unlike the POST success wrapper, this endpoint returns the note object directly with status 200.

You can also open /docs, expand GET /notes/{note_id}, and supply the saved ID using **Try it out**. IDs are treated as strings in this lesson; any nonmatching single-segment ID returns 404.

## 7. Handle a missing note

Search for missing-note, or open <http://127.0.0.1:8000/notes/missing-note>.

Expect status **404 Not Found** and:

```json
{"detail": "Note not found"}
```

In the page, the lookup handler checks response.status === 404 before trying to render a note. It clears any previous lookup result and displays “Note not found. Check the ID and try again.”

A missing record is different from a failed connection. If the server cannot be reached, the page tells you to check the connection. It does not claim the note is missing.

The application also keeps input validation: a title containing only spaces returns 422 from POST /notes. A rejected request must not create a saved note.

## 8. Verify the user experience

| Action | Expected behavior |
| --- | --- |
| Create a valid note | 201, a success message, and the note appears in the list. |
| Refresh the browser | The saved note is still listed. |
| Stop and restart the server | The same note and ID remain. |
| Find an existing ID | 200 and the matching note. |
| Find missing-note after a successful lookup | 404, a useful message, and the old result is cleared. |
| Submit a spaces-only title | Field error; no saved note is added. |
| Enter a title containing <b>text</b> | Tags display literally, without becoming HTML. |
| Stop the server and try a lookup | Connection feedback; the lookup controls become usable again. |

Watch the Network tab in browser developer tools to see the method, URL, status, and response body.

## 9. Practice

1. Save two notes, restart, and verify both titles and IDs.
2. Change the message shown for a missing note without changing the API's 404 status.
3. Add a “Find this note” button to each listed note that fills and submits the lookup form.
4. Show the number of saved notes after each successful refresh.
5. Explain why two POST requests with the same title create separate notes.
6. Optional: display the found note's ID alongside its title and content.

Keep storage.py unchanged while completing these exercises. The aim is to practice the application flow and response handling.

## Good habits

- Keep storage details behind small helpers.
- Preserve request and response contracts when changing internal implementation.
- Confirm persistence by restarting the process, not just reloading the browser.
- Distinguish missing data (404), invalid input (422), and connection failures.
- Keep generated local data out of source control; data/ is ignored by Git.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Notes vanish after restart | Confirm you are using this branch, the same project copy, and its data/notes.db file. |
| Storage cannot be opened | Make sure this project folder is writable and inspect the server terminal. |
| Lookup gives 404 | Copy the full ID from the list, without the "ID:" label. |
| Old lookup result remains | Ensure the current static/app.js is loaded; hard-refresh after edits. |
| No module named fastapi or uvicorn | Install requirements with the same environment's Python that runs the server. |
| Port already in use | Stop the other server, or add --port 8001 and use that port in the browser. |

Stop the server with **Ctrl+C**. Run deactivate if you activated the environment. Your notes remain on disk.

This is a local learning application with one shared notes collection. User accounts, deployment, database design, and schema migrations are outside this lesson.

## Completion checklist

- [ ] Create and list notes using the form and API.
- [ ] Prove that notes and IDs survive a server restart.
- [ ] Retrieve one note using a path parameter.
- [ ] Handle missing notes without confusing them with network failures.
- [ ] Explain the purpose of the storage helpers without needing to write SQL.

Further reading (optional): [FastAPI errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [application lifespan](https://fastapi.tiangolo.com/advanced/events/), and [Python's SQLite support](https://docs.python.org/3/library/sqlite3.html).
