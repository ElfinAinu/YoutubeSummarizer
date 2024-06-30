# Helper functions for interacting with APIs

import requests
import json
import config

def fetch_video_transcript(video_url):
    # Use YouTube API to fetch video transcript
    video_id = extract_video_id(video_url)
    api_url = f"https://www.googleapis.com/youtube/v3/captions?videoId={video_id}&key={config.YOUTUBE_API_KEY}"
    response = requests.get(api_url)
    if response.status_code == 200:
        transcript_data = response.json()
        return transcript_data['items'][0]['snippet']['text']
    else:
        raise Exception("Failed to fetch video transcript")

def fetch_playlist_videos(playlist_url):
    # Use YouTube API to fetch all videos in a playlist
    playlist_id = extract_playlist_id(playlist_url)
    api_url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&key={config.YOUTUBE_API_KEY}&part=snippet&maxResults=50"
    response = requests.get(api_url)
    if response.status_code == 200:
        playlist_data = response.json()
        video_urls = [item['snippet']['resourceId']['videoId'] for item in playlist_data['items']]
        return video_urls
    else:
        raise Exception("Failed to fetch playlist videos")

def extract_video_id(url):
    # Extract video ID from YouTube URL
    return url.split("v=")[-1]

def extract_playlist_id(url):
    # Extract playlist ID from YouTube URL
    return url.split("list=")[-1]
