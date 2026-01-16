import re



def extract_invoice_schema(text):
    schema = {
        "invoice_number": None,
        "invoice_date": None,
        "total_amount": None,
        "tax": None,
        "due_date": None,
        "currency": None,

    }

    # Invoice Number
    inv_match = re.search(r"INV-\d+", text, re.IGNORECASE)
    if inv_match:
        schema["invoice_number"] = inv_match.group()

    # Invoice Date
    date_patterns = [
    r"\b\d{4}\s*[-/]\s*\d{2}\s*[-/]\s*\d{2}\b",   # 2024 - 01 - 15
    r"\b\d{2}\s*[-/]\s*\d{2}\s*[-/]\s*\d{4}\b",   # 15 - 01 - 2024
    r"\b\d{2}\s*/\s*\d{2}\s*/\s*\d{2}\b",         # 15 / 01 / 24
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b",
    r"\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b",
]
    

    for pattern in date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
        # normalize spaces: "2024 - 01 - 15" → "2024-01-15"
            schema["invoice_date"] = re.sub(r"\s*", "", match.group())
            break
    
    # Due Date
    due_date_patterns = [
    r"(due\s*date|payment\s*due|pay\s*by)\s*[:\-]?\s*"
    r"(\d{4}\s*[-/]\s*\d{2}\s*[-/]\s*\d{2}|\d{2}\s*[-/]\s*\d{2}\s*[-/]\s*\d{4})"
]

    for pattern in due_date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            schema["due_date"] = re.sub(r"\s*", "", match.group(2))
            break

    # Currency Detection
    
    currency_map = {
    "₹": "INR",
    "$": "USD",
    "€": "EUR",
    "£": "GBP"
}

    keyword_map = {   # ✅ DEFINE FIRST
    "inr": "INR",
    "usd": "USD",
    "eur": "EUR",
    "gbp": "GBP"
}

    schema["currency"] = None

    # Symbol-based detection
    for symbol, code in currency_map.items():
     if symbol in text:
        schema["currency"] = code
        break

    # Keyword-based detection
    if not schema["currency"]:
        for k, v in keyword_map.items():
            if re.search(rf"\b{k}\b", text, re.IGNORECASE):
                schema["currency"] = v
                break


    # Amounts
    amounts = re.findall(r"\$\d+(?:\.\d{2})?", text)
    if amounts:
        values = [float(a.replace("$", "")) for a in amounts]
        schema["total_amount"] = max(values)

    # Tax (optional)
    tax_match = re.search(r"tax\s*\$?(\d+(?:\.\d{2})?)", text, re.IGNORECASE)
    if tax_match:
        schema["tax"] = float(tax_match.group(1))

    return schema

    

