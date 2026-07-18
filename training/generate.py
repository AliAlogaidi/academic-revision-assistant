import argparse
from pathlib import Path

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


PROMPT_PREFIX = (
    "Rewrite the following academic text. Change the sentence structure, reduce repetitive phrasing, "
    "and make it sound natural while preserving the meaning.\nText: "
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a revision with a trained humanizer model.")
    parser.add_argument("--model", default="training/models/academic-humanizer")
    parser.add_argument("--text")
    parser.add_argument("--file")
    parser.add_argument("--max-length", type=int, default=384)
    parser.add_argument("--min-length", type=int, default=80)
    args = parser.parse_args()

    if not args.text and not args.file:
        raise SystemExit("Use --text \"...\" or --file path/to/input.txt")

    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8").strip()

    model_path = Path(args.model)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    inputs = tokenizer(PROMPT_PREFIX + text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(
        **inputs,
        max_new_tokens=args.max_length,
        min_new_tokens=args.min_length,
        do_sample=False,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3,
        encoder_no_repeat_ngram_size=4,
        repetition_penalty=1.5,
    )
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))


if __name__ == "__main__":
    main()
