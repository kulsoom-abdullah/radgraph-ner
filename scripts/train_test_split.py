"""
This script splits the RadGraph dataset into train, validation, and test sets.
It can handle the following tasks:
1. Automatically convert a Hugging Face Dataset into JSONL format if it doesn't already exist.
2. Perform stratified splitting based on entity counts, ensuring better representation of rare entities.

Arguments:
    --input-file: Path to the input JSONL file.
    --output-dir: Directory where train/val/test splits will be saved.
    --stratify: Enable stratified splitting by entity counts (default: False).

Note:
- If some entity classes have fewer than 2 samples, stratification is automatically disabled.
- The splits are saved in the output directory as `train.jsonl`, `val.jsonl`, and `test.jsonl`.
"""
import os
import json
import logging
from sklearn.model_selection import train_test_split
from collections import Counter
from datasets import load_from_disk

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_reports(file_path):
    """Load reports from a JSONL file."""
    with open(file_path, "r") as f:
        return [json.loads(line) for line in f]

def save_splits(train, val, test, output_dir):
    """Save train, val, test splits as JSONL files."""
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/train.jsonl", "w") as f:
        for entry in train:
            f.write(json.dumps(entry) + "\n")
    logging.info(f"Train split saved to {output_dir}/train.jsonl")
    with open(f"{output_dir}/val.jsonl", "w") as f:
        for entry in val:
            f.write(json.dumps(entry) + "\n")
    logging.info(f"Validation split saved to {output_dir}/val.jsonl")
    with open(f"{output_dir}/test.jsonl", "w") as f:
        for entry in test:
            f.write(json.dumps(entry) + "\n")
    logging.info(f"Test split saved to {output_dir}/test.jsonl")

def create_jsonl(jsonl_file):
    """Create a JSONL file from the Hugging Face Dataset."""
    if not os.path.exists(jsonl_file):
        logging.info(f"{jsonl_file} does not exist. Creating it...")
        dataset = load_from_disk("data/processed/")
        dataset.to_json(jsonl_file)
        logging.info(f"Dataset saved as JSONL to '{jsonl_file}'")
    else:
        logging.info(f"{jsonl_file} already exists. Skipping creation.")

def main(input_file, output_dir, stratify=False):
    """Split dataset into train/val/test."""
    create_jsonl(input_file)  # Ensure JSONL file is created if it doesn't exist

    reports = load_reports(input_file)

    # Count entity labels
    label_counts = Counter()
    rare_reports = []
    for report in reports:
        for label in report["labels"]:
            label_type = label["label"]
            label_counts[label_type] += 1
            # Handle rare class
            if label_type == "Observation::measurement::definitely absent":
                rare_reports.append(report)

    # Log class counts
    logging.info("Class Counts (Entity Types):")
    for label, count in label_counts.items():
        logging.info(f"{label}: {count}")

    # Remove rare reports from main dataset
    reports = [r for r in reports if r not in rare_reports]

    # Stratify only if feasible
    stratify_labels = None
    if stratify:
        stratify_labels = [len(report["labels"]) for report in reports]
        if min(stratify_labels) < 2:
            logging.warning("Some classes have fewer than 2 samples. Stratification disabled.")
            stratify_labels = None

    # Split remaining reports
    train, temp = train_test_split(reports, test_size=0.2, stratify=stratify_labels, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, stratify=None, random_state=42)

    # Add rare reports to test set
    test.extend(rare_reports)
    logging.info(f"Rare class reports added to test set: {len(rare_reports)}")

    save_splits(train, val, test, output_dir)
    logging.info(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")

