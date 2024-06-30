# Functions for generating summaries

from langgraph.langgraph import LangGraph
import config

def generate_summary(transcript):
    # Use LangGraph to generate summary from transcript
    if config.LLM_PROVIDER == "openai":
        lg = LangGraph(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    elif config.LLM_PROVIDER == "anthropic":
        lg = LangGraph(api_key=config.ANTHROPIC_API_KEY, model=config.ANTHROPIC_MODEL)
    
    while True:
        summary = lg.summarize(transcript)
        reflection = lg.self_reflect(summary)
        
        if reflection.is_satisfactory:
            return summary
        else:
            transcript = lg.rewrite_query(transcript)
