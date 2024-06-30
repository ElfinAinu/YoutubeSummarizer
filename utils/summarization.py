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
    yaml_frontmatter: str

def generate_outline(state):
    transcript = state['transcript']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""Create a comprehensive and well-thought-out outline of the following transcript in markdown format.
                            Your product is not necessarily intended to be short, but rather to be a comprehensive and well-thought-out 
                            outline of the content presented in the transcript.
                            The outline should be detailed and reflect the key points and structure of the content presented in the transcript. 
                            Consider the subject matter and what the viewer is intended to take from the content: {transcript}""")
    outline = response.content  # Access the content attribute directly
    return {"outline": outline}

def call_model(state):
    transcript = state['transcript']
    guidance = state['guidance']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""{guidance}\n\nSummarize the following transcript, your intention is not necessarily to be brief, 
                            but rather to be a comprehensive and well-thought-out summary of the content presented in the 
                            transcript, giving the reader an alternative to watching the original video, 
                            and a resource to review as a comprehension aid: {transcript}""")
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
    response = model.invoke(f"""Produce an additional section to be appended to the referenced summary.
                            Your product should be in markdown format and clearly marked as 'Expanded Info'
                            Expand on the summary to provide more detailed insights and explanations 
                            *BUT DO NOT REPEAT THE CONTENT OF THE ORIGINAL SUMMARY*
                            Do not reproduce the glossary or any other content that was already in the original summary.
                            Include practical examples, analogies, and real-world applications where appropriate.
                            Ensure the expanded content is comprehensive and enhances the reader's understanding of the subject matter.
                            Structure your additions in a way that is easy to read and understand.
                            : {summary}""")
    expanded_summary = response.content  # Access the content attribute directly
    return {"expanded_summary": expanded_summary}

def generate_yaml_frontmatter(state):
    transcript = state['transcript']
    # Read the YAML format guidance from the file
    with open('utils/yaml_format.md', 'r') as file:
        yaml_format = file.read()
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""Generate a yaml frontmatter for the following transcript, do not wrap the yaml frontmatter in any markdown formatting. 
                             Use the following format as a guide:
                             {yaml_format}
                             : {transcript}""")
    yaml_frontmatter = response.content  # Access the content attribute directly
    return {"yaml_frontmatter": yaml_frontmatter}


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
    graph.add_node("generate_yaml_frontmatter", generate_yaml_frontmatter)  # Add generate_yaml_frontmatter step
    
    # Set the entry point and finish point
    graph.set_entry_point("generate_outline")
    graph.set_finish_point("generate_yaml_frontmatter")
    
    # Add edges between nodes
    graph.add_edge("generate_outline", "summarize")
    graph.add_edge("summarize", "critique_step")
    graph.add_edge("critique_step", "re_summarize")
    graph.add_edge("re_summarize", "expound_summary")
    graph.add_edge("expound_summary", "generate_yaml_frontmatter")  # Add edge to generate_yaml_frontmatter
    
    # Compile the graph
    compiled_graph = graph.compile()
    
    # Run the graph with the input transcript and guidance
    result = compiled_graph.invoke({"transcript": transcript, "guidance": guidance})
    
    # Combine the expanded summary and yaml frontmatter
    combined_result = f"{result['yaml_frontmatter']}\n\n{result['summary']}\n\n{result['expanded_summary']}"
    
    return combined_result