import streamlit as st
import requests
import os
import json
from typing import Dict, Any

# Configuration
API_URL = "http://localhost:8000/api"

# Page config
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔍",
    layout="wide"
)

# Header
st.title("🔍 Research Agent")
st.markdown(
    """
    This tool helps you research topics by breaking them down, searching for relevant information,
    and generating a concise summary. Enter a topic below to get started.
    """
)

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This research agent uses:
        
        - LangGraph for workflow orchestration
        - Google's Gemini 2.0 Flash for AI processing
        - Web search tools for information gathering
        
        The agent breaks down your topic, expands queries, searches for relevant
        information, and creates a concise summary.
        """
    )
    
    st.header("Settings")
    max_results = st.slider(
        "Maximum search results per query", 
        min_value=1, 
        max_value=10, 
        value=3
    )

# Main form
with st.form(key="research_form"):
    topic = st.text_input("Research Topic", placeholder="Enter a topic to research...")
    submit_button = st.form_submit_button("Research")

# Process form submission
if submit_button and topic:
    try:
        # Display progress
        progress_container = st.empty()
        progress_container.info("Processing your research request...")
        
        # Make API request
        response = requests.post(
            f"{API_URL}/research",
            json={"topic": topic, "max_results": max_results}
        )
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            
            # Clear progress message
            progress_container.empty()
            
            # Display results in tabs
            tab1, tab2, tab3 = st.tabs(["Summary", "Details", "Raw Data"])
            
            with tab1:
                st.header("Research Summary")
                st.markdown(result["summary"])
                
                if result.get("critique"):
                    with st.expander("Research Critique"):
                        st.markdown(result["critique"])
            
            with tab2:
                st.header("Research Details")
                
                st.subheader("Subtopics Explored")
                for i, subtopic in enumerate(result["subtopics"]):
                    st.markdown(f"{i+1}. {subtopic}")
                
                st.subheader("Key Search Results")
                for i, result_item in enumerate(result["search_results"][:5]):
                    with st.expander(f"{i+1}. {result_item.get('title', 'No title')}"):
                        st.markdown(result_item.get("snippet", "No snippet available"))
                        st.markdown(f"[Source]({result_item.get('url', '#')})")
            
            with tab3:
                st.header("Raw Data")
                st.json(result)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Display instructions if no topic entered
if not topic:
    st.info("Enter a research topic above to get started.")
    
    # Example topics
    st.markdown("### Example Topics")
    example_topics = [
        "Quantum computing applications in healthcare",
        "Climate change adaptation strategies",
        "Artificial intelligence ethics",
        "Space tourism industry trends",
        "Blockchain technology in supply chain management"
    ]
    
    for example in example_topics:
        if st.button(example):
            # Use the URL to add the topic to the text input and submit
            st.query_params = {"topic": example}
            st.rerun() 