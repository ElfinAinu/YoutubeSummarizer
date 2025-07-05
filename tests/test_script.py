#!/usr/bin/env python3
"""
Test script for YouTube Summarizer
Tests the tool with a specific YouTube video or mock transcript
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def main():
    """Test the YouTube summarizer with a specific video or mock transcript."""
    
    parser = argparse.ArgumentParser(description='Test YouTube Summarizer')
    parser.add_argument('--mock', action='store_true', 
                       help='Use mock transcript instead of real YouTube video')
    parser.add_argument('--url', default='https://youtu.be/FFfxT09W6D0',
                       help='YouTube URL to test (default: https://youtu.be/FFfxT09W6D0)')
    
    args = parser.parse_args()
    
    print("🧪 Testing YouTube Summarizer")
    if args.mock:
        print("📄 Using mock transcript from tests/mock_transcript.txt")
    else:
        print(f"📺 Video URL: {args.url}")
    print("=" * 50)
    
    # Change to parent directory if we're in tests/
    original_dir = os.getcwd()
    if Path.cwd().name == 'tests':
        os.chdir('..')
        print("📁 Changed to parent directory")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Are you in the correct directory?")
        sys.exit(1)
    
    # Check if config.json exists
    if not Path("config.json").exists():
        print("❌ Error: config.json not found. Please configure the application first.")
        sys.exit(1)
    
    # Check if API keys are configured
    try:
        import json
        with open("config.json", "r") as f:
            config = json.load(f)
        
        if (config.get("YOUTUBE_API_KEY") == "YOUR_YOUTUBE_API_KEY_HERE" or 
            config.get("OPENAI_API_KEY") == "YOUR_OPENAI_API_KEY_HERE"):
            print("❌ Error: API keys not configured. Please update config.json with your actual API keys.")
            print("📝 Required keys:")
            print("   - YOUTUBE_API_KEY")
            print("   - OPENAI_API_KEY (or ANTROPIC_API_KEY)")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error reading config.json: {e}")
        sys.exit(1)
    
    print("✅ Configuration looks good!")
    print("🚀 Running YouTube Summarizer...")
    print()
    
    # Run the main script
    try:
        if args.mock:
            # Set environment variable to use mock transcript
            env = os.environ.copy()
            env['USE_MOCK_TRANSCRIPT'] = 'true'
            env['MOCK_TRANSCRIPT_PATH'] = 'tests/mock_transcript.txt'
            result = subprocess.run([
                sys.executable, "main.py", "single", args.url
            ], capture_output=True, text=True, timeout=300, env=env)
        else:
            result = subprocess.run([
                sys.executable, "main.py", "single", args.url
            ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
            print("📄 Output:")
            print(result.stdout)
            
            # Check if output file was created
            output_files = list(Path(".").glob("*.md"))
            if output_files:
                print(f"📁 Generated files: {[f.name for f in output_files]}")
            else:
                print("⚠️  No .md files found in current directory")
                
        else:
            print("❌ Test failed!")
            print(f"Return code: {result.returncode}")
            print("Error output:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Test timed out after 5 minutes")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()