import re
import logging
import os
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config  # Import the config module

def get_video_details(video_id):
    logging.info("Building YouTube API client...")
    youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)
    logging.info("YouTube API client built successfully.")
    logging.info(f"Fetching video details for video ID: {video_id}")
    request = youtube.videos().list(part='snippet', id=video_id)
    logging.info("Video details fetched successfully.")
    response = request.execute()

    if response['items']:
        video_details = response['items'][0]['snippet']
        title = video_details['title']
        channel_name = video_details['channelTitle']
        return title, channel_name
    else:
        return None, None

def fetch_video_transcript(video_url):
    # Check if we should use mock transcript
    if os.getenv('USE_MOCK_TRANSCRIPT') == 'true':
        return fetch_mock_transcript(video_url)
    
    # Use YouTubeTranscriptApi to fetch video transcript and details
    video_id = extract_video_id(video_url)
    logging.info(f"Extracted video ID: {video_id}")
    
    try:
        logging.info(f"Initiating transcript fetch for video ID: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        logging.info(f"Successfully fetched transcript for video ID: {video_id}")
        transcript_text = "\n".join([entry['text'] for entry in transcript])
        logging.info(f"Transcript preview: {transcript_text[:100]}...")  # Log the first 100 characters
        
        # Fetch video details using YouTube Data API
        logging.info(f"Fetching video details for video ID: {video_id}")
        title, channel_name = get_video_details(video_id)
        logging.info(f"Successfully fetched video details for video ID: {video_id}")
        video_info = {
            "title": title if title else 'N/A',
            "channel": channel_name if channel_name else 'N/A',
            "url": video_url,
            "video_id": video_id,
            "transcript": transcript_text
        }
        logging.info(f"Fetched video details: {video_info}")
        return video_info
        
    except HttpError as e:
        logging.error(f"HTTP error occurred: {e.resp.status} {e.content}")
        raise Exception("Failed to fetch video transcript")
    except Exception as e:
        logging.error(f"Failed to fetch video transcript for URL: {video_url}. Error: {e}")
        raise Exception("Failed to fetch video transcript")

def fetch_mock_transcript(video_url):
    """Load transcript from mock file for testing purposes."""
    mock_transcript_path = os.getenv('MOCK_TRANSCRIPT_PATH', 'tests/mock_transcript.txt')
    video_id = extract_video_id(video_url)
    
    logging.info(f"Using mock transcript from: {mock_transcript_path}")
    
    try:
        with open(mock_transcript_path, 'r', encoding='utf-8') as f:
            transcript_text = f.read()
        
        logging.info(f"Successfully loaded mock transcript ({len(transcript_text)} characters)")
        logging.info(f"Mock transcript preview: {transcript_text[:100]}...")
        
        video_info = {
            "title": "Mock Video: AI and Machine Learning Explained",
            "channel": "Mock Channel",
            "url": video_url,
            "video_id": video_id,
            "transcript": transcript_text
        }
        
        logging.info(f"Mock video details: {video_info}")
        return video_info
        
    except FileNotFoundError:
        logging.error(f"Mock transcript file not found: {mock_transcript_path}")
        raise Exception(f"Mock transcript file not found: {mock_transcript_path}")
    except Exception as e:
        logging.error(f"Failed to load mock transcript: {e}")
        raise Exception(f"Failed to load mock transcript: {e}")

def fetch_playlist_videos(playlist_url):
    # Use YouTube API to fetch all videos in a playlist
    logging.info(f"Fetching videos for playlist URL: {playlist_url}")
    playlist_id = extract_playlist_id(playlist_url)
    logging.info(f"Extracted playlist ID: {playlist_id}")
    
    logging.info("Building YouTube API client...")
    youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API_KEY)
    logging.info("YouTube API client built successfully.")
    
    try:
        logging.info(f"Fetching playlist items for playlist ID: {playlist_id}")
        logging.info("Playlist items fetched successfully.")
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()
        
        logging.info(f"Received response: {response}")
        
        if 'items' in response and len(response['items']) > 0:
            video_urls = [item['snippet']['resourceId']['videoId'] for item in response['items']]
            logging.info(f"Fetched video URLs: {video_urls}")
            return video_urls
        else:
            logging.error("Failed to fetch playlist videos for URL: %s. Response: %s", playlist_url, response)
            raise Exception("Failed to fetch playlist videos")
    except HttpError as e:
        logging.error(f"HTTP error occurred: {e.resp.status} {e.content}")
        raise Exception("Failed to fetch playlist videos")
    except Exception as e:
        logging.error(f"Failed to fetch playlist videos for URL: {playlist_url}. Error: {e}")
        raise Exception("Failed to fetch playlist videos")

def extract_video_id(input_value):
    # Check if the input is already a video ID
    if re.match(r'^[0-9A-Za-z_-]{11}$', input_value):
        logging.info(f"Input is already a video ID: {input_value}")
        return input_value
    
    # Extract video ID from YouTube URL using regex
    logging.info(f"Extracting video ID from URL: {input_value}")
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', input_value)
    logging.info(f"Extracted video ID: {video_id_match.group(1) if video_id_match else 'None'}")
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError(f"Invalid YouTube URL or video ID: {input_value}")

def extract_playlist_id(url):
    # Extract playlist ID from YouTube URL using regex
    logging.info(f"Extracting playlist ID from URL: {url}")
    playlist_id_match = re.search(r'[?&]list=([0-9A-Za-z_-]+)', url)
    logging.info(f"Extracted playlist ID: {playlist_id_match.group(1) if playlist_id_match else 'None'}")
    if playlist_id_match:
        return playlist_id_match.group(1)
    else:
        raise ValueError(f"Invalid YouTube URL: {url}")