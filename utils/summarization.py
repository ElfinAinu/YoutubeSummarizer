# Functions for generating summaries

import openai

def generate_summary(transcript):
    # Use OpenAI API to generate summary from transcript
    openai.api_key = config.OPENAI_API_KEY
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following transcript:\n\n{transcript}",
        max_tokens=150
    )
    summary = response.choices[0].text.strip()
    return summary
