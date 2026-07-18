import argparse
import json
from pathlib import Path

from datasets import Dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)


PROMPT_PREFIX = (
    "Rewrite the following academic text. Change the sentence structure, reduce repetitive phrasing, "
    "and make it sound natural while preserving the meaning.\nText: "
)


def load_pairs(path: Path) -> Dataset:
    rows = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            item = json.loads(line)
            rows.append(
                {
                    "source": PROMPT_PREFIX + item["source"].strip(),
                    "target": item["target"].strip(),
                }
            )
    if not rows:
        raise ValueError(f"No training rows found in {path}")
    return Dataset.from_list(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune a small academic humanizer model.")
    parser.add_argument("--data", default="training/data/sample_pairs.jsonl")
    parser.add_argument("--base-model", default="google/flan-t5-small")
    parser.add_argument("--output", default="training/models/academic-humanizer")
    parser.add_argument("--epochs", type=int, default=8)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--max-input-length", type=int, default=384)
    parser.add_argument("--max-output-length", type=int, default=256)
    args = parser.parse_args()

    dataset = load_pairs(Path(args.data))
    split = dataset.train_test_split(test_size=0.2 if len(dataset) > 5 else 0.01, seed=42)

    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.base_model)

    def tokenize(batch):
        model_inputs = tokenizer(
            batch["source"],
            max_length=args.max_input_length,
            truncation=True,
        )
        labels = tokenizer(
            text_target=batch["target"],
            max_length=args.max_output_length,
            truncation=True,
        )
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized = split.map(tokenize, batched=True, remove_columns=split["train"].column_names)
    collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output,
        learning_rate=3e-5,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        num_train_epochs=args.epochs,
        predict_with_generate=True,
        save_strategy="epoch",
        eval_strategy="epoch",
        logging_steps=10,
        report_to="none",
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        processing_class=tokenizer,
        data_collator=collator,
    )
    trainer.train()
    trainer.save_model(args.output)
    tokenizer.save_pretrained(args.output)
    print(f"Saved trained model to {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
