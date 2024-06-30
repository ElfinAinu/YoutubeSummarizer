# Unit tests for summarization.py

import pytest
from utils.summarization import generate_summary
from langgraph import LangGraph

def test_generate_summary(mocker):
    # Mock the LangGraph.summarize and self_reflect calls to return predefined responses
    mock_lg = mocker.Mock()
    mock_lg.summarize.return_value = "This is a test summary."
    mock_lg.self_reflect.return_value.is_satisfactory = True
    mocker.patch("langgraph.LangGraph", return_value=mock_lg)
    transcript = "This is a test transcript."
    summary = generate_summary(transcript)
    assert summary == "This is a test summary."

def test_generate_summary_unsatisfactory(mocker):
    # Mock the LangGraph.summarize, self_reflect, and rewrite_query calls to return predefined responses
    mock_lg = mocker.Mock()
    mock_lg.summarize.side_effect = ["Unsatisfactory summary.", "This is a test summary."]
    mock_lg.self_reflect.side_effect = [mocker.Mock(is_satisfactory=False), mocker.Mock(is_satisfactory=True)]
    mock_lg.rewrite_query.return_value = "Rewritten transcript."
    mocker.patch("langgraph.LangGraph", return_value=mock_lg)
    transcript = "This is a test transcript."
    summary = generate_summary(transcript)
    assert summary == "This is a test summary."
