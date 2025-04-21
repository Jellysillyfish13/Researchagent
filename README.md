# Quick Start

https://jellysillyfish13.github.io/Researchagent/

# Research Agent

A powerful, automated research assistant that leverages LLM technologies to break down research topics, expand queries, search for relevant information, and generate comprehensive summaries.

## Overview

Research Agent is a modular, graph-based workflow system built using LangGraph. It automates the research process by orchestrating multiple specialized tools to transform a broad research topic into a comprehensive, well-sourced summary.

## Features

- **Topic Breakdown**: Automatically decomposes broad research topics into focused subtopics
- **Query Expansion**: Enhances search queries with related terms and alternative phrasings
- **Smart Search**: Finds relevant information across the web
- **Summary Generation**: Creates concise, coherent summaries from search results
- **Critical Analysis**: Evaluates summaries for accuracy, comprehensiveness, and suggests refinements
- **Iterative Refinement**: Identifies and fills information gaps through additional targeted searches

## Architecture

Research Agent is built on LangGraph, a framework for creating cyclic workflows with AI components. The system follows a graph-based architecture where each node represents a specialized tool:

```
topic_breakdown → query_expansion → search → summarize → critique_node → [END or back to search]
```

The conditional edge from `critique_node` enables iterative refinement when necessary.

## Components

- **State Management**: Uses TypedDict for structured state representation
- **Tool Integration**: Specialized tools for each phase of the research process
- **LLM Integration**: Uses LiteLLM for flexible model selection (supports Gemini, Claude, GPT, etc.)
- **Error Handling**: Robust error recovery with fallback options



## Dependencies

- **LangGraph**: For workflow orchestration
- **Google Gemini API**: For AI reasoning capabilities
- **FastAPI**: For API endpoints (optional)
- **Python 3.10+**: For type hints and modern Python features


## Advanced Configuration

The Research Agent can be customized in several ways:

- **Model Selection**: Choose different LLM providers by modifying the LLMTool configuration
- **Search Sources**: Configure alternative search backends
- **Prompt Engineering**: Customize the prompts used for each tool
- **Workflow Modification**: Add or remove nodes to change the research workflow


## Acknowledgements

- [LangGraph](https://github.com/langchain-ai/langgraph) for the workflow orchestration framework
