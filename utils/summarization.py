# Functions for generating summaries

from langgraph import LangGraph
import config

def generate_summary(transcript):
    # Use LangGraph to generate summary from transcript
    lg = LangGraph(api_key=config.ANTHROPIC_API_KEY)
    summary = lg.summarize(transcript)
    return summary
