import pytest

from radgraph.data.preprocess import load_json, prepare_dataset


def test_load_json():
    """
    Test that `load_json` correctly loads data from
    valid files and raises errors on invalid paths.
    """
    data = load_json("data/raw/section_findings.json")
    assert isinstance(data, list), "Data should be a list!"

    # Test invalid file
    with pytest.raises(Exception):
        load_json("data/raw/nonexistent.json")


def test_prepare_dataset():
    json_files = ["data/raw/section_findings.json", "data/raw/section_impression.json"]
    dataset = prepare_dataset(json_files)
    assert len(dataset) > 0, "Dataset should not be empty!"
    assert isinstance(dataset[0], dict), "Each dataset entry should be a dictionary."
