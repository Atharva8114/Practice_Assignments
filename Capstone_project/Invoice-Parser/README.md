# 🧾 Invoice Parser + RAG Query System

A **production‑ready, end‑to‑end invoice intelligence platform** that combines **OCR**, **LayoutLMv3**, and **Retrieval‑Augmented Generation (RAG)** to extract, understand, and query invoice data — **without using any paid APIs or proprietary LLMs**.

---

## ✨ Key Highlights

🚀 **Fully Open‑Source & Free Stack**
🧠 **Layout‑aware Document Understanding**
🔍 **Natural Language Invoice Search (RAG)**
🖥️ **Interactive Streamlit UI**
📄 **Multi‑format Invoice Support**

---

## 🔥 Features

### 📂 Multi‑Format Invoice Support

* PNG, JPG, JPEG
* Single & multi‑page PDFs

### 🔠 Advanced OCR Pipeline

* **Tesseract OCR** for text extraction
* Bounding‑box extraction & normalization (0–1000 scale)
* Robust handling of noisy invoices

### 🧠 Layout Understanding (LayoutLMv3)

* Uses **microsoft/layoutlmv3‑base**
* Combines **text + layout + spatial relationships**
* Token normalization for clean outputs

### 🧾 Invoice Schema Extraction

Automatically extracts:

* Invoice Number
* Invoice Date & Due Date
* Total Amount
* Tax Amount
* Currency

### 📊 Line Item Detection

Extracts structured line items:

* Description
* Quantity
* Unit Price
* Line Total

### 🔍 RAG‑Based Invoice Querying

* Ask questions across **all uploaded invoices**
* FAISS‑based vector search
* Context‑aware answers using FLAN‑T5

### 🖥️ Interactive UI

* Built with **Streamlit**
* Drag‑and‑drop uploads
* Real‑time extraction & querying

---

## 🏗️ System Architecture

```
Invoice Upload
      ↓
PDF/Image Processing
      ↓
OCR (Tesseract)
      ↓
LayoutLMv3 Embeddings
      ↓
Schema Extraction
      ↓
Line Item Detection
      ↓
FAISS Vector Store
      ↓
RAG Query System
```

---

## 🛠️ Prerequisites

### ✅ Option 1: Docker (Recommended)

Docker bundles **all system dependencies**.

* Docker installed on your system

👉 Best for **quick setup & deployment**

---

### ✅ Option 2: Local Python Setup

#### 🔧 System Dependencies

**Tesseract OCR** *(Required)*

* Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
* macOS: `brew install tesseract`
* Windows: Download from GitHub

**Poppler** *(Required for PDFs)*

* Ubuntu/Debian: `sudo apt-get install poppler-utils`
* macOS: `brew install poppler`
* Windows: Download Poppler binaries

#### 🐍 Python Requirements

* Python **3.8+**
* pip package manager

---

## 🚀 Installation

### 🐳 Option 1: Docker Installation (Recommended)

```bash
# Build image
docker build -t invoice-parser-rag .

# Run container
docker run -p 8501:8501 invoice-parser-rag
```

