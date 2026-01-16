from services.rag_service import RAGService

def test_rag_add_and_query():
    rag = RAGService()

    invoice_text = """
    Invoice Number: INV-1001
    Total Amount: 500
    Currency: USD
    """

    rag.add_invoice(invoice_text)

    answer, docs = rag.query("What is the invoice number?")

    assert "INV-1001" in answer
    assert len(docs) > 0
