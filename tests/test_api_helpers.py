# Unit tests for api_helpers.py

import pytest
from utils.api_helpers import fetch_video_transcript, fetch_playlist_videos

def test_fetch_video_transcript(mocker):
    # Mock the requests.get call to return a predefined response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "snippet": {
                    "text": "This is a test transcript."
                }
            }
        ]
    }
    mocker.patch("requests.get", return_value=mock_response)
    transcript = fetch_video_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert transcript == "This is a test transcript."

def test_fetch_playlist_videos(mocker):
    # Mock the requests.get call to return a predefined response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "snippet": {
                    "resourceId": {
                        "videoId": "dQw4w9WgXcQ"
                    }
                }
            }
        ]
    }
    mocker.patch("requests.get", return_value=mock_response)
    video_urls = fetch_playlist_videos("https://www.youtube.com/playlist?list=PLynG1JpD5GQ")
    assert video_urls == ["dQw4w9WgXcQ"]
