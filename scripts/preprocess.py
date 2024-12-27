from radgraph.data.preprocess import prepare_dataset

if __name__ == "__main__":
    # Paths to the raw JSON files
    json_files = ["data/raw/section_findings.json", "data/raw/section_impression.json"]

    # Prepare dataset
    dataset = prepare_dataset(json_files)

    # Save to processed directory
    dataset.save_to_disk("data/processed/")
    print("Dataset saved to data/processed/")
