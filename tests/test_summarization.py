# Unit tests for summarization.py

import pytest
from utils.summarization import generate_summary

def test_generate_summary(mocker):
    # Mock the openai.Completion.create call to return a predefined response
    mock_response = mocker.Mock()
    mock_response.choices = [mocker.Mock(text="This is a test summary.")]
    mocker.patch("openai.Completion.create", return_value=mock_response)
    transcript = "This is a test transcript."
    summary = generate_summary(transcript)
    assert summary == "This is a test summary."