📍 Access UI at: **[http://localhost:8501](http://localhost:8501)**

#### Development Mode (Live Code Changes)

```bash
docker run -p 8501:8501 -v $(pwd):/app invoice-parser-rag
```

---

### 🐍 Option 2: Local Python Installation

```bash
# Clone repository
git clone <repo-url>
cd invoice-parser-rag

# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt
```

#### ⚙️ Windows Only: Configure Tesseract Path

Edit `services/ocr_service.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

🌐 Opens automatically at **[http://localhost:8501](http://localhost:8501)**

Alternate port:

```bash
streamlit run app.py --server.port 8080
```

---

## 📁 Project Structure

```
.
├── app.py                  # Streamlit UI
├── Dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
├── services/
│   ├── ocr_service.py
│   ├── layoutlm_service.py
│   ├── pdf_service.py
│   ├── schema_extractor.py
│   ├── line_item_extractor.py
│   ├── token_normalizer.py
│   ├── rag_service.py
│   └── schema_mapper.py
└── README.md
```

---

## 🧑‍💻 Usage Guide

### 📤 Upload Invoices

* Drag & drop or browse files
* Supports images & PDFs
* Multi‑page PDFs processed page‑by‑page

### 📊 View Extracted Data

For each invoice:

* Invoice preview
* Structured JSON summary
* Line items table
* Raw OCR text

### 🔍 Ask Questions (RAG)

Example queries:

* "What is the total amount of invoice INV‑12345?"
* "Which invoices are due this month?"
* "Show invoices from Company XYZ"
* "What items were purchased in January?"

---

## 🧾 Expected Invoice Schema

| Field          | Description   | Example    |
| -------------- | ------------- | ---------- |
| invoice_number | Invoice ID    | INV‑12345  |
| invoice_date   | Invoice date  | 2024‑01‑15 |
| due_date       | Payment due   | 2024‑02‑15 |
| total_amount   | Total payable | 1250.00    |
| tax            | Tax amount    | 125.00     |
| currency       | Currency      | INR, USD   |
| line_items     | Itemized list | See below  |

### 📦 Line Item Schema

* description
* quantity
* unit_price
* amount

---

## ⚠️ Current Limitations & Known Issues

> **Important Note on Model Performance**

The current implementation of this project **performs significantly better on generated / synthetic invoices** (programmatically created or template-based invoices) **compared to real-world scanned invoices**.

### 🔍 Observed Behavior

* **OCR (Tesseract)** works reliably on both generated and real invoices and is able to extract most of the visible text accurately.
* However, the **LayoutLMv3-based extraction sometimes fails to correctly map certain fields (schemas)** when dealing with real-world invoices.

### ❗ Root Cause

* Real invoices often have:

  * Highly varied layouts
  * Non-standard field positioning
  * Decorative fonts, stamps, or watermarks
  * Inconsistent spacing and alignment

* The current **LayoutLMv3 model is not fine-tuned on a sufficiently diverse real-invoice dataset**, which results in:

  * Missed schema fields (e.g., invoice number, tax, or due date)
  * Incorrect association between text tokens and layout regions

### ✅ What Works Well

* Generated invoices with:

  * Clean layouts
  * Consistent spacing
  * Standard field labels (e.g., "Invoice No", "Total Amount")

### 🚧 Planned Improvements

* Fine-tuning LayoutLMv3 on **real-world invoice datasets** (e.g., RVL-CDIP, DocBank, CORD-style invoices)
* Hybrid extraction strategy:

  * Rule-based + OCR fallback when LayoutLM confidence is low
* Confidence scoring for extracted schemas
* Template clustering before schema extraction

---

## 🧠 Technical Details

### OCR Pipeline

* Tesseract text + bounding boxes
* Normalized coordinates for LayoutLM

### Schema Extraction

* Regex‑based pattern matching
* Multi‑date format support
* Currency symbol detection
* Largest monetary value selected as total

### RAG System

* **Embeddings:** all‑MiniLM‑L6‑v2 (384‑D)
* **Vector DB:** FAISS (L2 similarity)
* **LLM:** google/flan‑t5‑small
* **Top‑K Retrieval:** 5 documents

---

## 🐞 Troubleshooting

| Issue                    | Solution                       |
| ------------------------ | ------------------------------ |
| TesseractNotFoundError   | Install Tesseract / use Docker |
| PDFInfoNotInstalledError | Install Poppler                |
| CUDA OOM                 | Runs on CPU by default         |
| Poor OCR                 | Use 300 DPI images             |
| Port in use              | Change port mapping            |

---

## ⚡ Performance Tips

* Batch invoice uploads
* Allocate more RAM in Docker: `--memory=4g`
* Enable GPU if available

---

## 🤖 Models Used

| Component            | Model            |
| -------------------- | ---------------- |
| Layout Understanding | LayoutLMv3‑base  |
| Embeddings           | all‑MiniLM‑L6‑v2 |
| LLM                  | FLAN‑T5‑small    |

---

## 🔮 Future Enhancements

* Multi‑language OCR
* Template‑aware invoice parsing
* Table structure detection
* Export to QuickBooks / Xero
* REST API for batch processing
* Invoice fraud & anomaly detection

---

### ⭐ If you like this project, consider starring the repository!

