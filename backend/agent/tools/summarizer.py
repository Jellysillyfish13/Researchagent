from typing import Dict, List, Any
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import generate_gemini_response, format_results_for_llm

class SummarizerTool:
    """
    Tool to summarize search results into a coherent summary
    """
    
    def __init__(self):
        self.__name__ = "summarizer_tool"
    
    async def __call__(self, topic: str, search_results: List[Dict[str, Any]]) -> str:
        """
        Generate a research summary from search results
        
        Args:
            topic: The research topic
            search_results: The search results to summarize
            
        Returns:
            A summary paragraph
        """
        # Format the search results for the LLM
        formatted_results = format_results_for_llm(search_results)
        
        prompt = f"""
        You are a research assistant tasked with creating a concise, informative summary 
        on the topic: "{topic}"
        
        Use the following search results to create your summary:
        
        {formatted_results}
        
        Guidelines:
        - Write approximately 1 paragraph (5-7 sentences)
        - Focus on factual information from the search results
        - Organize information in a logical flow
        - Maintain a neutral, informative tone
        - Include key concepts, findings, or definitions
        - Do not include personal opinions or speculation
        
        WRITE ONLY THE SUMMARY, without any introductions or explanations.
        """
        
        summary = await generate_gemini_response(prompt)
        
        # Clean up the summary
        summary = summary.strip()
        
        return summary