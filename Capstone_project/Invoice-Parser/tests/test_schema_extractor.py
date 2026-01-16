from services.schema_extractor import extract_invoice_schema

def test_extract_invoice_schema_basic():
    text = """
    INVOICE # INV-3337
    DATE: 2024-01-15
    TOTAL $93.50
    TAX $8.50
    """

    schema = extract_invoice_schema(text)

    assert schema["invoice_number"] == "INV-3337"
    assert schema["invoice_date"] == "2024-01-15"
    assert schema["total_amount"] == 93.5
    assert schema["tax"] == 8.5
