# AI-Based Academic Text Revision Assistant

**Student Name:** ___________________________  
**Course:** _________________________________  
**Instructor:** ______________________________  
**Date:** _________________________________  

---

## Abstract

This report presents an AI-based academic text revision assistant designed to improve the quality, clarity, and originality of academic writing. The system allows users to paste a draft into a web interface and receive a revised version that improves sentence structure, flow, tone, and readability while preserving the original meaning. The project was developed as a simple minimum viable product using Python for the backend and HTML, CSS, and JavaScript for the frontend. The system also includes an optional AI integration and a local fallback rewriting engine. The main purpose of the project is to support responsible academic revision, not to encourage plagiarism or misuse of AI tools.

## 1. Introduction

Artificial intelligence tools are increasingly used in academic writing. These tools can help students organize ideas, improve grammar, and produce drafts more quickly. However, AI-generated text often has weaknesses such as repetitive sentence patterns, generic expressions, unnatural flow, and unclear structure. These weaknesses can reduce the quality of academic writing and make the text less original or less convincing.

The project described in this report aims to address these issues by creating a simple web application that revises AI-assisted academic text. The system focuses on improving writing quality through meaningful rewriting rather than simple synonym replacement. It supports academic users by helping them produce clearer, more natural, and better-structured text.

## 2. Project Objective

The main objective of this project is to build a platform that takes academic text as input and produces an improved version as output. The system is designed to revise text in a way that preserves the original meaning while improving clarity, sentence structure, and academic tone.

The specific objectives are:

- To improve the readability and flow of academic text.
- To rewrite sentences using clearer and more natural structures.
- To preserve the main meaning and important terminology of the original text.
- To support formal and semi-formal academic tones.
- To provide a simple before-and-after comparison.
- To remind users about proper citation when the text contains source-based claims.

## 3. Problem Statement

Many students use AI tools to generate or improve academic writing. Although these tools can be useful, the generated text may not always meet academic standards. It may sound mechanical, lack originality of expression, or fail to present ideas in a logical order. In addition, students may rely too heavily on AI-generated output without reviewing, understanding, or properly citing the information.

Therefore, there is a need for a simple system that helps users revise AI-assisted text responsibly. The system should improve the quality of the writing while encouraging academic integrity.

## 4. System Overview

The developed system is a web-based application. Users paste their text into a text box, choose a tone and revision depth, and then submit the text for revision. The system processes the input and displays the original and revised versions side by side.

The application includes three main parts:

1. A frontend web interface.
2. A Python backend server.
3. A rewriting engine.

The frontend is responsible for collecting user input and displaying the output. The backend receives the request and sends it to the rewriting engine. The rewriting engine revises the text and returns the improved version with quality notes.

## 5. Main Features

### 5.1 Text Rewriting Engine

The text rewriting engine is the core part of the system. It improves the input text by modifying sentence structure, improving word choice, and reorganizing ideas where needed. The system is designed to perform meaningful rewriting instead of only replacing words with synonyms.

### 5.2 Tone Selection

The system supports two tone options:

- Formal
- Semi-formal

This allows the user to choose the writing style that best fits the academic context.

### 5.3 Revision Depth

The system includes different levels of revision. A lighter revision makes smaller changes, while a stronger revision makes more noticeable structural improvements. This makes the system more flexible for different writing needs.

### 5.4 Before and After Comparison

The web interface displays the original text and the revised text side by side. This helps users compare the two versions and check whether the revised version still reflects the intended meaning.

### 5.5 Quality Notes

After revision, the system provides quality notes that explain the type of improvements made. These notes may include meaning preservation, flow improvement, and citation reminders.

### 5.6 Citation Reminder

The system includes a citation reminder feature. If the text appears to contain research-based claims, evidence, statistics, or source-dependent information, the system reminds the user to verify and cite the relevant sources.

## 6. Technology Used

The project was built using a simple and practical technology stack.

| Component | Technology |
|---|---|
| Backend Language | Python |
| Backend Framework | FastAPI |
| Fallback Server | Python built-in HTTP server |
| Frontend | HTML, CSS, JavaScript |
| Data Exchange | JSON |
| Optional AI Provider | OpenAI API |

