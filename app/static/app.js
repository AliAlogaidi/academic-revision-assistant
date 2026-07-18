const form = document.querySelector("#rewriteForm");
const sourceText = document.querySelector("#sourceText");
const tone = document.querySelector("#tone");
const depth = document.querySelector("#depth");
const citationNotes = document.querySelector("#citationNotes");
const submitButton = document.querySelector("#submitButton");
const clearButton = document.querySelector("#clearButton");
const copyButton = document.querySelector("#copyButton");
const providerStatus = document.querySelector("#providerStatus");
const beforeText = document.querySelector("#beforeText");
const afterText = document.querySelector("#afterText");
const beforeCount = document.querySelector("#beforeCount");
const afterCount = document.querySelector("#afterCount");
const qualityNotes = document.querySelector("#qualityNotes");
const integrityNote = document.querySelector("#integrityNote");
const summaryBadge = document.querySelector("#summaryBadge");

function countWords(value) {
  const words = value.trim().match(/\S+/g);
  return words ? words.length : 0;
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  clearButton.disabled = isLoading;
  submitButton.textContent = isLoading ? "Revising..." : "Revise Text";
  providerStatus.textContent = isLoading ? "Working" : "Ready";
}

function renderNotes(notes) {
  qualityNotes.innerHTML = "";
  notes.forEach((note) => {
    const item = document.createElement("li");
    item.className = "note-item";
    const label = document.createElement("strong");
    label.textContent = `${note.label}: `;
    item.append(label, note.detail);
    qualityNotes.appendChild(item);
  });
}

function resetWorkspace() {
  sourceText.value = "";
  beforeText.textContent = "Your original text will appear here.";
  afterText.textContent = "The revised version will appear here.";
  beforeCount.textContent = "0 words";
  afterCount.textContent = "0 words";
  providerStatus.textContent = "Ready";
  summaryBadge.textContent = "Waiting for text";
  integrityNote.textContent = "";
  qualityNotes.innerHTML = "<li>Submit a draft to generate revision notes.</li>";
}

clearButton.addEventListener("click", resetWorkspace);

copyButton.addEventListener("click", async () => {
  const value = afterText.textContent.trim();
  if (!value || value === "The revised version will appear here.") {
    return;
  }
  await navigator.clipboard.writeText(value);
  copyButton.textContent = "Copied";
  window.setTimeout(() => {
    copyButton.textContent = "Copy Revised";
  }, 1200);
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = sourceText.value.trim();
  beforeText.textContent = text;
  beforeCount.textContent = `${countWords(text)} words`;
  afterText.textContent = "";
  afterCount.textContent = "0 words";
  setLoading(true);

  try {
    const response = await fetch("/api/rewrite", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        tone: tone.value,
        depth: depth.value,
        include_citation_notes: citationNotes.checked,
      }),
    });

    if (!response.ok) {
      throw new Error("The draft could not be revised.");
    }

    const data = await response.json();
    afterText.textContent = data.revised;
    afterCount.textContent = `${countWords(data.revised)} words`;
    providerStatus.textContent = data.provider;
    summaryBadge.textContent = "Revision complete";
    renderNotes(data.quality_notes);
    integrityNote.textContent = data.academic_integrity_note;
  } catch (error) {
    providerStatus.textContent = "Error";
    summaryBadge.textContent = "Check input";
    afterText.textContent = error.message;
  } finally {
    submitButton.disabled = false;
    clearButton.disabled = false;
    submitButton.textContent = "Revise Text";
  }
});
