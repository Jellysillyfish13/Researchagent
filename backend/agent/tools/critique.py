from typing import Dict, List, Any
import sys
import os
import json
# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import generate_gemini_response

class CritiqueTool:
    """
    Tool to critique research summaries and suggest improvements
    """
    
    def __init__(self):
        self.__name__ = "critique_tool"
    
    async def __call__(self, topic: str, summary: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Critique a research summary and suggest improvements
        
        Args:
            topic: The research topic
            summary: The generated summary
            search_results: The search results used to generate the summary
            
        Returns:
            Dictionary with critique and refinement suggestions
        """
        # Format search results for the LLM
        formatted_results = "\n".join([
            f"- {result.get('title', 'No title')}: {result.get('snippet', 'No snippet')}"
            for result in search_results[:3]  # Limit to avoid token limits
        ])
        
        prompt = f"""
        You are a research critique specialist. Evaluate the following research summary 
        on the topic: "{topic}".
        
        SUMMARY:
        {summary}
        
        SEARCH RESULTS USED (SAMPLE):
        {formatted_results}
        
        Provide a detailed critique addressing:
        1. Accuracy - Does the summary accurately reflect the search results?
        2. Comprehensiveness - Are important aspects missing?
        3. Balance - Is the treatment of the topic balanced?
        4. Clarity - Is the summary clear and well-organized?
        
        Then, determine if the research needs refinement:
        - If YES, suggest specific additional search queries.
        - If NO, indicate that the research is adequate.
        
        FORMAT YOUR RESPONSE AS A JSON OBJECT with the following keys:
        - "critique": Your detailed critique
        - "needs_refinement": Boolean (true/false)
        - "refinement_queries": List of additional search queries (if needs_refinement is true)
        """
        
        response = await generate_gemini_response(prompt)
        
        # Extract the JSON from the response
        try:
            # Clean up the response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].strip()
            else:
                json_str = response.strip()
                
            result = json.loads(json_str)
            
            # Ensure we have all required fields
            if "critique" not in result:
                result["critique"] = "No critique provided."
            if "needs_refinement" not in result:
                result["needs_refinement"] = False
            if "refinement_queries" not in result and result["needs_refinement"]:
                result["refinement_queries"] = [f"{topic} latest research", f"{topic} critiques"]
                
            return result
        except Exception as e:
            print(f"Error parsing critique: {e}")
            # Return a fallback result
            return {
                "critique": "The summary appears reasonable but could benefit from additional details and sources.",
                "needs_refinement": False,
                "refinement_queries": []
            }