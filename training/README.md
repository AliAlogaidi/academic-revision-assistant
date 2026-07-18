# Training Your Own Academic Humanizer Model

This folder contains a starter pipeline for training a small text-to-text model.

The goal is academic style transfer:

- Input: rough, repetitive, or AI-like academic draft.
- Output: clearer, more natural, more readable academic revision.

It should not be presented as a guarantee for AI-detector scores.

## 1. Dataset Format

Add examples to:

```text
training/data/sample_pairs.jsonl
```

Each line must be JSON:

```json
{"source": "rough text here", "target": "human revised text here"}
```

For a real model, collect at least:

- 100 examples for a basic class demo.
- 500-1000 examples for better results.
- 3000+ examples for stronger style consistency.

## 2. Install Dependencies

```powershell
pip install transformers datasets torch sentencepiece accelerate
```

## 3. Train

```powershell
python training/train_humanizer.py --data training/data/sample_pairs.jsonl --epochs 8
```

The model will be saved to:

```text
training/models/academic-humanizer
```

## 4. Test The Model

```powershell
python training/generate.py --text "Artificial intelligence is very important because it helps students write faster but the text can sound robotic."
```

## 5. Presentation Explanation

You can say:

> We moved from only using an external API to designing our own trainable model. The model uses paired examples: an AI-like academic sentence as input and a more natural revised version as output. This allows the system to learn rewriting patterns such as sentence restructuring, smoother transitions, and less repetitive phrasing.
