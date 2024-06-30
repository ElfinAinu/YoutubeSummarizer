# Unit tests for summarization.py

import pytest
from utils.summarization import generate_summary
from langgraph import LangGraph

def test_generate_summary(mocker):
    # Mock the LangGraph.summarize call to return a predefined response
    mock_lg = mocker.Mock()
    mock_lg.summarize.return_value = "This is a test summary."
    mocker.patch("langgraph.LangGraph", return_value=mock_lg)
    transcript = "This is a test transcript."
    summary = generate_summary(transcript)
    assert summary == "This is a test summary."
