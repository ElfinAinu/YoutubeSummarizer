from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
import config
from typing import TypedDict

class StateSchema(TypedDict):
    transcript: str
    summary: str
    guidance: str
    critique: str
    outline: str  # Added outline to the state schema
    expanded_summary: str

def generate_outline(state):
    transcript = state['transcript']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"Create a comprehensive and well-thought-out outline of the following transcript in markdown format. The outline should be detailed and reflect the key points and structure of the content presented in the transcript. Consider the subject matter and what the viewer is intended to take from the content: {transcript}")
    outline = response.content  # Access the content attribute directly
    return {"outline": outline}

def call_model(state):
    transcript = state['transcript']
    guidance = state['guidance']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"{guidance}\n\nSummarize the following transcript: {transcript}")
    summary = response.content  # Access the content attribute directly
    return {"summary": summary}

def critique_summary(state):
    summary = state['summary']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""Critique the following summary and suggest revisions and additions.
                            Produce a list of revisions and additions, and a brief explanation of each.
                            Consider the content of the transcript, the subject, and what the end-user is likely to
                            desire of the summary. It's ok to suggest revisions and additions that are not in the
                            original summary.
                            : {summary}""")
    critique = response.content  # Access the content attribute directly
    return {"critique": critique}

def expound_summary(state):
    summary = state['summary']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""Expand on the following summary to provide more detailed insights and explanations.
                            Include practical examples, analogies, and real-world applications where appropriate.
                            Ensure the expanded content is comprehensive and enhances the reader's understanding of the subject matter.
                            Differentiate the expanded content from the original summary so that it's clear to the reader what content
                            is being expanded and what is the originally from the video.
                            Use markdown formatting to separate the expanded content from the original summary.
                            : {summary}""")
    expanded_summary = response.content  # Access the content attribute directly
    return {"expanded_summary": expanded_summary}


def generate_summary(transcript):
    # Read the output guidance from the file
    with open('utils/output_guidance.md', 'r') as file:
        guidance = file.read()
    
    # Initialize the graph with state schema
    graph = StateGraph(StateSchema)
    
    # Add nodes to the graph
    graph.add_node("generate_outline", generate_outline)
    graph.add_node("summarize", call_model)
    graph.add_node("critique_step", critique_summary)
    graph.add_node("re_summarize", call_model)  # Re-run summarize step with critique input
    graph.add_node("expound_summary", expound_summary)  # Add expound_summary step
    
    # Set the entry point and finish point
    graph.set_entry_point("generate_outline")
    graph.set_finish_point("expound_summary")
    
    # Add edges between nodes
    graph.add_edge("generate_outline", "summarize")
    graph.add_edge("summarize", "critique_step")
    graph.add_edge("critique_step", "re_summarize")
    graph.add_edge("re_summarize", "expound_summary")  # Add edge to expound_summary
    
    # Compile the graph
    compiled_graph = graph.compile()
    
    # Run the graph with the input transcript and guidance
    result = compiled_graph.invoke({"transcript": transcript, "guidance": guidance})
    
    return result["expanded_summary"]