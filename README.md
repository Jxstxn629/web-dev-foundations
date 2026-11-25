# Tutorial 3: Creating a POST Endpoint

Build a POST endpoint that accepts JSON, then extend it with a Pydantic request model to validate input and create notes.

This lesson is standalone. **Time:** 35–45 minutes. **Prerequisites:** Python 3.10+, Git, a text editor, and basic Python functions, dictionaries, and classes.

## 1. Get the lesson

```sh
git clone --branch tutorial-03-post-endpoint https://github.com/Jxstxn629/web-dev-foundations.git
cd web-dev-foundations
```

Already cloned the repository? Save or commit your work, stop the running server, then run:

```sh
git fetch origin
git switch tutorial-03-post-endpoint
```

The checked-in main.py is the completed extension from step 7. To build it progressively, replace main.py with the initial example in step 3, then follow the remaining steps.

## 2. Set up Python

A virtual environment keeps this project's packages separate. If .venv already exists, skip the creation command.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If activation is blocked, use `.\.venv\Scripts\python.exe` instead of `python` in installation and server commands.

**macOS / Linux:**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

FastAPI handles routing, Uvicorn runs the server, and Pydantic defines and validates data models. requirements.txt pins the direct dependencies used for this lesson.

## 3. Create a basic POST endpoint

A client sends an HTTP request; the server sends a response. GET usually retrieves data. POST submits data for processing, often to create a resource.

The **request body** contains data sent to the server. The **response body** contains data returned by the server. JSON represents structured data using objects, lists, and values.

Put this complete starter application in main.py:

```python
from fastapi import FastAPI

app = FastAPI(title="My First POST Endpoint")


@app.post("/notes")
def receive_note(payload: dict[str, str]) -> dict[str, str]:
    return payload
```

The decorator connects POST /notes to receive_note. The dictionary parameter tells FastAPI to read a JSON object from the request body. Its keys and values must be strings, but this initial version does not require specific fields or validate their lengths.

This endpoint echoes the submitted data and returns 200 OK. It does not create or save a note yet.

## 4. Send a POST request

Start the server from the folder containing main.py:

```sh
python -m uvicorn main:app --reload
```

main:app selects the app object in main.py. --reload restarts the server when Python code changes; use it for local development. Keep the terminal running.

Open <http://127.0.0.1:8000/docs>. The address refers to your computer, on port 8000.

1. Expand **POST /notes**.
2. Select **Try it out**.
3. Replace the example body with:

```json
{
  "title": "Learn POST requests",
  "content": "Send JSON to my API."
}
```

4. Select **Execute**.
5. Inspect the response: status 200 and the same JSON object.

The request's Content-Type is application/json. This tells the server how to interpret the body. Typing /notes into the browser's address bar sends GET, not POST; the starter application returns 405 Method Not Allowed for that request.

## 5. Try a command-line client

Keep the server running and open another terminal.

**PowerShell:**

```powershell
$body = @{
    title = "Learn POST requests"
    content = "Send JSON to my API."
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/notes" -Method Post -ContentType "application/json" -Body $body
```

**macOS / Linux:**

```sh
curl -i http://127.0.0.1:8000/notes \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn POST requests","content":"Send JSON to my API."}'
```

curl's -d option sends a POST body; -i displays response headers. PowerShell's Invoke-RestMethod displays parsed data; use /docs to inspect the response code.

## 6. Extension: create a Pydantic request model

Try sending {} to the starter endpoint. It succeeds because a dictionary alone does not specify which fields your application needs.

A request model describes the accepted fields and their validation rules. Add this import and class above your endpoint:

```python
from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=100)
    content: str = Field(default="", max_length=1000)
```

| Rule | Meaning |
| --- | --- |
| title: str without a default | title is required and must be a string. |
| min_length=1, max_length=100 | The title must contain 1–100 characters after trimming. |
| content with default="" | content can be omitted; it defaults to an empty string. |
| max_length=1000 | Content may contain at most 1,000 characters after trimming. |
| str_strip_whitespace=True | Remove surrounding whitespace from string fields. A spaces-only title becomes empty and fails validation. |
| extra="forbid" | Reject unexpected fields, including a client-supplied id. |

Now replace the starter endpoint with:

```python
@app.post("/notes")
def receive_note(note: NoteCreate) -> NoteCreate:
    return note
```

