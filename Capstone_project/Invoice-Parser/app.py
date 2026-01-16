import streamlit as st
from services.ocr_service import run_ocr
from services.layoutlm_service import extract_entities
from services.token_normalizer import normalize_layoutlm_tokens
from services.schema_extractor import extract_invoice_schema
from services.pdf_service import pdf_to_images
from services.line_item_extractor import extract_line_items
from services.rag_service import RAGService
from PIL import Image

st.title("Invoice Parser + RAG Query System")

# Initialize RAG service
rag = RAGService()

uploaded_file = st.file_uploader("Upload Invoice", type=["png", "jpg", "jpeg", "pdf"])

if uploaded_file:
    images = []

    if uploaded_file.type == "application/pdf":
        images = pdf_to_images(uploaded_file.read())
    else:
        images = [Image.open(uploaded_file).convert("RGB")]

    for idx, image in enumerate(images):
        st.image(image, caption=f"Page {idx + 1}", use_column_width=True)

        words, boxes = run_ocr(image)
        tokens = extract_entities(image, words, boxes)
        normalized_text = normalize_layoutlm_tokens(tokens)

        schema = extract_invoice_schema(normalized_text)
        line_items = extract_line_items(words, boxes)
        schema["line_items"] = line_items

        # -------------------------
        # Invoice Summary
        # -------------------------
        st.subheader(f"Invoice Summary – Page {idx + 1}")
        st.json(schema)

        # -------------------------
        # Raw OCR Output (NEW)
        # -------------------------
        st.subheader("Raw OCR Text")
        raw_ocr_text = " ".join(words)
        st.text_area(
            label="OCR Output",
            value=raw_ocr_text,
            height=250
        )

        # -------------------------
        # Add invoice to RAG DB
        # -------------------------
        schema_text = f"""
Invoice Number: {schema['invoice_number']}
Invoice Date: {schema['invoice_date']}
Due Date: {schema.get('due_date')}
Total Amount: {schema['total_amount']}
Tax: {schema.get('tax')}
Currency: {schema.get('currency')}
Line Items: {schema.get('line_items')}
Raw OCR: {raw_ocr_text}
"""
        rag.add_invoice(schema_text)

# -------------------------
# Query invoices (RAG)
# -------------------------
st.subheader("Ask questions about uploaded invoices")
user_query = st.text_input("Enter your query:")

if user_query:
    answer, top_matches = rag.query(user_query)
    st.markdown(f"**Answer:** {answer}")

    with st.expander("Top Retrieved Invoices for reference"):
        for t in top_matches:
            st.text(t)
