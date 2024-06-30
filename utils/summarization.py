from langgraph import LangGraph  # Corrected import statement
import config

def generate_summary(transcript):
    # Use StateGraph to generate summary from transcript
    if config.LLM_PROVIDER == "openai":
        lg = LangGraph(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    elif config.LLM_PROVIDER == "anthropic":
        lg = LangGraph(api_key=config.ANTHROPIC_API_KEY, model=config.ANTHROPIC_MODEL)
    else:
        raise ValueError("Invalid LLM provider specified in config.py")
    
    while True:
        summary = lg.summarize(transcript)
        reflection = lg.self_reflect(summary)
        
        if reflection.is_satisfactory:
            return summary
        else:
            transcript = lg.rewrite_query(transcript)
