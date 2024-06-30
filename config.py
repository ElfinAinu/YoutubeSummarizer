# Configuration settings for the application

import os

# Load API keys from environment variables
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Output folder path
OUTPUT_FOLDER = os.getenv('OUTPUT_FOLDER', 'output')
