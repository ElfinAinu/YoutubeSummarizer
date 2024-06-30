# Functions for file operations

import os

import re

def sanitize_title(title):
    # Remove invalid characters from the title
    return re.sub(r'[\\/*?:"<>|]', "", title)

def save_summary(summary, output_path, video_title):
    # Save the generated summary to a file in Markdown format
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    sanitized_title = sanitize_title(video_title)
    file_path = os.path.join(output_path, f"{sanitized_title}.md")
    with open(file_path, "w") as file:
        file.write(f"# Summary\n\n{summary}")