FastAPI reads the body and validates it before calling receive_note. The function receives a NoteCreate object, so fields are accessed as note.title and note.content. Invalid input receives a 422 response with error details; the endpoint function is not called.

This serves a similar validation role to Laravel Form Requests. Pydantic models describe data; they do not automatically handle authorization or database uniqueness checks. More specialized rules can be added with Pydantic field validators and model validators.

For now, this version still echoes validated data with status 200. Refresh /docs to see the new request schema and try the missing-title and blank-title cases.

## 7. Extension: create a note from validated input

Replace main.py with the complete application below. It includes the model from step 6, stores notes in memory, and adds GET /notes to retrieve them.

```python
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
```

NoteCreate defines what clients may send. Note inherits those fields and adds a server-generated id for responses. uuid4 generates the identifier; the client does not choose it.

POST /notes now creates a note and returns **201 Created**. response_model documents and validates the response shape. GET /notes returns the list with status 200.

The notes list is **temporary, process-local memory**. Restarting the server or triggering a code reload clears it. Run this example with a single server process; multiple workers would each have their own list. A database is a later topic.

Repeat the POST request in /docs. Expect:

```json
{
  "title": "Learn POST requests",
  "content": "Send JSON to my API.",
  "id": "a-server-generated-UUID"
}
```

The id above is a placeholder; your actual value will differ. Open <http://127.0.0.1:8000/notes> or execute GET /notes in /docs to see the created note.

Submitting the same POST twice creates two separate notes with different IDs. A POST request is not automatically deduplicated.

## 8. Check validation and errors

Use the completed version and replace the POST body in /docs for each case:

| Body or action | Expected result |
| --- | --- |
| {"title":"My note"} | 201; content defaults to an empty string. |
| {"title":"  My note  "} | 201; title becomes "My note". |
| {} | 422; required title is missing. |
| {"title":""} or {"title":"   "} | 422; title is too short. |
| {"title":123} | 422; title must be a string. |
| {"title":"Note","id":"chosen-by-client"} | 422; unexpected field. |
| Title of 101 characters | 422; title is too long. |
| Content of 1,001 characters | 422; content is too long. |
| Invalid JSON, such as a missing closing brace | 422; JSON cannot be parsed. |
| GET /notes | 200; current notes list. |
| POST /missing | 404; route not found. |

Inspect detail in the error response. Its loc identifies the input location, such as ["body", "title"]; msg explains the failure. Error text may vary by package version.

Compare GET /notes before and after an invalid POST: the list should not grow. Never rely only on client-side form validation.

## 9. Practice

1. Add an optional category field to NoteCreate, defaulting to "general", with a maximum length of 30. Update create_note so the submitted category reaches the created Note.
2. Test a title of exactly 100 characters, then 101. Predict the responses first.
3. Add a custom field validator that rejects a title containing a line break. Verify normal titles still work.
4. Restart the server and confirm the list is empty. Explain why a database would change this behavior.
5. Explain why POST and GET can use the same /notes path without being the same endpoint.

## Good habits

- Put input rules in a request model so the endpoint can focus on its work.
- Keep client-provided fields separate from server-generated values.
- Use 201 when a resource is created, and check error paths as well as success.
- Validate before changing application state.
- Do not confuse validation with authorization.
- Use a database when data must survive restarts.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No module named fastapi, pydantic, or uvicorn | Install requirements using the same environment's Python that runs the server. |
| Could not import module main | Run the command from the directory containing main.py. |
| GET /notes returns 405 | You are running the starter version, which only defines POST. |
| Valid-looking body returns 422 | Inspect detail; check spelling, types, lengths, and unexpected fields. |
| Notes disappear | Restarting or reloading the server clears in-memory data. |
| Port already in use | Stop the other server or add --port 8001 and use that port in your URLs. |

Stop the server with **Ctrl+C**. Run deactivate if you activated the environment.

## Completion checklist

- [ ] Send a JSON POST body through /docs or a command-line client.
- [ ] Explain the difference between request and response bodies.
- [ ] Define a Pydantic request model and explain its rules.
- [ ] Create a note with status 201 and retrieve it with GET.
- [ ] Confirm invalid requests do not create notes.
- [ ] Explain why notes disappear on restart.

Further reading: [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/), [response status codes](https://fastapi.tiangolo.com/tutorial/response-status-code/), and [Pydantic custom validators](https://docs.pydantic.dev/latest/concepts/validators/).
