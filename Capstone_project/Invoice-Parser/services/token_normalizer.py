def normalize_layoutlm_tokens(tokens):
    """
    Converts LayoutLM subword tokens into readable text
    """
    clean_tokens = []

    for token in tokens:
        if token in ["<s>", "</s>"]:
            continue

        # Remove Ġ (whitespace marker)
        token = token.replace("Ġ", "")

        # Merge numeric splits like ['2', '50'] → '250'
        if clean_tokens and token.isdigit() and clean_tokens[-1].isdigit():
            clean_tokens[-1] += token
        else:
            clean_tokens.append(token)

    # Join intelligently
    text = " ".join(clean_tokens)

    # Fix common spacing issues
    text = text.replace(" - ", "-")
    text = text.replace(" : ", ":")
    text = text.replace(" $ ", "$")
    text = text.replace(" . ", ".")
    text = text.replace("$ ", "$")

    return text
