# Tutorial 2: Returning HTML from a GET Endpoint

Create a small Python web server from scratch and serve a web page. This lesson is standalone; no earlier tutorial is required. You will learn how the response's content type tells the browser what it received, and how HTML becomes a rendered page.

**Time:** 30–45 minutes. **Prerequisites:** Python 3.10+, Git, a text editor, and basic familiarity with Python functions and strings.

## 1. Get the lesson

For a fresh copy:

```sh
git clone --branch tutorial-02-html-response https://github.com/Jxstxn629/web-dev-foundations.git
cd web-dev-foundations
```

Already have the repository? Stop the server and save or commit your exercise changes before switching:

```sh
git fetch origin
git switch tutorial-02-html-response
```

This branch contains everything needed, including main.py, requirements.txt, and pages/index.html. The checked-in application is the final file-serving version from step 9. Run it directly, or replace main.py with step 3's inline version and follow the progression. Both versions use the same /page URL.

The example includes an HTML page and a small JSON endpoint for comparison. The main branch still contains only the repository overview.

## 2. Prepare the environment

A virtual environment keeps this project's Python packages separate from other projects. Create and activate one using the commands for your operating system below. If .venv already exists, skip its creation command.

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

requirements.txt lists the packages for this example. FastAPI connects URLs to Python functions; Uvicorn runs the HTTP server. Install them using the commands above.

## 3. Choose an HTML response

Your browser is the **client**. It sends an HTTP **request** to the Python **server**, which sends back a **response**. GET is the HTTP method used here to retrieve content. An endpoint is a method and path, such as GET /page.

A response includes a status code, headers, and a body. A status of 200 means success. The Content-Type header identifies the body's format: HTML for a web document or JSON for structured data.

Replace main.py with this complete application:

```python
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
```

app is the FastAPI application. Each @app.get decorator connects a path to the function below it. The root endpoint (/) returns a dictionary as JSON. The /page endpoint returns an HTML document.

The triple quotes create a multiline Python string. The function's return type is str; the decorator tells FastAPI to send that string using HTMLResponse. Its Content-Type is text/html with a UTF-8 charset. The endpoint is also documented as returning HTML.

Simply returning an HTML-looking string with FastAPI's default JSON response would serialize it as a JSON string. The response format must match the intended content.

## 4. Read the HTML

| Element | Purpose |
| --- | --- |
| <!doctype html> | Declares a modern HTML document. |
| html lang="en" | Sets the document language to English. |
| head | Contains metadata about the page. |
| meta charset | Declares the text encoding. |
| meta viewport | Helps the page use the device's viewport width. |
| title | Sets the browser tab's title. |
| body and main | Contain the visible page and its main content. |
| h1 and p | Define a heading and paragraph. |
| ul and li | Define a bulleted list and its items. |
| a href | Creates a link to another URL. |

The HTML uses meaningful elements so its structure is understandable without visual styling.

## 5. Run and inspect the page

```sh
python -m uvicorn main:app --reload
```

Keep the terminal running. In main:app, main refers to main.py and app is the application object. The --reload option restarts the server when you save changes; it is for local development. The address 127.0.0.1 refers to your computer and 8000 is the server's port.

Open <http://127.0.0.1:8000/page>. Expect a heading, a paragraph, a three-item list, and a link. The browser tab should say **My First Web Page**.

Click the link. It sends a new GET request to / and displays {"message":"Welcome to your first API!"} as JSON. Use your browser's Back button to return to the page.

Open developer tools, select **Network**, and reload /page. Select the page request and inspect:

- **Method:** GET.
- **Status:** 200 OK.
- **Content-Type:** text/html; charset=utf-8.
- **Response body:** the HTML source.

Use the browser's **View Page Source** command to compare the markup with the rendered page. The server sends text; the browser interprets its HTML structure. No JavaScript or separate HTML file is needed for this example.

## 6. Compare HTML and JSON

| Request | Content type | What the browser receives |
| --- | --- | --- |
| GET / | application/json | A welcome message as structured data. |
| GET /page | text/html; charset=utf-8 | A document to render as a page. |
| GET /missing | application/json | A 404 error response. |

JSON represents structured data using keys and values; HTML describes a document that the browser renders. A 404 response means the requested route was not found. HTML and JSON both travel in HTTP responses. Choosing HTML for one endpoint does not change the other endpoints.

Open <http://127.0.0.1:8000/docs> and try GET /page. Inspect the response body and headers there, then visit /page directly to see normal browser rendering.

## 7. Practice

