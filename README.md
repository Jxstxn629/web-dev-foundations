# Tutorial 2: Returning HTML from a GET Endpoint

Use the API from Tutorial 1 to serve a web page. You will learn how the response's content type tells the browser what it received, and how HTML becomes a rendered page.

**Time:** 20–30 minutes. **Prerequisites:** [Tutorial 1](https://github.com/Jxstxn629/web-dev-foundations/tree/tutorial-01-first-api), Python 3.10+, Git, and a text editor.

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

This branch contains the completed example. To follow the steps yourself, remove the HTMLResponse import and the /page endpoint from main.py, then add them back as you work.

The JSON endpoints from Tutorial 1 remain available. The main branch still contains only the repository overview.

## 2. Prepare the environment

If your virtual environment from Tutorial 1 already exists, activate it and install requirements. Otherwise create it first.

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

No new dependencies are needed for this lesson.

## 3. Choose an HTML response

In Tutorial 1, endpoints returned dictionaries as JSON. A browser can also receive HTML, which describes a document's structure.

Add this import to main.py:

```python
from fastapi.responses import HTMLResponse
```

Then add a new endpoint below the existing functions:

```python
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
        <p><a href="/hello?name=Ada">Compare with a JSON response</a></p>
    </main>
</body>
</html>"""
```

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

Open <http://127.0.0.1:8000/page>. Expect a heading, a paragraph, a three-item list, and a link. The browser tab should say **My First Web Page**.

Click the link. It sends a new GET request to /hello?name=Ada and displays the JSON greeting from Tutorial 1. Use your browser's Back button to return to the page.

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
| GET /hello?name=Ada | application/json | A greeting as structured data. |
| GET /page | text/html; charset=utf-8 | A document to render as a page. |
| GET /missing | application/json | A 404 error response. |

HTML and JSON both travel in HTTP responses. Choosing HTML for one endpoint does not change the other endpoints.

Open <http://127.0.0.1:8000/docs> and try GET /page. Inspect the response body and headers there, then visit /page directly to see normal browser rendering.

## 7. Practice

1. Change the heading and tab title. Save, reload, and confirm both changed.
2. Add an h2 heading called “What I learned” followed by a list of three points.
3. Add GET /about returning a complete HTML document with status 200. Give it an appropriate title and a link back to /page.
4. Add a link from /page to /about. Follow both links and inspect their GET requests.
5. Predict what happens if you remove response_class=HTMLResponse from /page. Try it, inspect the content type and response body, then restore it.

## Good habits

- Use GET to retrieve a page without changing server-side data.
- Match the response type to the content you return.
- Use descriptive function names, page titles, and semantic HTML elements.
- Keep user input out of raw HTML strings. If you later insert user text into an HTML text node, escape it; use templates with autoescaping as pages grow. Validation alone does not make text safe to embed in HTML.
- Keep this small example readable. Separating HTML into templates is a later step.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Browser shows a quoted string instead of a page | Check the HTMLResponse import and response_class on /page. |
| /page returns 404 | Check the URL, save main.py, and confirm you started the server from this lesson's directory. |
| Syntax error after editing HTML | Keep the opening and closing triple quotes intact. |
| Old page content appears | Save the file, check the reload logs, and refresh the browser. |
| Port already in use | Stop the earlier server with Ctrl+C, or use --port 8001 and update the URL. |

Stop the server with **Ctrl+C**. Run `deactivate` if you activated the environment.

## Completion checklist

- [ ] Explain why this endpoint uses HTMLResponse.
- [ ] Find the Content-Type header in browser developer tools.
- [ ] Distinguish HTML source from the rendered document.
- [ ] Create /about and navigate between the two pages.
- [ ] Confirm that the original JSON endpoints still work.

Further reading: [FastAPI HTML responses](https://fastapi.tiangolo.com/advanced/custom-response/#html-response).
