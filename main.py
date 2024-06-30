# Entry point for the YouTube Video Summarization Tool

import sys
import argparse
import argparse
import sys
import config
from utils.api_helpers import fetch_video_transcript, fetch_playlist_videos
from utils.summarization import generate_summary
from utils.file_operations import save_summary

def main():
    config.check_config()
    parser = argparse.ArgumentParser(description="YouTube Video Summarization Tool")
    parser.add_argument("mode", choices=["single", "interactive", "playlist"], help="Mode of operation")
    parser.add_argument("url", nargs="?", help="YouTube video or playlist URL")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai", help="LLM provider to use")
    parser.add_argument("--model", help="Model to use for the selected LLM provider")
    args = parser.parse_args()

    # Set the LLM provider and model in the config
    config.LLM_PROVIDER = args.provider
    if args.model:
        if args.provider == "openai":
            config.OPENAI_MODEL = args.model
        elif args.provider == "anthropic":
            config.ANTHROPIC_MODEL = args.model

    if args.mode == "single":
        if not args.url:
            print("Error: URL is required for single video mode")
            sys.exit(1)
        transcript = fetch_video_transcript(args.url)
        summary = generate_summary(transcript)
        video_title = "Video Title"  # Fetch the actual video title here
        save_summary(summary, config.OUTPUT_FOLDER, video_title)
    elif args.mode == "interactive":
        while True:
            url = input("Enter YouTube video URL (or 'exit' to quit): ")
            if url.lower() == "exit":
                break
            transcript = fetch_video_transcript(url)
            summary = generate_summary(transcript)
            save_summary(summary, config.OUTPUT_FOLDER)
    elif args.mode == "playlist":
        if not args.url:
            print("Error: URL is required for playlist mode")
            sys.exit(1)
        videos = fetch_playlist_videos(args.url)
        for video in videos:
            transcript = fetch_video_transcript(video)
            summary = generate_summary(transcript)
            save_summary(summary, config.OUTPUT_FOLDER)

if __name__ == "__main__":
    main()
