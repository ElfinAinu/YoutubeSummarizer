# Configuration settings for the application

import os

# Load API keys from environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Output folder path
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'output')
# Preferred model for LangGraph
LANGGRAPH_MODEL = os.getenv('LANGGRAPH_MODEL', 'default_model')

# Preferred LLM provider and model
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'openai')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-3.5')

def check_config():
    required_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'YOUTUBE_API_KEY', 'OUTPUT_FOLDER']
    required_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'YOUTUBE_API_KEY', 'OUTPUT_FOLDER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
