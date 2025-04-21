from typing import List, Dict, Any
import sys
import os
import json
from dotenv import load_dotenv
load_dotenv() 
# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import search_web

class SearchTool:
    """
    Tool to search the web for information
    """
    
    def __init__(self):
        self.__name__ = "search_tool"
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            print("WARNING: SEARCH_API_KEY environment variable not set. Search functionality will be limited.")
            # Use a mock API key for development
            self.api_key = "mock_api_key"
    
    async def __call__(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search the web for information
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            A list of search result dictionaries
        """
        # If using mock data for development
        if self.api_key == "mock_api_key":
            return self._mock_search(query, max_results)
        
        # Real search
        results = search_web(query, self.api_key, max_results)
        return results
    
    def _mock_search(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Mock search function for development/testing
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            A list of mock search results
        """
        # Create mock results based on the query
        mock_results = []
        for i in range(min(max_results, 3)):
            mock_results.append({
                "title": f"Result {i+1} for {query}",
                "snippet": f"This is a snippet of information related to {query}. It contains relevant details that would be useful for research.",
                "url": f"https://example.com/result-{i+1}"
            })
        return mock_results