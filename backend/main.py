from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
from agent.langagent import ResearchAgentGraph
import uvicorn

app = FastAPI(title="Research Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ResearchRequest(BaseModel):
    topic: str
    max_results: Optional[int] = 5

class ResearchResponse(BaseModel):
    summary: str
    subtopics: List[str]
    search_results: List[Dict[str, Any]]
    critique: Optional[str] = None

# Initialize the agent
research_agent = ResearchAgentGraph()

@app.post("/api/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest):
    """
    Process a research request and return results
    """
    try:
        # Run the agent on the research topic
        result = await research_agent.run(
            {"topic": request.topic, "max_results": request.max_results}
        )
        
        return ResearchResponse(
            summary=result["summary"],
            subtopics=result["subtopics"],
            search_results=result["search_results"],
            critique=result.get("critique")
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)