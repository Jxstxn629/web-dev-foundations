const form = document.querySelector("#note-form");
const fields = document.querySelector("#note-fields");
const submitButton = document.querySelector("#submit-button");
const formStatus = document.querySelector("#form-status");
const listStatus = document.querySelector("#list-status");
const notesList = document.querySelector("#notes-list");
const refreshButton = document.querySelector("#refresh-button");

const inputs = {
    title: document.querySelector("#title"),
    content: document.querySelector("#content"),
};
const errors = {
    title: document.querySelector("#title-error"),
    content: document.querySelector("#content-error"),
};

function clearErrors() {
    for (const name of Object.keys(inputs)) {
        errors[name].textContent = "";
        inputs[name].removeAttribute("aria-invalid");
    }
}

function showValidationErrors(details) {
    let firstInvalid = null;
    for (const error of details) {
        const name = error.loc?.[1];
        if (Object.hasOwn(inputs, name)) {
            errors[name].textContent = error.msg;
            inputs[name].setAttribute("aria-invalid", "true");
            firstInvalid ??= inputs[name];
        }
    }
    return firstInvalid;
}

function renderNotes(notes) {
    notesList.replaceChildren();
    for (const note of notes) {
        const item = document.createElement("li");
        const heading = document.createElement("h3");
        const content = document.createElement("p");
        // Display user text as text, never as executable HTML.
        heading.textContent = note.title;
        content.textContent = note.content || "(No content)";
        item.append(heading, content);
        notesList.append(item);
    }
}

async function loadNotes() {
    refreshButton.disabled = true;
    listStatus.textContent = "Loading notes…";
    try {
        const response = await fetch("/notes");
        if (!response.ok) {
            listStatus.textContent = "Could not load notes (HTTP " + response.status + "). Try Refresh notes.";
            return;
        }
        const notes = await response.json();
        renderNotes(notes);
        listStatus.textContent = notes.length ? notes.length + " note(s)." : "No notes yet. Create your first note.";
    } catch {
        listStatus.textContent = "Could not load notes. Check the server and your connection, then refresh.";
    } finally {
        refreshButton.disabled = false;
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (fields.disabled) return;

    clearErrors();
    const payload = {title: inputs.title.value, content: inputs.content.value};
    fields.disabled = true;
    submitButton.textContent = "Saving…";
    formStatus.textContent = "Saving your note…";
    let firstInvalid = null;

    try {
        const response = await fetch("/notes", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(payload),
        });

        if (response.status === 422) {
            const result = await response.json();
            firstInvalid = showValidationErrors(result.detail);
            formStatus.textContent = "Please correct the highlighted fields and try again.";
            return;
        }
        if (!response.ok) {
            formStatus.textContent = "Save failed (HTTP " + response.status + "). Refresh notes before retrying.";
            return;
        }

        const result = await response.json();
        formStatus.textContent = result.message + ": " + result.data.title;
        form.reset();
        // A failed list refresh must not turn a successful save into a failed save.
        await loadNotes();
    } catch {
        formStatus.textContent = "Could not confirm the save. Check the server and your connection, then refresh notes before retrying.";
    } finally {
        fields.disabled = false;
        submitButton.textContent = "Create note";
        firstInvalid?.focus();
    }
});

refreshButton.addEventListener("click", loadNotes);
loadNotes();
