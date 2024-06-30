import re
import logging
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi

def fetch_video_transcript(video_url):
    # Use YouTubeTranscriptApi to fetch video transcript and details
    logging.info(f"Fetching transcript for video URL: {video_url}")
    video_id = extract_video_id(video_url)
    logging.info(f"Extracted video ID: {video_id}")
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = "\n".join([entry['text'] for entry in transcript])
        logging.info(f"Fetched transcript: {transcript_text[:100]}...")  # Log the first 100 characters
        
        # Fetch video details using web scraping
        video_details = scrape_video_details(video_url)
        video_info = {
            "title": video_details.get('title', 'N/A'),
            "channel": video_details.get('channel', 'N/A'),
            "upload_date": video_details.get('upload_date', 'N/A'),
            "transcript": transcript_text
        }
        logging.info(f"Fetched video details: {video_info}")
        return video_info
        
    except Exception as e:
        logging.error(f"Failed to fetch video transcript for URL: {video_url}. Error: {e}")
        raise Exception("Failed to fetch video transcript")

def scrape_video_details(video_url):
    response = requests.get(video_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch video page. Status code: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract video title
    title_tag = soup.find('meta', {'name': 'title'})
    title = title_tag['content'] if title_tag else 'N/A'
    
    # Extract channel name
    channel_tag = soup.find('meta', {'itemprop': 'author'})
    channel = channel_tag['content'] if channel_tag else 'N/A'
    
    # Extract upload date
    upload_date_tag = soup.find('meta', {'itemprop': 'uploadDate'})
    upload_date = upload_date_tag['content'] if upload_date_tag else 'N/A'
    
    return {
        "title": title,
        "channel": channel,
        "upload_date": upload_date
    }

def fetch_playlist_videos(playlist_url):
    # Use YouTube API to fetch all videos in a playlist
    logging.info(f"Fetching videos for playlist URL: {playlist_url}")
    playlist_id = extract_playlist_id(playlist_url)
    logging.info(f"Extracted playlist ID: {playlist_id}")
    
    youtube = get_authenticated_service()
    
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    
    logging.info(f"Received response: {response}")
    
    if 'items' in response and len(response['items']) > 0:
        video_urls = [item['snippet']['resourceId']['videoId'] for item in response['items']]
        return video_urls
    else:
        logging.error("Failed to fetch playlist videos for URL: %s. Response: %s", playlist_url, response)
        raise Exception("Failed to fetch playlist videos")

def extract_video_id(url):
    # Extract video ID from YouTube URL using regex
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError(f"Invalid YouTube URL: {url}")

def extract_playlist_id(url):
    # Extract playlist ID from YouTube URL using regex
    playlist_id_match = re.search(r'(?:list=|\/)([0-9A-Za-z_-]{1}).*', url)
    if playlist_id_match:
        return playlist_id_match.group(1)
    else:
        raise ValueError(f"Invalid YouTube URL: {url}")