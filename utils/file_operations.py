# Functions for file operations

import os

def save_summary(summary, output_path):
    # Save the generated summary to a file in Markdown format
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    file_path = os.path.join(output_path, "summary.md")
    with open(file_path, "w") as file:
        file.write(f"# Summary\n\n{summary}")
