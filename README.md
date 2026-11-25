# Tutorial 1: Creating Your First API

Build a small web API and understand how a client asks a server for data. Python is our implementation language; the focus is web development concepts and good coding habits.

**Time:** 30–45 minutes. **Prerequisites:** Python 3.10+, Git, a text editor, and basic familiarity with functions and dictionaries.

## 1. Understand the request and response

An API is an interface through which programs interact. A web API uses HTTP requests and responses.

Your browser is the **client**; our Python application is the **server**. For example:

```text
Client -> GET /hello?name=Ada -> Server
Client <- 200 OK + JSON body <- Server
```

- **GET** is an HTTP method for retrieving data.
- **/hello** is a path. A method and path together identify an endpoint.
- **?name=Ada** supplies input through a query parameter.
- **JSON** is a text format for structured data.
- The **status code** describes the outcome; the **body** contains returned data.

## 2. Get the lesson

```sh
git clone --branch tutorial-01-first-api https://github.com/Jxstxn629/web-dev-foundations.git
cd web-dev-foundations
```

The repository is private, so cloning requires access and GitHub authentication. Already cloned it? Save your changes, run `git fetch origin`, then `git switch tutorial-01-first-api`.

This branch includes a completed `main.py`. Run it to explore, or replace its contents with step 4 and build it up yourself.

## 3. Install dependencies

Create an isolated environment so this project's packages stay separate.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` instead of `python` in the installation and server commands. No execution-policy change is needed.

**macOS / Linux:**

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

FastAPI defines our endpoints. Uvicorn runs the HTTP server. The requirements file pins the direct dependencies to the versions checked for this lesson.

## 4. Create your first endpoint

Put this in `main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="My First API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to your first API!"}
```

The decorator `@app.get("/")` connects GET requests for the root path to `read_root`. The function returns a dictionary, which FastAPI converts to JSON. The return annotation describes the expected Python value.

## 5. Start the server

Run this from the folder containing `main.py`:

```sh
python -m uvicorn main:app --reload
```

`main:app` means “use the app object in main.py.” `--reload` restarts the server when code changes; use it for local development.

Leave the terminal running. Open <http://127.0.0.1:8000/> in your browser:

```json
{"message": "Welcome to your first API!"}
```

`127.0.0.1` means your own computer, and `8000` is the server's port.

Open <http://127.0.0.1:8000/docs>. Expand **GET /**, select **Try it out**, then **Execute**. Inspect the status code (`200`), response body, and `application/json` content type.

## 6. Accept a query parameter

Change the first import to:

```python
from fastapi import FastAPI, Query
```

Keep your existing app and root endpoint, then append:

```python
@app.get("/hello")
def greet(name: str = Query(default="world", min_length=1, max_length=50)) -> dict[str, str]:
    return {"message": f"Hello, {name}!"}
```

Visit <http://127.0.0.1:8000/hello?name=Ada>. Expected response:

```json
{"message": "Hello, Ada!"}
```

Omitting `name` uses the default value `world`. Supplying an empty name fails validation. Names must contain 1–50 characters; spaces still count as characters.

## 7. Check success and failure

Try these URLs in your browser. Open developer tools, choose **Network**, and reload to inspect status codes. You can also try the defined endpoints in `/docs`.

| Request | Status | Expected result |
| --- | --- | --- |
| GET / | 200 | Welcome message |
| GET /hello | 200 | Hello, world! |
| GET /hello?name=Ada | 200 | Hello, Ada! |
| GET /hello?name= | 422 | Input validation error |
| GET /missing | 404 | Endpoint not found |

A `404` means no matching route was found. A `422` here means the input violated the endpoint's validation rules. Read the error body for details.

## 8. Practice

1. Add `GET /health` returning `{"status":"ok"}`. Verify status 200 and check that it appears in `/docs`.
2. Add `GET /about` returning a project name and a short description. Choose clear JSON keys.
3. Try a 50-character name and a 51-character name. Predict the status codes first.
4. Optional challenge: reject names consisting only of spaces. Decide what error response to return, and confirm normal names still work.

## Good habits

- Give functions descriptive names and keep endpoints focused.
- Validate input at the API boundary; check invalid inputs as well as valid ones.
- Use GET to retrieve data without changing application state.
- Keep packages in a virtual environment and dependencies in the repository.
- Keep secrets and local environment files out of Git; this branch includes a `.gitignore`.
- Make a small commit after each working exercise and describe the change.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Python command not found | Install Python and reopen the terminal; use python3 on macOS/Linux when creating the environment. |
| No module named fastapi or uvicorn | Install requirements using the same environment's Python that runs the server. |
| Could not import module main | Run the server from the directory containing main.py. |
| Port already in use | Stop the other server, or add --port 8001 and use 8001 in your URLs. |
| Browser cannot connect | Keep the server running and check the terminal for errors. |

Stop the server with **Ctrl+C**. If you activated the environment, run `deactivate` when finished.

## Completion checklist

- [ ] Explain the client/server request and response.
- [ ] Identify the method, path, and query parameter in a request.
- [ ] Return JSON from an endpoint.
- [ ] Distinguish successful responses, validation errors, and missing routes.
- [ ] Complete the health and about exercises.

This lesson does not require a database or deployment. The repository's `main` branch remains an overview only; this branch contains Tutorial 1.

Further reading: [FastAPI first steps](https://fastapi.tiangolo.com/tutorial/first-steps/) and [query validation](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/).
