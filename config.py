# Configuration settings for the application

import os

# Load API keys from environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

import json

# Load configuration from JSON file
CONFIG_FILE = 'config.json'

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config_data = json.load(file)
            return config_data
    else:
        return {}

def save_config(config_data):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config_data, file, indent=4)

config_data = load_config()

# Output folder path
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'output')
# Preferred model for LangGraph
LANGGRAPH_MODEL = config_data.get('LANGGRAPH_MODEL', 'default_model')

# Preferred LLM provider and model
LLM_PROVIDER = config_data.get('LLM_PROVIDER', 'openai')
OPENAI_MODEL = config_data.get('OPENAI_MODEL', 'gpt-4')
ANTHROPIC_MODEL = config_data.get('ANTHROPIC_MODEL', 'claude-3.5')

def check_config():
    required_vars = ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'YOUTUBE_API_KEY', 'OUTPUT_FOLDER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
