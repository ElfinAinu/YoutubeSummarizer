# Unit tests for file_operations.py

import os
from utils.file_operations import save_summary

def test_save_summary(tmpdir):
    # Test saving summary to file
    summary = "This is a test summary."
    output_path = tmpdir.mkdir("output")
    save_summary(summary, str(output_path))
    file_path = os.path.join(str(output_path), "summary.md")
    assert os.path.exists(file_path)
    with open(file_path, "r") as file:
        content = file.read()
        assert content == "# Summary\n\nThis is a test summary."
