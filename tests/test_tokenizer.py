from radgraph.utils.tokenizer import load_tokenizer, tokenize_texts


def test_load_tokenizer():
    tokenizer = load_tokenizer()
    assert tokenizer is not None, "Tokenizer should be loaded successfully!"


def test_tokenize_texts():
    tokenizer = load_tokenizer()
    texts = ["Example report text.", ""]
    tokens = tokenize_texts(texts, tokenizer)

    assert "input_ids" in tokens, "Tokenized output should have input_ids!"
    assert (
        len(tokens["input_ids"]) == 2
    ), "Two texts should result in two tokenized outputs!"
