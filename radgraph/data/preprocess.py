import json

from datasets import Dataset

from radgraph.utils.tokenizer import load_tokenizer, tokenize_texts


def load_json(file_path):
    """Loads JSON data from a file."""
    with open(file_path, "r") as f:
        return json.load(f)


def prepare_dataset(json_files):
    """Converts raw RadGraph JSON files into a Hugging Face Dataset."""
    examples = []
    for file_path in json_files:
        with open(file_path, "r") as f:
            data = json.load(f)  # Load the list of dictionaries
            for report in data:
                for key, content in report.items():
                    text = content["text"]
                    entities = content["entities"]  # Dictionary of entities

                    labels = [
                        {
                            "tokens": entity["tokens"],
                            "label": entity["label"],
                            "start_ix": entity["start_ix"],
                            "end_ix": entity["end_ix"],
                            "relations": entity["relations"],
                        }
                        for entity in entities.values()
                    ]

                    # Append processed data
                    examples.append({"text": text, "labels": labels})

    return Dataset.from_list(examples)


def prepare_tokenized_dataset(dataset, model_name="distilbert-base-uncased"):
    """
    Tokenizes a Hugging Face Dataset for NER training.

    Args:
        dataset (Dataset): Hugging Face Dataset object.
        model_name (str): Name of the Hugging Face model for the tokenizer.

    Returns:
        Dataset: Tokenized dataset.
    """
    tokenizer = load_tokenizer(model_name)

    def tokenize_function(example):
        return tokenize_texts([example["text"]], tokenizer)

    # Apply tokenization to the dataset
    return dataset.map(tokenize_function, batched=True)
