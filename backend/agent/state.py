from typing import Dict, List, Any, Optional, TypedDict, Literal

class AgentState(TypedDict, total=False):
    """
    State definition for the research agent
    """
    # Input parameters
    topic: str
    max_results: int
    
    # Intermediate results
    subtopics: List[str]
    expanded_queries: List[str]
    search_results: List[Dict[str, Any]]
    
    # Output results
    summary: str
    critique: str
    
    # Control flow
    needs_refinement: bool
    refinement_queries: Optional[List[str]]