# AI-Based Academic Text Revision System

## 1. Introduction

Artificial intelligence tools are increasingly used to support academic writing. However, AI-assisted text can sometimes sound repetitive, generic, or structurally weak. This project presents a simple web-based system that helps users revise AI-assisted academic drafts by improving clarity, sentence flow, originality of expression, and citation awareness.

The system is designed as a first-version MVP. It focuses on meaningful rewriting rather than basic synonym replacement. The goal is to help users produce clearer and more natural academic writing while preserving the original meaning and encouraging responsible academic practice.

## 2. Project Objective

The objective of this project is to create a platform where users can paste academic text and receive a revised version that is clearer, more natural, and better structured.

The system aims to:

- Preserve the meaning of the original text.
- Improve sentence structure and flow.
- Support formal and semi-formal academic tone.
- Reduce repetitive or generic phrasing.
- Provide before-and-after comparison.
- Remind users to check citations for source-dependent claims.

The system does not guarantee bypassing plagiarism checkers or AI-detection tools. Instead, it supports ethical academic revision by improving writing quality and encouraging proper citation.

## 3. Core Features

### 3.1 Text Rewriting Engine

The rewriting engine receives user input and generates a revised version of the text. It focuses on deeper paraphrasing by changing sentence structure, improving word choice, and reorganizing ideas where appropriate.

Main functions include:

- Sentence polishing.
- Phrase improvement.
- Paragraph-level revision.
- Sentence reordering for better logical flow.
- Preservation of important academic meaning.

### 3.2 Humanization Layer

The system attempts to make the revised text sound more natural by improving rhythm and readability. It avoids making every sentence follow the same structure.

This includes:

- Mixing sentence lengths.
- Removing overly mechanical phrasing.
- Improving transitions between ideas.
- Supporting formal and semi-formal writing styles.

### 3.3 Similarity-Aware Revision

The system reduces surface-level similarity by using clearer structure and fresh phrasing. Instead of simply replacing words with synonyms, it revises how ideas are expressed.

This approach is more useful for academic writing because it improves the quality of the explanation rather than only changing individual words.

### 3.4 Before and After Comparison

The web interface shows the original text and revised text side by side. This allows users to compare both versions and decide whether the revision accurately reflects their intended meaning.

### 3.5 Quality Notes

After rewriting, the system provides quality notes. These notes explain what was improved, such as meaning preservation, flow improvement, and citation awareness.

### 3.6 Citation Reminder

The system includes an optional citation reminder. If the text appears to contain research-based claims, data, or evidence, the app reminds the user to verify and cite the relevant sources.

## 4. Technology Stack

The project uses a simple and extendable technology stack.

| Component | Technology |
|---|---|
| Backend | Python |
| Web Framework | FastAPI version included |
| Fallback Server | Python standard library HTTP server |
| Frontend | HTML, CSS, JavaScript |
| AI Integration | Optional OpenAI API |
| Data Format | JSON |

The project includes both a FastAPI backend and a no-dependency fallback server. This makes the app easier to run in environments where Python packages are not installed.

## 5. System Architecture

The system has three main layers:

1. Frontend interface
2. Backend API
3. Rewriting engine

The user enters text into the frontend. The frontend sends the text to the backend API. The backend passes the text to the rewriting engine. The rewriting engine returns a revised version, which is displayed in the browser.

### Architecture Flow

```text
User Input
   ↓
Web Interface
   ↓
Backend API
   ↓
Academic Rewriting Engine
   ↓
Revised Text + Quality Notes
   ↓
Before/After Display
```

## 6. Implementation Details

### 6.1 `server.py`

The `server.py` file provides a simple local server using Python's built-in HTTP server. It allows the app to run without installing external dependencies.

It handles:

- Serving the main HTML page.
- Serving CSS and JavaScript files.
- Receiving rewrite requests from the frontend.
- Returning revised text as JSON.

### 6.2 `app/rewriter.py`

The `rewriter.py` file contains the main rewriting logic. It includes a local fallback rewriting system and an optional OpenAI-based rewriting method.

The local fallback can:

- Split text into sentences.
- Improve selected phrases.
- Normalize sentence formatting.
- Reorganize sentences for better flow.
- Add citation reminders when needed.

If an OpenAI API key is provided, the system can use an AI model to produce stronger revisions.

### 6.3 `app/main.py`

The `main.py` file contains the FastAPI version of the backend. It defines the web app and the `/api/rewrite` endpoint.

This version is useful for future expansion because FastAPI makes it easier to add:

- User accounts.
- Database storage.
- Similarity scoring APIs.
- Authentication.
- Advanced AI model settings.

### 6.4 Frontend Files

The frontend consists of:

- `index.html`
- `styles.css`
- `app.js`

The frontend allows users to paste text, select tone, choose revision depth, enable citation reminders, and view the revised output.

## 7. Ethical Considerations

This system should be used as a revision assistant, not as a tool for academic dishonesty. The revised output should always be reviewed by the user.

Important ethical guidelines include:

- Do not submit revised text without understanding it.
- Cite all source-based ideas, facts, data, and quotations.
- Do not use the tool to hide plagiarism.
- Use the system to improve clarity and originality of expression.
- Follow the rules of the user's school, university, or institution.

AI-detection tools can be unreliable, so the system does not promise to bypass them. Instead, it focuses on improving academic writing quality in a responsible way.

## 8. Testing

The project was tested using a sample academic paragraph. The system successfully returned a revised version of the input text and provided quality notes.

Tested items:

- Python syntax compilation.
- Local rewriting engine.
- HTTP API response.
- Before-and-after output format.

The local fallback provider was verified successfully.

## 9. Limitations

The current MVP has some limitations:

- The local fallback rewriting engine is basic compared to a full AI model.
- It does not include a real plagiarism checker.
- It does not include an AI-detection score.
- It does not store user history.
- It does not include user login or authentication.
- Citation reminders are heuristic and should not replace manual checking.

## 10. Future Improvements

Future versions of the system could include:

- Integration with OpenAI or HuggingFace models.
- Similarity scoring API integration.
- Citation detection and reference suggestions.
- File upload support for `.docx`, `.pdf`, and `.txt`.
- User accounts and saved revision history.
- More tone options.
- Side-by-side sentence-level comparison.
- Export to Word or PDF.

## 11. Conclusion

This project provides a working MVP for an AI-based academic text revision system. It allows users to paste text, choose rewriting settings, and receive a clearer and more natural academic revision.

The system is simple, modular, and easy to extend. It demonstrates how Python, a web interface, and optional AI integration can be combined to support responsible academic writing improvement.
