# Tutorial 4: Connecting an HTML Form to Your API

Build a small notes application: enter a note in an HTML form, send JSON to a Python API, and display the result without navigating away.

**Standalone:** no earlier tutorial is required. **Time:** 45–60 minutes. **Prerequisites:** Python 3.10+, Git, a browser, a text editor, and basic familiarity with Python functions/classes and HTML. The JavaScript concepts used here are explained below.

## 1. Get the complete starter project

```sh
git clone --branch tutorial-04-html-form-api https://github.com/Jxstxn629/web-dev-foundations.git
cd web-dev-foundations
```

If already cloned, save or commit your changes, stop any running server, then run:

```sh
git fetch origin
git switch tutorial-04-html-form-api
```

The branch includes a working backend and the completed frontend, including the extension. Run it first, then follow the steps to understand and modify each part. You do not need to copy files from another tutorial.

```text
main.py             Python server and API
requirements.txt    Python dependencies
pages/index.html    Form and notes list
static/app.js       Browser events, API calls, and rendering
static/styles.css   Basic page styling
```

## 2. Install and run

Create an isolated Python environment. If .venv already exists, skip creating it.

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

Leave the terminal running. Open <http://127.0.0.1:8000/>. Open the page through the server, rather than double-clicking the HTML file.

FastAPI handles HTTP routes, Uvicorn runs the server, and Pydantic validates data. main:app selects app in main.py. The reload option is for local development.

## 3. Understand the page and API

The browser is the client. It first requests the HTML page, then its JavaScript and CSS. JavaScript sends further requests to the same server.

| Request | Result |
| --- | --- |
| GET / | HTML form and notes list. |
| GET /static/app.js | Browser JavaScript. |
| GET /static/styles.css | Page styling. |
| POST /notes | Creates a note; returns JSON with status 201. |
| GET /notes | Returns a JSON list with status 200. |
| GET /docs | Interactive API documentation. |

In main.py, FileResponse serves the HTML file. StaticFiles exposes only the static directory. Both use paths based on main.py so file locations do not depend on your terminal's directory.

The form sends:

```json
{"title": "My first note", "content": "Hello from the browser."}
```

The API returns:

```json
{
  "message": "Note created",
  "data": {
    "id": "a-server-generated-UUID",
    "title": "My first note",
    "content": "Hello from the browser."
  }
}
```

The id is a placeholder above. GET /notes returns an array of these note objects, without the message/data wrapper.

NoteCreate is the request model: title is required, trimmed, and limited to 1–100 characters; content defaults to an empty string and is limited to 1,000 characters. Unexpected fields are rejected. NoteResponse and NoteCreatedResponse define the public output.

Notes live in temporary, process-local memory. Restarting or reloading the server clears them. Use a single server process for this lesson.

## 4. Read the HTML form

Open pages/index.html. Notice:

- A label's for attribute matches its input's id.
- name identifies the field; id lets JavaScript find the element.
- required and maxlength provide browser-side checks.
- aria-describedby connects an input to its hint and error message.
- The submit button sends the form's submit event.
- role="status" makes status updates available to assistive technology.
- The script uses defer, so it runs after the document has been parsed.

The fieldset groups the inputs and button. We will disable the group during a save in the extension.

Browser checks improve feedback, but the server still validates every request. A client can bypass HTML constraints.

## 5. Send the form using fetch

Open static/app.js. document.querySelector selects an element; the variables at the top hold the elements needed by the script.

The submit handler uses this pattern, shown here as an excerpt of the completed handler:

```javascript
event.preventDefault();

const payload = {
    title: inputs.title.value,
    content: inputs.content.value,
};

const response = await fetch("/notes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
});
```

preventDefault stops normal form navigation. JSON.stringify turns a JavaScript object into JSON text. Content-Type tells the server what the body contains.

fetch starts an HTTP request and returns a promise: a value that becomes available later. An async function can use await to wait for that value without blocking the whole browser.

The relative URL /notes uses the page's current server. Since the page and API share the same scheme, host, and port (the same origin), no CORS configuration is needed.

This is a JSON submission. A normal HTML form submission uses a different encoding; it would need a corresponding backend parser.

## 6. Display success and field errors

fetch does not throw just because the server returns an HTTP error. Check response.status or response.ok.

The completed handler has three HTTP branches:

1. For 422, parse the validation response and show errors.
2. For another unsuccessful status, show a general failure message.
3. For success, parse the response, show result.message and result.data.title, reset the form, and load the notes list.

response.json() asynchronously parses JSON into a JavaScript value.

