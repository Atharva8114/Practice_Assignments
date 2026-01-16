import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

class RAGService:
    def __init__(self):
        # Embedding model
        self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')

        # Initialize FAISS index
        self.dimension = 384  # all-MiniLM-L6-v2 embedding size
        self.index = faiss.IndexFlatL2(self.dimension)
        self.invoice_texts = []  # stores raw invoice text for retrieval

        # LLM for answering queries
        self.qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

    def add_invoice(self, schema_text):
        """Add invoice text to vector DB."""
        embedding = self.embed_model.encode(schema_text)
        embedding = np.array([embedding]).astype('float32')
        self.index.add(embedding)
        self.invoice_texts.append(schema_text)

    def query(self, user_query, top_k=5):
        """Query vector DB and generate answer."""
        query_vec = self.embed_model.encode(user_query)
        query_vec = np.array([query_vec]).astype('float32')
        distances, indices = self.index.search(query_vec, top_k)

        # Get top matched invoices
        retrieved_texts = [self.invoice_texts[i] for i in indices[0] if i < len(self.invoice_texts)]
        context = "\n\n".join(retrieved_texts)

        # Generate answer using LLM
        prompt = f"Answer the query based on these invoices:\n{context}\nQuery: {user_query}"
        answer = self.qa_pipeline(prompt, max_length=200)[0]['generated_text']

        return answer, retrieved_texts