1. Change the heading and tab title. Save, reload, and confirm both changed.
2. Add an h2 heading called “What I learned” followed by a list of three points.
3. Add GET /about returning a complete HTML document with status 200. Give it an appropriate title and a link back to /page.
4. Add a link from /page to /about. Follow both links and inspect their GET requests.
5. Predict what happens if you remove response_class=HTMLResponse from /page. Try it, inspect the content type and response body, then restore it.

## 8. Move the HTML into a file

Inline HTML is useful for a small first example. A separate file lets you edit the page without mixing markup with Python routing code.

Create a folder named pages beside main.py. Inside it, create index.html:

```text
web-dev-foundations/
|-- main.py
|-- requirements.txt
|-- pages/
    |-- index.html
```

Copy the HTML between the triple quotes in step 3 into pages/index.html. Include everything from <!doctype html> through </html>, but **do not include** the Python return statement or triple quotes. Save the file as UTF-8.

If you completed the practice exercises, move your updated HTML so your changes are preserved. The branch already includes index.html with the original example.

## 9. Serve the file from the GET endpoint

Replace main.py with this complete file-serving version. If you added an /about endpoint during practice, keep that function too.

```python
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
```

- Path comes from Python's standard library; no new package is needed.
- __file__ refers to main.py. Resolving its parent locates the project folder independently of the terminal's current directory.
- PAGE_PATH points to pages/index.html. The path's / operators join its parts across operating systems.
- FileResponse sends the file's contents. Setting media_type to text/html tells the browser to render HTML.
- The URL remains /page. A disk filename and a URL do not have to match.

Remove the old inline /page function rather than defining the same route twice. The HTMLResponse import is no longer needed.

This serves a fixed file, not a template: expressions such as {{ name }} are sent literally. FileResponse does not substitute Python variables into HTML. Only this specific file is exposed by the route; the pages directory is not automatically a public static directory.

## 10. Verify the file response

Keep the server running with the command from step 5, or start it again. Open <http://127.0.0.1:8000/page>.

1. Confirm that the page looks the same as the inline version.
2. Inspect the Network response: expect status 200 and Content-Type text/html; charset=utf-8.
3. Change the heading in pages/index.html, save, and refresh the browser. The endpoint reads the file for each request, so HTML-only edits do not need a server restart. Hard-refresh if your browser shows cached content.
4. Follow the JSON comparison link and confirm / still returns the welcome message.

A file response may also include Content-Length, Last-Modified, and ETag headers. These describe the file and can help clients handle caching.

## 11. Practice with HTML files

1. Move your /about page into pages/about.html and return it using FileResponse.
2. Link /page and /about to each other. Confirm both URLs return text/html.
3. Explain why returning a filename string from a default JSON endpoint would not send the file's contents.
4. Explain why PAGE_PATH is based on main.py rather than the current terminal directory.

## Good habits

- Use GET to retrieve a page without changing server-side data.
- Match the response type to the content you return.
- Use descriptive function names, page titles, and semantic HTML elements.
- Keep user input out of raw HTML strings. If you later insert user text into an HTML text node, escape it; use templates with autoescaping as pages grow. Validation alone does not make text safe to embed in HTML.
- Separate page markup from routing code as pages grow. Templates with dynamic values are a later step.
- Use a fixed, application-controlled file path; do not accept an unrestricted file path from a request.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No module named fastapi or uvicorn | Install requirements using the same virtual environment's Python that runs the server. |
| Could not import module main | Run the server command from the folder containing main.py. |
| Browser shows a quoted string instead of a page | For the inline version, check HTMLResponse. For the file version, return FileResponse rather than a filename from a default JSON endpoint. |
| File response fails with a server error | Check the terminal and confirm pages/index.html exists at PAGE_PATH; a missing server file is a setup error, not an automatic 404 response. |
| /page returns 404 | Check the URL, save main.py, and confirm you started the server from this lesson's directory. |
| Syntax error after editing HTML | Keep the opening and closing triple quotes intact. |
| Old page content appears | Save the file, check the reload logs, and refresh the browser. |
| Port already in use | Stop the earlier server with Ctrl+C, or use --port 8001 and update the URL. |

Stop the server with **Ctrl+C**. Run `deactivate` if you activated the environment.

## Completion checklist

- [ ] Explain when to use HTMLResponse and when to use FileResponse.
- [ ] Find the Content-Type header in browser developer tools.
- [ ] Distinguish HTML source from the rendered document.
- [ ] Create /about and navigate between the two pages.
- [ ] Move HTML into a separate file and serve it with FileResponse.
- [ ] Edit the HTML file and verify the updated page.
- [ ] Explain how the JSON response at / differs from the HTML response at /page.

Further reading: [FastAPI HTML responses](https://fastapi.tiangolo.com/advanced/custom-response/#html-response) and [file responses](https://fastapi.tiangolo.com/advanced/custom-response/#fileresponse).
