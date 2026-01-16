from services.token_normalizer import normalize_layoutlm_tokens

def test_token_normalizer_basic():
    tokens = ["ĠINV", "-", "3337", "ĠDATE", ":", "2024"]

    text = normalize_layoutlm_tokens(tokens)

    assert "INV-3337" in text
    assert "2024" in text
