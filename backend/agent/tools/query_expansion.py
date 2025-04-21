from typing import List
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import generate_gemini_response

class QueryExpansionTool:
    """
    Tool to expand search queries with related terms and variations
    """
    
    def __init__(self):
        self.__name__ = "query_expansion_tool"
    
    async def __call__(self, query: str) -> str:
        """
        Expand a search query with related terms
        
        Args:
            query: The original search query
            
        Returns:
            An expanded search query
        """
        prompt = f"""
        You are a search expert tasked with expanding a search query to improve 
        search results. For the query below, enhance it by:
        
        1. Adding synonyms or related terms
        2. Including alternative phrasings
        3. Formulating the query to maximize search relevance
        
        ORIGINAL QUERY: {query}
        
        Return ONLY the expanded search query as a single string, optimized for search engines.
        """
        
        response = await generate_gemini_response(prompt)
        
        # Clean up the response
        expanded_query = response.strip()
        
        # Remove quotes if present
        if expanded_query.startswith('"') and expanded_query.endswith('"'):
            expanded_query = expanded_query[1:-1]
            
        return expanded_query