# Functions for file operations

import os

import re

def sanitize_title(title):
    # Remove invalid characters from the title
    return re.sub(r'[\\/*?:"<>|]', "", title)

def save_summary(summary, output_path, video_title):
    # Save the generated summary to a file in Markdown format
    logging.info(f"Checking if output path {output_path} exists...")
    if not os.path.exists(output_path):
        logging.info(f"Output path {output_path} does not exist. Creating directory...")
        os.makedirs(output_path)
    sanitized_title = sanitize_title(video_title)
    file_path = os.path.join(output_path, f"{sanitized_title}.md")
    logging.info(f"Saving summary to file: {file_path}")
    with open(file_path, "w") as file:
        logging.info("Summary saved successfully.")
        file.write(f"# Summary\n\n{summary}")
