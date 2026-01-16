Invoice Parser + RAG Query System
A comprehensive invoice processing system that combines OCR, LayoutLM, and RAG (Retrieval-Augmented Generation) to extract, analyze, and query invoice data intelligently.
Features

Multi-format Support: Process PNG, JPG, JPEG, and PDF invoices
Advanced OCR: Tesseract-based text extraction with bounding box normalization
Layout Understanding: LayoutLMv3 for layout-aware document understanding
Schema Extraction: Automatically extracts key invoice fields (invoice number, dates, amounts, tax, currency)
Line Item Detection: Identifies and extracts itemized charges with quantities and prices
RAG Query System: Natural language querying across all uploaded invoices using FAISS vector search
Interactive UI: Streamlit-based web interface for easy document upload and querying

Architecture
Invoice Upload → PDF/Image Processing → OCR (Tesseract) 
    → LayoutLMv3 Embeddings → Schema Extraction → Line Item Detection
    → Vector Storage (FAISS) → RAG Query System
Prerequisites
For Docker Installation (Recommended)

Docker installed on your system (Get Docker)

For Local Python Installation
System Dependencies

Tesseract OCR (Required)

Ubuntu/Debian: sudo apt-get install tesseract-ocr
macOS: brew install tesseract
Windows: Download from GitHub


Poppler (Required for PDF processing)

Ubuntu/Debian: sudo apt-get install poppler-utils
macOS: brew install poppler
Windows: Download from Poppler releases



Python Requirements

Python 3.8 or higher
pip package manager

Installation
Option 1: Docker Installation (Recommended)
Docker eliminates the need to manually install system dependencies.
Prerequisites

Docker installed on your system (Get Docker)

Quick Start
bash# Build the image
docker build -t invoice-parser-rag .

# Run the container
docker run -p 8501:8501 invoice-parser-rag
Access the application at http://localhost:8501
Option 2: Local Python Installation
1. Clone the Repository
bashgit clone <repository-url>
cd invoice-parser-rag
2. Create Virtual Environment (Recommended)
bashpython -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
3. Install Python Dependencies
bashpip install -r requirements.txt
4. Configure Tesseract Path (Windows Only)
If you're on Windows, uncomment and update the path in services/ocr_service.py:
pythonpytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
Project Structure
.
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Docker container configuration
├── services/
│   ├── ocr_service.py             # Tesseract OCR integration
│   ├── layoutlm_service.py        # LayoutLMv3 model wrapper
│   ├── pdf_service.py             # PDF to image conversion
│   ├── schema_extractor.py        # Invoice field extraction
│   ├── line_item_extractor.py     # Line item detection
│   ├── token_normalizer.py        # LayoutLM token processing
│   ├── rag_service.py             # RAG query system with FAISS
│   └── schema_mapper.py           # Alternative schema mapping
└── README.md                       # This file
Running the Application
Option 1: Docker (Recommended)
Docker provides a consistent environment with all dependencies pre-installed.
Build the Docker Image
bashdocker build -t invoice-parser-rag .
Run the Container
bashdocker run -p 8501:8501 invoice-parser-rag
Access the application at http://localhost:8501
Run with Volume Mount (for development)
bashdocker run -p 8501:8501 -v $(pwd):/app invoice-parser-rag
Option 2: Local Python Environment
Start the Streamlit Server
bashstreamlit run app.py
The application will open automatically in your default browser at http://localhost:8501
Alternative: Specify Port
bashstreamlit run app.py --server.port 8080
Usage Guide
1. Upload Invoices

Click "Browse files" or drag-and-drop invoice files
Supported formats: PNG, JPG, JPEG, PDF
Multi-page PDFs are processed page-by-page

2. View Extracted Data
For each uploaded invoice, the system displays:

Invoice Image: Visual preview of the document
Invoice Summary: Extracted fields in JSON format

Invoice Number
Invoice Date
Due Date
Total Amount
Tax
Currency
Line Items (description, quantity, unit price, amount)


Raw OCR Text: Complete text extracted by Tesseract

3. Query Invoices
After uploading invoices:

Scroll to the "Ask questions about uploaded invoices" section
Enter natural language queries like:

"What is the total amount of invoice INV-12345?"
"Which invoices are due this month?"
"Show me all invoices from Company XYZ"
"What items were purchased in invoice dated January 15?"


View the AI-generated answer and retrieved invoice contexts

Extracted Fields
Invoice Schema
FieldDescriptionExampleinvoice_numberInvoice identifierINV-12345invoice_dateDate of invoice2024-01-15due_datePayment due date2024-02-15total_amountTotal invoice amount1250.00taxTax amount125.00currencyCurrency codeUSD, EUR, INR, GBPline_itemsArray of itemized chargesSee below
Line Item Schema
Each line item contains:

description: Item description
quantity: Number of units
unit_price: Price per unit
amount: Total line amount

Technical Details
OCR Pipeline

Tesseract Extraction: Extracts text with bounding boxes
Normalization: Coordinates normalized to 0-1000 range for LayoutLM
Layout Analysis: LayoutLMv3 processes spatial relationships
Token Normalization: Subword tokens merged into readable text

Schema Extraction Rules

Invoice Number: Pattern matching for INV-XXXXX format
Dates: Multiple date format support (YYYY-MM-DD, DD/MM/YYYY, text dates)
Currency: Symbol detection (₹, $, €, £) and keyword matching
Amounts: Extracts monetary values, selects maximum as total
Tax: Pattern matching for tax declarations

RAG System

Embedding Model: all-MiniLM-L6-v2 (384 dimensions)
Vector Store: FAISS with L2 distance
LLM: Google FLAN-T5-small for answer generation
Retrieval: Top-5 most relevant invoices for context

Troubleshooting
Common Issues
Issue: TesseractNotFoundError

Solution: Install Tesseract OCR and ensure it's in your PATH
Docker: Already included in the container

Issue: PDFInfoNotInstalledError

Solution: Install Poppler utilities
Docker: Already included in the container

Issue: CUDA out of memory

Solution: Models run on CPU by default. For GPU, ensure sufficient VRAM or reduce batch size

Issue: Poor OCR accuracy

Solution: Ensure invoice images are high resolution (300 DPI recommended) and well-lit

Issue: Docker container won't start

Solution: Check if port 8501 is already in use. Use a different port: docker run -p 8080:8501 invoice-parser-rag

Issue: Permission denied when running Docker

Solution (Linux): Add your user to the docker group: sudo usermod -aG docker $USER (then log out and back in)

Performance Optimization

Process invoices in batches for better throughput
Use GPU acceleration by installing torch with CUDA support
For large document collections, consider upgrading to more powerful embedding models
Docker: Add --memory=4g flag to allocate more RAM if processing large PDFs

Model Information

LayoutLMv3: microsoft/layoutlmv3-base - Document understanding
Sentence Transformer: all-MiniLM-L6-v2 - Text embeddings
LLM: google/flan-t5-small - Answer generation

Dependencies
Key libraries:

streamlit: Web interface
pytesseract: OCR engine wrapper
transformers: LayoutLMv3 and FLAN-T5 models
sentence-transformers: Embedding generation
faiss-cpu: Vector similarity search
pdf2image: PDF processing
Pillow: Image manipulation
torch: Deep learning framework

See requirements.txt for complete list with versions.
Future Enhancements

 Support for more invoice formats and templates
 Custom field extraction using user-defined patterns
 Invoice validation and anomaly detection
 Export to accounting software formats (QuickBooks, Xero)
 Batch processing API
 Multi-language OCR support
 Enhanced line item detection with table structure recognition