# Functions for generating summaries

from langgraph import LangGraph
import config

def generate_summary(transcript):
    # Use LangGraph to generate summary from transcript
    lg = LangGraph(api_key=config.ANTHROPIC_API_KEY)
    
    while True:
        summary = lg.summarize(transcript)
        reflection = lg.self_reflect(summary)
        
        if reflection.is_satisfactory:
            return summary
        else:
            transcript = lg.rewrite_query(transcript)
