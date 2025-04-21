from typing import List, Dict, Any
import sys
import os
import json
import traceback

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils import generate_gemini_response

class TopicBreakdownTool:
    """
    Tool to break down a research topic into subtopics
    """
    
    def __init__(self):
        # Ensure the tool name matches what is used in ResearchAgentGraph
        self.__name__ = "TopicBreakdownTool"
    
    async def __call__(self, topic: str) -> List[str]:
        """
        Break down a research topic into manageable subtopics
        
        Args:
            topic: The main research topic
            
        Returns:
            A list of subtopics
        """
        try:
            prompt = f"""
            You are a research assistant tasked with breaking down a broad topic into specific, 
            searchable subtopics. For the topic below, generate 3-5 focused subtopics 
            that would help in comprehensive research.

            TOPIC: {topic}

            FORMAT YOUR RESPONSE AS A JSON ARRAY OF STRINGS. 
            Example: ["subtopic 1", "subtopic 2", "subtopic 3"]
            """
            
            try:
                # Use async function to get the response
                response = await generate_gemini_response(prompt, model_name="gemini-1.5-flash")
                
            except Exception as e:
                print(f"Error calling generate_gemini_response: {e}")
                # If the API call fails, return fallback options
                return [f"{topic} overview", f"{topic} definition", f"{topic} examples"]
            
            # Clean up JSON response
            clean_response = response.strip()
            if clean_response.startswith("```") and clean_response.endswith("```"):
                clean_response = clean_response[3:-3].strip()
            if clean_response.startswith("python") or clean_response.startswith("json"):
                clean_response = clean_response.split("\n", 1)[1].strip()
 
            try:
                subtopics = json.loads(clean_response)
                
                if not isinstance(subtopics, list) or not all(isinstance(item, str) for item in subtopics):
                    raise ValueError("Response is not a list of strings")
                return subtopics
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing subtopics: {e}")
                print(f"Raw response: {response}")
              
                try:
                    # Attempt to fix common JSON format issues
                    clean_response = clean_response.replace("'", "\"")
                    subtopics = json.loads(clean_response)
                    if isinstance(subtopics, list) and all(isinstance(item, str) for item in subtopics):
                        return subtopics
                except Exception:
                    pass
                
                # If parsing fails, return fallback options
                return [f"{topic} overview", f"{topic} definition", f"{topic} examples"]
                
        except Exception as e:
            print(f"Unexpected error in TopicBreakdownTool: {e}")
            print(traceback.format_exc())
            # If any exception occurs, return fallback options
            return [f"{topic} overview", f"{topic} definition", f"{topic} examples"]
