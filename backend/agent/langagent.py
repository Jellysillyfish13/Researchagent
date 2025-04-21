from typing import Dict, Any, List, Annotated, TypedDict, Optional, Literal
from langgraph.graph import StateGraph, END
import asyncio
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

# Import tools
from .tools.topic_breakdown import TopicBreakdownTool
from .tools.query_expansion import QueryExpansionTool
from .tools.search import SearchTool
from .tools.critique import CritiqueTool
from .tools.summarizer import SummarizerTool

# Define agent state
class AgentState(TypedDict, total=False):
    """
    Definition of research agent state
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

class ResearchAgentGraph:
    def __init__(self):
        # Initialize tool instances
        self.topic_breakdown_tool = TopicBreakdownTool()
        self.query_expansion_tool = QueryExpansionTool()
        self.search_tool = SearchTool()
        self.critique_tool = CritiqueTool()
        self.summarizer_tool = SummarizerTool()
        
        # Build tool map using string names
        self.tools_map = {
            "topic_breakdown": self.topic_breakdown_tool,
            "query_expansion_tool": self.query_expansion_tool,
            "search_tool": self.search_tool,
            "critique_tool": self.critique_tool,
            "summarizer_tool": self.summarizer_tool
        }
        
        # Build and compile the state graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """
        Build LangGraph workflow
        """
        # Create state graph
        graph = StateGraph(AgentState)
        
        # Add nodes - Note: node names must not conflict with state keys
        graph.add_node("topic_breakdown", self._run_topic_breakdown)
        graph.add_node("query_expansion", self._run_query_expansion)
        graph.add_node("search", self._run_search)
        graph.add_node("summarize", self._run_summarize)
        graph.add_node("critique_node", self._run_critique)  # Renamed to avoid conflict with state key
        
        # Define transitions between nodes
        graph.add_edge("topic_breakdown", "query_expansion")
        graph.add_edge("query_expansion", "search")
        graph.add_edge("search", "summarize")
        graph.add_edge("summarize", "critique_node")
        
        # Add conditional edges from critique_node to search or END
        graph.add_conditional_edges(
            "critique_node",
            self._should_refine,
            {
                "search": "search",
                "end": END
            }
        )
        
        # Set entry point of the workflow
        graph.set_entry_point("topic_breakdown")
        
        # Compile and return the state graph
        return graph.compile()

    async def _run_topic_breakdown(self, state: AgentState) -> AgentState:
        """Run the topic breakdown tool"""
        topic = state["topic"]
        result = await self.topic_breakdown_tool(topic)
        state["subtopics"] = result
        return state

    async def _run_query_expansion(self, state: AgentState) -> AgentState:
        """Run the query expansion tool"""
        expanded_queries = []
        for subtopic in state["subtopics"]:
            expanded_query = await self.query_expansion_tool(subtopic)
            expanded_queries.append(expanded_query)
        state["expanded_queries"] = expanded_queries
        return state

    async def _run_search(self, state: AgentState) -> AgentState:
        """Run the search tool for each expanded query"""
        all_results = []
        for query in state["expanded_queries"]:
            search_results = await self.search_tool(
                query=query,
                max_results=state["max_results"]
            )
            all_results.extend(search_results)
        state["search_results"] = all_results
        return state

    async def _run_summarize(self, state: AgentState) -> AgentState:
        """Run the summarizer tool"""
        summary = await self.summarizer_tool(
            topic=state["topic"],
            search_results=state["search_results"]
        )
        state["summary"] = summary
        return state

    async def _run_critique(self, state: AgentState) -> AgentState:
        """Run the critique tool"""
        critique_result = await self.critique_tool(
            topic=state["topic"],
            summary=state["summary"],
            search_results=state["search_results"]
        )
        
        # Ensure the critique_result is a dictionary
        if isinstance(critique_result, str):
            import json
            try:
                critique_result = json.loads(critique_result)
            except json.JSONDecodeError:
                critique_result = {
                    "critique": critique_result,
                    "needs_refinement": False,
                    "refinement_queries": []
                }
        
        # Update state
        state["critique"] = critique_result.get("critique", "")
        state["needs_refinement"] = critique_result.get("needs_refinement", False)
        
        if state["needs_refinement"]:
            state["refinement_queries"] = critique_result.get("refinement_queries", [])
        
        return state

    def _should_refine(self, state: AgentState) -> str:
        """Determine whether to re-run search with refined queries"""
        if state["needs_refinement"] and state.get("refinement_queries", []):
            # Update expanded queries to refined queries
            state["expanded_queries"] = state["refinement_queries"]
            return "search"
        else:
            return "end"

    async def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the research agent
        
        Args:
            inputs: A dictionary containing "topic" and optional parameters
        
        Returns:
            A result dictionary containing the summary and supporting information
        """
        # Initialize state
        state = AgentState(
            topic=inputs["topic"],
            max_results=inputs.get("max_results", 5),
            subtopics=[],
            expanded_queries=[],
            search_results=[],
            summary="",
            critique="",
            needs_refinement=False
        )
        
        # Invoke the graph and wait for result
        result = await self.graph.ainvoke(state)
        
        # Return results
        return {
            "topic": result["topic"],
            "subtopics": result["subtopics"],
            "search_results": result["search_results"],
            "summary": result["summary"],
            "critique": result["critique"]
        }
