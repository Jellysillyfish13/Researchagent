author: Sicheng Bao
summary: Learn how to set up and run the Research Agent system for automated, AI-powered research
id: research-agent-setup-codelab
categories: AI, Research, LangGraph
environments: Web
status: Published

# Research Agent Setup Guide

## Overview
Duration: 5:00

### What You'll Learn
- How to clone and set up the Research Agent repository
- Installing dependencies using uv for faster package management
- Creating and activating a virtual environment
- Configuring necessary API keys
- Running your first research query

### Prerequisites
- Python 3.10 or higher
- Git installed on your system
- Basic familiarity with command line tools
- A SerpAPI key for web search capabilities
- A Google Gemini API key for AI capabilities


## Clone the Repository
Duration: 2:00

The first step is to clone the Research Agent repository to your local machine.

```bash
git clone git@github.com:Jellysillyfish13/Researchagent.git

```

This will create a local copy of the Research Agent project on your machine and navigate you into the project directory.

## Install uv Package Manager
Duration: 3:00

Research Agent uses uv, a fast Python package installer and resolver, to manage dependencies efficiently.

```bash
pip install uv
```

```bash
uv --version
```

uv is significantly faster than traditional pip and provides better dependency resolution, making it ideal for projects with complex dependencies like Research Agent.

## Create and Activate a Virtual Environment
Duration: 3:00

Creating a dedicated virtual environment helps isolate the project dependencies from your system Python.

Create a virtual environment
```bash
uv venv venv
```
Activate the virtual environment on Windows:
```bash
venv\Scripts\activate
```
On macOS/Linux:
```bash
source venv/bin/activate
```

Your command prompt should now show the virtual environment name, indicating that it's active.

## Install Dependencies
Duration: 5:00

With the virtual environment activated, install all the required dependencies using uv.
Check your vscode and make sure you are using the virtual env

```bash
which python
```

Then install the requirements
```bash
uv pip install -r requirements.txt
```

This will install all the packages listed in requirements.txt, including:
- LangGraph for workflow orchestration
- LiteLLM for model interfacing
- FastAPI (if you're using the API option)
- And other necessary libraries

## Configure API Keys
Duration: 5:00

Research Agent requires API keys for search and AI capabilities. You'll need to create a `.env` file in the project root.

```bash
touch .env
```

Open the `.env` file in your favorite text editor and add the following:

```ini
# API Keys
SERPAPI_API_KEY=your_serpapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```


### Getting API Keys

#### SerpAPI
- Visit [SerpAPI's website](https://serpapi.com/) and create an account
- Navigate to the API Keys section in your dashboard
- Copy your API key and paste it into the .env file

#### Google Gemini API
- Visit [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key?)
- Create an account if you don't already have one
- Generate an API key in the settings
- Copy your API key and paste it into the .env file



## Run Your First Research Query
Duration: 5:00

Now that everything is set up, let's run your first research query!

```bash
cd backend 
```
```bash
uvicorn main:app --reload 
```
Then open another terminal
```bash
cd frontend 
```
```bash
streamlit run app.py 
```