Python was chosen because it is widely used in AI and backend development. The frontend technologies were chosen because they are simple, lightweight, and suitable for an MVP.

## 7. System Architecture

The system follows a simple client-server architecture. The user interacts with the web interface in the browser. When the user submits text, the frontend sends a request to the backend API. The backend processes the request using the rewriting engine and sends the revised text back to the frontend.

```text
User
  ↓
Web Interface
  ↓
Backend Server
  ↓
Rewriting Engine
  ↓
Revised Text and Quality Notes
  ↓
Browser Output
```

This architecture makes the system easy to understand, test, and extend in the future.

## 8. Implementation

### 8.1 Backend Implementation

The backend was implemented in Python. The project includes a FastAPI version for modern API development and a simple fallback server using Python's built-in HTTP server. The fallback server allows the application to run even if external packages are not installed.

The backend handles:

- Loading the web page.
- Serving CSS and JavaScript files.
- Receiving text from the frontend.
- Sending the text to the rewriting engine.
- Returning the revised text as JSON.

### 8.2 Rewriting Engine

The rewriting engine is implemented in the `app/rewriter.py` file. It contains the logic for revising text. The local fallback engine can split the text into sentences, improve selected expressions, normalize formatting, reorganize sentences, and add citation reminders.

The system also supports optional integration with an AI model if an OpenAI API key is provided. This makes the project extendable and allows stronger rewriting quality in future versions.

### 8.3 Frontend Implementation

The frontend was created using HTML, CSS, and JavaScript. It provides a clean interface where users can enter text, select tone and revision depth, and view the revised result.

The frontend sends the input text to the backend using a JSON request and then displays the revised output on the page.

## 9. Testing and Results

The system was tested using a sample academic paragraph about artificial intelligence in education. The application successfully accepted the input text, processed it through the rewriting engine, and returned a revised version.

The following parts were tested:

- Python syntax compilation.
- Local rewriting engine.
- HTTP API request and response.
- Before-and-after output display.
- Quality notes generation.

The test confirmed that the MVP works correctly as a basic academic revision assistant.

## 10. Ethical Considerations

This system is intended to support academic writing improvement, not academic dishonesty. It should not be used to hide plagiarism or submit work without understanding it.

Users should follow these ethical guidelines:

- Review the revised text before submitting it.
- Make sure the final work reflects their own understanding.
- Cite all borrowed ideas, facts, data, and quotations.
- Follow the academic rules of their institution.
- Use AI as a support tool, not as a replacement for learning.

The system does not guarantee that text will pass plagiarism checkers or AI-detection tools. Its purpose is to improve clarity, originality of expression, and academic quality in a responsible way.

## 11. Limitations

The current version is an MVP and has several limitations:

- The local rewriting engine is simpler than a full AI model.
- It does not include a real plagiarism detection system.
- It does not include AI-detection scoring.
- It does not save user history.
- It does not support file uploads.
- Citation reminders are basic and should not replace manual source checking.

These limitations can be addressed in future versions.

## 12. Future Work

Future improvements may include:

- Integration with advanced AI models.
- Plagiarism similarity scoring.
- AI-detection risk analysis.
- File upload support for Word and PDF documents.
- Exporting revised text to Word or PDF.
- User accounts and saved revision history.
- More academic tone options.
- Sentence-level comparison between original and revised text.
- Better citation detection and reference suggestions.

## 13. Conclusion

This project successfully demonstrates a simple AI-based academic text revision assistant. The system allows users to paste academic text, revise it through a web interface, and compare the original and improved versions. It focuses on improving clarity, structure, tone, and responsible originality.

The project is modular and easy to extend. It provides a strong foundation for future development, including advanced AI integration, similarity checking, citation support, and document export features. Overall, the system shows how AI can be used responsibly to support academic writing improvement.

## References

FastAPI Documentation. (n.d.). *FastAPI framework documentation*. https://fastapi.tiangolo.com/

OpenAI. (n.d.). *OpenAI API documentation*. https://platform.openai.com/docs/

Python Software Foundation. (n.d.). *Python documentation*. https://docs.python.org/
