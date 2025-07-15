"""
Vector database service using ChromaDB.
This handles storing and searching document embeddings.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
from langchain_cohere import CohereEmbeddings
from app.config import settings as app_settings


class VectorService:

    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(
            path="./data/chroma"
        )

        self.collection =self.chroma_client.get_or_create_collection(
            name="customer_support_docs",
            metadata={"description": "Company knowledge base "}
        ) 

        self.embeddings = CohereEmbeddings(
            cohere_api_key=app_settings.cohere_api_key,
            model="embed-englis-v3.0"
        )
        
        async def add_document(self, text:str, metadata: Dict = None):
                    """
                        Add a document to our vector database
                        Args:
                            text: The document content
                            metadata: Extra info (filename, date, etc.)

                    """
                    doc_id = f"doc_{hash(text)}"
                    embedding = await self.embeddings.aembed_query(text)

                    self.collection.add(
                           ids=[doc_id],
                           embeddings= [embedding],
                           documents=[text],
                           metadata=[metadata or {}]
                    )

                    return doc_id 
        
        async def search(self, query:str, n_results: int=3):                           
                       """
                       Search for relevant documents
                       Args:
                            query: What the user is asking
                            n_results: How many results to return
                        """
                       query_embedding = await self.embeddings.aembed_query(query)
                       results = self.collection.query(
                               query_embeddings=[query_embedding],
                               n_results=n_results
                       )
                       documents = results.get('documents', [[]])[0]
                       return documents
        def delete_all():
                self.chroma_client.delete_collection("customer_support_docs")
                self.collection = self.chroma_client.create_collection(
                        name="customer_support_docs"
                )
 
vector_service = VectorService()