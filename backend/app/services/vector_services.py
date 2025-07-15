"""
Vector database service using ChromaDB.
This handles storing and searching document embeddings.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict


class VectorService:

    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(
            path="./data/chroma"
        )

        self.collection =self.chroma_client.get_or_create_collection(
            name="customer_support_docs",
            metadata={"description": "Company knowledge base "}
        )