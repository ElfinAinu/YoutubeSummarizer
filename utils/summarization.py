from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI
import config
import logging
from typing import TypedDict
from datetime import datetime


def fill_yaml_frontmatter(title, url, video_id, date):
    yaml_frontmatter = f"""---
title: "{title}"
url: "{url}"
video_id: "{video_id}"
date: "{date}"
channel: "Channel Name"
references: ["Book Title", "Research Paper", "Other Video"]
tags: ["List", "Of", "Applicable", "Tags"]
categories: ["List", "Of", "Applicable", "Categories"]
---
"""
    return yaml_frontmatter

class StateSchema(TypedDict):
    transcript: str
    summary: str
    guidance: str
    critique: str
    outline: str
    expanded_summary: str
    yaml_frontmatter: str
    title: str
    url: str
    video_id: str
    date: str

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

def critique_outline(state):
    outline = state['outline']
    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""Critique the following outline and suggest improvements.
                            Consider the structure, completeness, and organization of the content.
                            Provide specific suggestions for enhancement.
                            : {outline}""")
    critique = response.content  # Access the content attribute directly
    return {"critique": critique}

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
    title = state['title']
    url = state['url']
    video_id = state['video_id']
    date = state['date']
    transcript = state['transcript']
    
    yaml_frontmatter = fill_yaml_frontmatter(title, url, video_id, date)

    model = ChatOpenAI(api_key=config.OPENAI_API_KEY, model=config.OPENAI_MODEL)
    response = model.invoke(f"""Generate the yaml frontmatter to help with categorization and searching for this summary in a large collection of obsidian notes.
                            Fence the yaml content between triple dashes `---`.  The yaml fencing `---` must begin at the very first character of your output. The yaml fencing `---` must be the very last part of your output. 
                            Do not place any additional content, headings, formatting or symbols in your output.
                            Return only that content.
                            The following frontmatter is prepopulated with video title, video_id, channel name, and the current date/time:
                             {yaml_frontmatter}
                             : {transcript}""")
    yaml_frontmatter = response.content
    return {"yaml_frontmatter": yaml_frontmatter}

def generate_summary(transcript, title, url, video_id, date):
    # Read the output guidance from the file
    logging.info("Reading output guidance from file...")
    with open('utils/output_guidance.md', 'r', encoding='utf-8') as file:
        logging.info("Output guidance read successfully.")
        guidance = file.read()
    
    # Initialize the graph with state schema
    logging.info("Initializing StateGraph with StateSchema...")
    graph = StateGraph(StateSchema)
    logging.info("StateGraph initialized.")
    
    # Add nodes to the graph
    graph.add_node("generate_outline", generate_outline)
    graph.add_node("summarize", call_model)
    graph.add_node("critique_outline", critique_outline)  # Critique step for outline
    graph.add_node("critique_summary", critique_summary)  # Critique step for summary
    graph.add_node("re_summarize", call_model)  # Re-run summarize step with critique input
    graph.add_node("expound_summary", expound_summary)  # Add expound_summary step
    graph.add_node("generate_yaml_frontmatter", generate_yaml_frontmatter)  # No input_keys argument
    
    # Set the entry point and finish point
    graph.set_entry_point("generate_outline")
    graph.set_finish_point("generate_yaml_frontmatter")
    
    # Add edges between nodes
    graph.add_edge("generate_outline", "critique_outline")  # First critique after outline
    graph.add_edge("critique_outline", "summarize")  # Summarize after first critique
    graph.add_edge("summarize", "critique_summary")  # Second critique after summarization
    graph.add_edge("critique_summary", "re_summarize")  # Re-summarize after second critique
    graph.add_edge("re_summarize", "expound_summary")
    graph.add_edge("expound_summary", "generate_yaml_frontmatter")  # Add edge to generate_yaml_frontmatter
    
    # Compile the graph
    logging.info("Compiling the graph...")
    compiled_graph = graph.compile()
    logging.info("Graph compiled successfully.")
    
    # Run the graph with the input transcript and guidance
    logging.info("Invoking the compiled graph with input data...")
    result = compiled_graph.invoke({
        "transcript": transcript,
        "guidance": guidance,
        "title": title,
        "url": url,
        "video_id": video_id,
        "date": date
    })
    logging.info("Graph invocation complete.")
    
    logging.info(f"Yaml frontmatter: {result['yaml_frontmatter']}")
    # Combine the expanded summary and yaml frontmatter
    cleaned_yaml_frontmatter = result['yaml_frontmatter'].replace("# Summary", "").replace("```yaml", "").replace("```", "").strip()
    combined_result = f"{cleaned_yaml_frontmatter}\n\n{result['summary']}\n\n{result['expanded_summary']}"
    
    logging.info("Summary generation complete.")
    return combined_result
