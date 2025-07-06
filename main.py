# Entry point for the YouTube Video Summarization Tool

import sys
import argparse
import config
import logging
from utils.api_helpers import fetch_video_transcript, fetch_playlist_videos
from utils.summarization import generate_summary
from utils.file_operations import save_summary
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="YouTube Video Summarization Tool")
    parser.add_argument(
        "mode",
        choices=["single", "interactive", "playlist", "config"],
        help="Mode of operation",
    )
    parser.add_argument("url", nargs="?", help="YouTube video or playlist URL")
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM provider to use",
    )
    parser.add_argument("--model", help="Model to use for the selected LLM provider")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    logging.info("Checking configuration...")
    config.check_config()
    logging.info("Configuration check complete.")

    logging.info(f"Mode: {args.mode}")

    if args.mode == "config":
        logging.info("Entering configuration mode...")
        configure()
        logging.info("Configuration complete.")
        sys.exit(0)

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
        process_video(args.url)
    elif args.mode == "interactive":
        while True:
            url = input("Enter YouTube video URL (or 'exit' to quit): ")
            if url.lower() == "exit" or url == "":
                break
            process_video(url)
    elif args.mode == "playlist":
        if not args.url:
            print("Error: URL is required for playlist mode")
            sys.exit(1)
        videos = fetch_playlist_videos(args.url)  # No need to pass the API key
        for video in videos:
            process_video(video)


def configure():
    print("Select LLM Provider:")
    print("1. OpenAI")
    print("2. Anthropic")
    provider_choice = input("Enter choice (1 or 2): ")

    if provider_choice == "1":
        config.LLM_PROVIDER = "openai"
        config.OPENAI_MODEL = input("Enter OpenAI model (default: gpt-4): ") or "gpt-4"
    elif provider_choice == "2":
        config.LLM_PROVIDER = "anthropic"
        config.ANTHROPIC_MODEL = (
            input("Enter Anthropic model (default: claude-3.5): ") or "claude-3.5"
        )
    else:
        print("Invalid choice. Exiting.")
        return

    config.LANGGRAPH_MODEL = (
        input("Enter LangGraph model (default: default_model): ") or "default_model"
    )

    config.YOUTUBE_API_KEY = input("Enter YouTube API key: ") or config.YOUTUBE_API_KEY
    config.LIEUTUBE_PARENT_DIRECTORY = (
        input("Enter output folder (default: output): ") or "output"
    )

    config_data = {
        "YOUTUBE_API_KEY": config.YOUTUBE_API_KEY,
        "LIEUTUBE_PARENT_DIRECTORY": config.LIEUTUBE_PARENT_DIRECTORY,
        "LLM_PROVIDER": config.LLM_PROVIDER,
        "OPENAI_MODEL": config.OPENAI_MODEL,
        "ANTHROPIC_MODEL": config.ANTHROPIC_MODEL,
        "LANGGRAPH_MODEL": config.LANGGRAPH_MODEL,
    }
    config.save_config(config_data)
    print("Configuration saved successfully.")


def process_video(url):
    """Process a single video URL and save the summary."""
    logging.info(f"Fetching video transcript for URL: {url}")
    video_details = fetch_video_transcript(url)
    logging.info(f"Fetched video title: {video_details['title']}")
    logging.info(f"Fetched video URL: {video_details['url']}")
    
    transcript_preview = (
        video_details["transcript"][:100] + "..."
        if len(video_details["transcript"]) > 100
        else video_details["transcript"]
    )
    logging.info(f"Fetched video transcript preview: {transcript_preview}")
    
    transcript = video_details["transcript"]
    logging.info("Generating summary...")
    
    summary = generate_summary(
        transcript,
        video_details["title"],
        video_details["url"],
        video_details["video_id"],
        datetime.now().strftime("%Y-%m-%d_%H%M%S"),
    )
    logging.info("Summary generated.")
    
    video_title = video_details["title"]
    logging.info(
        f"Saving summary to {config.LIEUTUBE_PARENT_DIRECTORY} with title {video_title}"
    )
    save_summary(summary, config.LIEUTUBE_PARENT_DIRECTORY, video_title)
    logging.info("Summary saved.")


if __name__ == "__main__":
    main()