A validation error includes a location such as ["body", "title"]. showValidationErrors uses that field name to set the appropriate error paragraph's textContent and aria-invalid attribute. After the inputs are re-enabled, the first invalid field receives focus.

Try a title containing only spaces. Browser required validation accepts nonempty spaces, but the API trims them and returns 422. You should see a title error beside the input. Correct the title and resubmit; old errors should clear.

## 7. Fetch and render the notes list

loadNotes runs when the page opens, after a successful save, and when you click **Refresh notes**.

It fetches GET /notes, checks the status, reads the JSON array, and passes it to renderNotes. That function creates li, h3, and p elements for each note.

User-provided titles and content are assigned with textContent. This treats them as text. Using innerHTML for untrusted content could turn a note into executable markup.

Try a title such as <b>Hello</b>. The list should display the angle brackets literally, rather than rendering bold HTML.

## 8. Extension: loading states and network failures

The completed script already includes this extension. Trace these parts and experiment with them:

- Before the POST, disable the fieldset and change the button to “Saving…”.
- A guard ignores a second submit event while that fieldset is disabled.
- Use try/catch for network failures and unreadable responses.
- Use finally to re-enable the controls and restore the button label on success or failure.
- Keep the entered text when a save fails; reset it only after a confirmed successful response.
- Handle a failed list refresh separately from a successful POST.

Disabling the form prevents repeated submissions from this page while its request is running. It is not server-side deduplication.

A network failure can happen after the server saves a note but before the browser receives the response. The UI therefore says it could not confirm the save and asks you to refresh notes before retrying.

### Try the failure paths

1. Open the page while the server is running.
2. Stop the server with Ctrl+C.
3. Enter a note and submit. Expect a connection message; your input remains and the form becomes enabled again.
4. Restart the server and click Refresh notes. The list is empty because this lesson uses memory.
5. In browser developer tools, choose a slow network preset. Submit and observe the disabled inputs and “Saving…” button until the request finishes.
6. Return network settings to normal.

HTTP errors and network errors are different: 422 is a response from the server; a connection failure may provide no response at all.

## 9. Check the full flow

Open developer tools and choose Network. Submit a valid note and inspect:

| Check | Expected result |
| --- | --- |
| POST request body | JSON containing title and content. |
| POST response | 201, application/json, and message/data fields. |
| Following GET /notes | 200 and an array including the new note. |
| Page navigation | The document stays open; the form and list update in place. |
| Blank title | Browser blocks submission. |
| Spaces-only title | Server returns 422 and a field error appears. |
| Refresh notes | Existing server notes are fetched again. |
| Text containing HTML tags | Displayed literally in the list. |

For a server-side length check, use /docs to send 101 title characters; the HTML input normally prevents typing that many.

## 10. Practice

1. Add a character counter beneath content and update it on the input event.
2. Add an optional category to the request model, response model, HTML form, JSON payload, and displayed note. Keep the validation-error mapping in sync.
3. Add a GET list response model with a data array, then update loadNotes to read it. Explain why frontend and backend response contracts must agree.
4. Add a visible “Last refreshed” timestamp only after a successful list load.
5. Explain why automatically retrying a failed POST can create duplicate notes.

## Good habits

- Keep markup, browser behavior, and server rules in their own files.
- Validate on the server even when HTML performs checks.
- Check HTTP statuses and handle network failures.
- Display user data with textContent.
- Preserve input when a request fails.
- Distinguish a failed refresh from a failed save.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| Form does nothing | Check the browser console and ensure /static/app.js loads. JavaScript must be enabled. |
| Fetch fails or page opened as file:// | Open http://127.0.0.1:8000/ through the running server. |
| No module named fastapi or uvicorn | Install requirements with the same environment's Python used to run the server. |
| Static directory does not exist | Keep the supplied static folder beside main.py. |
| Old JavaScript runs | Hard-refresh the browser after editing static/app.js. |
| Port already in use | Stop the other server, or add --port 8001 and open that address. |
| Notes disappear after editing Python | Development reload restarted the server and cleared memory. |

Stop the server with **Ctrl+C**. Run deactivate if you activated the environment.

## Completion checklist

- [ ] Submit the form as JSON without leaving the page.
- [ ] Read the nested success response.
- [ ] Show server validation errors beside the matching fields.
- [ ] Load and render notes safely.
- [ ] Restore controls after both success and failure.
- [ ] Explain same-origin requests and temporary server storage.

Further reading: [MDN: Using Fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch), [FastAPI request bodies](https://fastapi.tiangolo.com/tutorial/body/), and [response models](https://fastapi.tiangolo.com/tutorial/response-model/).
