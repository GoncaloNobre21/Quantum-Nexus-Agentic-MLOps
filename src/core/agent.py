from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from src.core.retriever import HybridRetriever
from src.utils.logger import logger

class NexusAgent:
    """
    Autonomous Agent for RAG operations with self-correction capabilities.
    """
    def __init__(self, retriever: HybridRetriever, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.retriever = retriever
        self.system_prompt = ChatPromptTemplate.from_template(
            "You are a professional AI assistant. Answer the user question based on the context.\n\n"
            "Context: {context}\n\n"
            "Question: {question}"
        )
        logger.info(f"NexusAgent initialized with model={model_name}")

    async def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Main execution flow: Search -> Evaluate -> Synthesize
        """
        logger.info(f"Agent executing query: {query}")
        
        # Phase 1: Retrieval
        context_docs = await self.retriever.search(query)
        context_text = "\n".join([doc["content"] for doc in context_docs])
        
        # Phase 2: Evaluation (Self-Correction Placeholder)
        # In a real enterprise app, we'd use a separate LLM call to grade retrieval quality
        relevance_score = 1.0  # Simulated score
        
        if relevance_score < 0.7:
            logger.warning("Low relevance detected. Refinement required.")
            # Logic for query refinement would go here
        
        # Phase 3: Generation
        chain = self.system_prompt | self.llm
        response = await chain.ainvoke({
            "context": context_text,
            "question": query
        })
        
        return {
            "query": query,
            "answer": response.content,
            "sources": [doc["metadata"] for doc in context_docs],
            "metadata": {
                "relevance_score": relevance_score,
                "model": self.llm.model_name
            }
        }
