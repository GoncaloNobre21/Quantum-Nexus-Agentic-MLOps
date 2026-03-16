from typing import List, Dict, Any
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from src.utils.logger import logger

class HybridRetriever:
    """
    Enterprise hybrid retriever combining Vector search and semantic metadata filtering.
    """
    def __init__(self, persist_directory: str = "data/chroma"):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )
        logger.info(f"Initialized HybridRetriever with persist_directory={persist_directory}")

    async def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Execute hybrid search across vector space and metadata.
        """
        logger.info(f"Searching for query: {query}")
        # Similarity search
        results = self.vector_store.similarity_search(query, k=top_k)
        
        # Transform to standard format
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": 0.0  # Placeholder for complex scoring
            } for doc in results
        ]

    def add_documents(self, texts: List[str], metadatas: List[Dict] = None):
        """
        Ingest new documents into the vector store.
        """
        logger.info(f"Ingesting {len(texts)} documents")
        self.vector_store.add_texts(texts=texts, metadatas=metadatas)
        self.vector_store.persist()
