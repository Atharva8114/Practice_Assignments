import re

def map_schema(tokens):
    text = " ".join(tokens)

    def find(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1) if match else None

    return {
        "invoice_number": find(r"(invoice\s*(no|number)[:\-]?\s*)(\w+)"),
        "invoice_date": find(r"(date[:\-]?\s*)(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"),
        "total_amount": find(r"(total\s*(amount)?[:\-]?\s*)(₹?\$?\d+[.,]?\d*)"),
        "tax": find(r"(tax[:\-]?\s*)(₹?\$?\d+[.,]?\d*)"),
    }
