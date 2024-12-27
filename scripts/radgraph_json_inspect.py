import json
from pathlib import Path
from typing import Dict, List


def get_text_span(text: str, start_ix: int, end_ix: int) -> str:
    """Extract text span from the full text using token indices."""
    words = text.split()
    if start_ix == end_ix:
        return words[start_ix] if 0 <= start_ix < len(words) else "Index out of range"
    else:
        span = (
            words[start_ix : end_ix + 1] if 0 <= start_ix <= end_ix < len(words) else []
        )
        return " ".join(span)


def load_radgraph_file(file_path: str) -> List[Dict]:
    """
    Load and parse a RadGraph JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        List of dictionaries containing the RadGraph annotations
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # Print first entry structure for debugging
        if data and len(data) > 0:
            print(f"\nFirst entry structure in {Path(file_path).name}:")
            first_report = data[0]["0"]  # Access the nested report
            print("Fields available:", list(first_report.keys()))
            print("\nExample text:", first_report["text"][:100], "...")
            if "entities" in first_report:
                print(
                    f"Number of entities in 1st report: {len(first_report['entities'])}"
                )
                # Print example entity structure
                first_entity = next(iter(first_report["entities"].values()))
                print("Example entity structure:", first_entity)

        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return []
    except Exception as e:
        print(f"Error loading file {file_path}: {str(e)}")
        return []


def format_report_sample(data: List[Dict], num_samples: int = 1) -> str:
    """
    Format a sample of RadGraph reports with their annotations as a string.

    Args:
        data: List of RadGraph annotations
        num_samples: Number of samples to display

    Returns:
        Formatted string containing the report samples
    """
    if not data:
        return "No data to display"

    output = []
    for i, report_wrapper in enumerate(data[:num_samples]):
        report = report_wrapper["0"]  # Access the nested report
        text = report["text"]

        output.append(f"\n{'='*80}")
        output.append(f"Report #{i+1}:")

        # Extract and format text
        output.append("\nText:")
        output.append(text)

        # Extract and format entities
        output.append("\nEntities:")
        entities = report.get("entities", {})
        if not entities:
            output.append("No entities found")
        else:
            # Convert entities dict to list for easier handling
            entity_list = [
                {**entity, "id": entity_id} for entity_id, entity in entities.items()
            ]
            # Sort entities by start position for readability
            entity_list.sort(key=lambda x: int(x.get("start_ix", 0)))

            for entity in entity_list:
                entity_id = entity.get("id", "unknown")
                output.append(f"\n- Entity {entity_id}:")
                output.append(f"  Label: {entity.get('label', 'No label')}")

                # Extract actual text span
                start_ix = int(entity.get("start_ix", -1))
                end_ix = int(entity.get("end_ix", -1))
                span_text = get_text_span(text, start_ix, end_ix)

                output.append(f"  Text: {span_text}")
                output.append(f"  Start: {start_ix}")
                output.append(f"  End: {end_ix}")

                # Add tokens if available
                tokens = entity.get("tokens", [])
                if tokens:
                    output.append(f"  Tokens: {', '.join(tokens)}")

        # Extract and format relations
        relations = report.get("relations", {})
        if relations:
            output.append("\nRelations:")
            for rel_id, relation in relations.items():
                output.append(f"\n- Relation {rel_id}:")
                output.append(f"  Type: {relation.get('type', 'No type')}")

                # Get source and target entity texts
                source_id = relation.get("source")
                target_id = relation.get("target")

                if source_id in entities and target_id in entities:
                    source_entity = entities[source_id]
                    target_entity = entities[target_id]

                    source_text = get_text_span(
                        text,
                        int(source_entity.get("start_ix", -1)),
                        int(source_entity.get("end_ix", -1)),
                    )
                    target_text = get_text_span(
                        text,
                        int(target_entity.get("start_ix", -1)),
                        int(target_entity.get("end_ix", -1)),
                    )

                    output.append(f"  Source: {source_id} ({source_text})")
                    output.append(f"  Target: {target_id} ({target_text})")
                else:
                    output.append(f"  Source: {source_id}")
                    output.append(f"  Target: {target_id}")

    return "\n".join(output)


def save_samples_to_file(
    findings_data: List[Dict],
    impression_data: List[Dict],
    output_path: str = "radgraph_samples.txt",
    num_samples: int = 2,
):
    """
    Save formatted report samples to a file.

    Args:
        findings_data: List of findings reports
        impression_data: List of impression reports
        output_path: Path to save the output file
        num_samples: Number of samples to save for each section
    """
    with open(output_path, "w", encoding="utf-8") as f:
        # Write findings samples
        f.write("\nFINDINGS SECTION SAMPLES:")
        f.write(format_report_sample(findings_data, num_samples))

        # Write impression samples
        f.write("\n\nIMPRESSION SECTION SAMPLES:")
        f.write(format_report_sample(impression_data, num_samples))

        # Write basic statistics
        f.write("\n\nBASIC STATISTICS:")
        f.write(f"\nNumber of Finding reports: {len(findings_data)}")
        f.write(f"\nNumber of Impression reports: {len(impression_data)}")

        # Write additional info about data structure
        if findings_data:
            f.write("\n\nDATA STRUCTURE INFO:")
            example_report = findings_data[0]["0"]
            f.write("\nAvailable Fields: " + ", ".join(sorted(example_report.keys())))

            # Show entity structure
            if "entities" in example_report:
                first_entity = next(iter(example_report["entities"].values()))
                f.write("\n\nExample Entity Structure:")
                f.write("\nEntity Fields: " + ", ".join(sorted(first_entity.keys())))


def main():
    # File paths
    findings_path = "/teamspace/studios/this_studio/data/raw/section_findings.json"
    impression_path = "/teamspace/studios/this_studio/data/raw/section_impression.json"

    # Load files
    print("\nLoading Findings section...")
    findings_data = load_radgraph_file(findings_path)

    print("\nLoading Impression section...")
    impression_data = load_radgraph_file(impression_path)

    # Save samples to file
    output_path = "radgraph_samples.txt"
    print(f"\nSaving samples to {output_path}...")
    save_samples_to_file(findings_data, impression_data, output_path, num_samples=2)
    print("Done!")


if __name__ == "__main__":
    main()
