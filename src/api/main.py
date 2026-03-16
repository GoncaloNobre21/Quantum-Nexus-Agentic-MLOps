from fastapi import FastAPI, HTTPException, Depends
from src.api.schemas import QueryRequest, QueryResponse, IngestionRequest, HealthResponse
from src.core.retriever import HybridRetriever
from src.core.agent import NexusAgent
from src.utils.logger import logger
import uvicorn
import os

app = FastAPI(
    title="Quantum Nexus: Agentic MLOps Platform",
    description="Enterprise-grade Agentic RAG and MLOps Framework",
    version="0.1.0"
)

# Global State
retriever = HybridRetriever(persist_directory=os.getenv("CHROMA_DIR", "data/chroma"))
agent = NexusAgent(retriever=retriever)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}

@app.post("/ingest", status_code=201)
async def ingest_documents(request: IngestionRequest):
    try:
        retriever.add_documents(texts=request.texts, metadatas=request.metadatas)
        return {"message": f"Successfully ingested {len(request.texts)} documents"}
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail="Document ingestion failed")

@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    try:
        response = await agent.execute_query(request.query)
        return response
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise HTTPException(status_code=500, detail="Internal processing error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
