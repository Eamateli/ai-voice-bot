"""
Vector database service using ChromaDB.
This handles storing and searching document embeddings.
"""
import chromadb
from typing import List, Dict
import cohere
from app.config import settings as app_settings

class VectorService:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(
            path="./data/chroma"
        )
        
        self.collection = self.chroma_client.get_or_create_collection(
            name="customer_support_docs",
            metadata={"description": "Company knowledge base"}
        )
        
        # Use Cohere directly instead of LangChain
        self.co = cohere.Client(app_settings.COHERE_API_KEY)
    
    async def add_document(self, text: str, metadata: Dict = None):
        doc_id = f"doc_{hash(text)}"
        
        # Use Cohere's embed endpoint directly
        response = self.co.embed(
            texts=[text],
            model="embed-english-v3.0"
        )
        embedding = response.embeddings[0]
        
        self.collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata or {}]
        )
        
        return doc_id
    
    async def search(self, query: str, n_results: int = 3):
        # Embed the query
        response = self.co.embed(
            texts=[query],
            model="embed-english-v3.0"
        )
        query_embedding = response.embeddings[0]
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        documents = results.get('documents', [[]])[0]
        return documents
    
    def delete_all(self):
        self.chroma_client.delete_collection("customer_support_docs")
        self.collection = self.chroma_client.create_collection(
            name="customer_support_docs"
        )

vector_service = VectorService()