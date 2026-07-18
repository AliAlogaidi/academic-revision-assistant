# Academic Revision Assistant

A small FastAPI MVP for revising AI-assisted academic drafts. It focuses on clarity,
structure, originality, tone control, and citation hygiene. It does not promise to
bypass plagiarism or AI-detection systems.

## Features

- Paste text and choose formal or semi-formal academic tone.
- Optional rewrite goals: structure, natural flow, concision, and citation reminders.
- Before/after comparison with simple quality notes.
- Optional OpenAI provider through `OPENAI_API_KEY`.
- Local fallback rewriter so the app runs without an API key.

## Run

No-dependency local demo:

```powershell
python server.py
```

FastAPI version:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000`.

## Deploy Online

The app is ready to deploy as a Python web service.

Use this start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

For Render:

1. Upload the project to GitHub.
2. Create a new Render Web Service.
3. Select the GitHub repository.
4. Build command:

```bash
pip install -r requirements.txt
```

5. Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

6. Add environment variables in Render:

```text
TOHUMAN_API_TOKEN=your_real_token
TOHUMAN_INTENSITY=aggressive
```

Do not upload `.env` publicly.

## Optional ToHuman API

If you have a ToHuman API token, set it in your environment before running the app:

```powershell
$env:TOHUMAN_API_TOKEN="your_token_here"
$env:TOHUMAN_INTENSITY="medium"
python server.py
```

Keep the token in the backend only. Do not put it in `app/static/app.js` or any browser file.

## Training A Custom Humanizer

The project also includes a starter training pipeline in `training/`.

It uses paired examples:

- `source`: rough or AI-like academic text
- `target`: clearer, more natural academic revision

Start with:

```powershell
pip install -r training/requirements-training.txt
python training/train_humanizer.py --data training/data/sample_pairs.jsonl --epochs 8
```

Then test:

```powershell
python training/generate.py --text "Paste a rough academic sentence here."
```

For a real project result, expand `training/data/sample_pairs.jsonl` with many more examples.

## API

`POST /api/rewrite`

```json
{
  "text": "Paste draft text here.",
  "tone": "formal",
  "depth": "balanced",
  "include_citation_notes": true
}
```

## Academic Integrity

Use the output as a revision aid. Review claims, cite source ideas, and keep any
discipline-specific terminology that must remain unchanged.
