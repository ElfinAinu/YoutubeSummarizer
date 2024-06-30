# YouTube Video Summarization Tool

## Overview
The YouTube Video Summarization Tool is a command-line application that leverages the Anthropic and OpenAI APIs, as well as the YouTube API, to generate summaries for YouTube videos. The tool supports three execution modes: single video, interactive mode, and playlist mode. The resulting summaries are saved in a specified output folder in Markdown format.

## Installation
To install the dependencies, run:
```sh
pip install -r requirements.txt
```

## Usage
### Single Video Mode
To summarize a single YouTube video, run:
```sh
python main.py single <YouTube video URL>
```
Example:
```sh
python main.py single https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Interactive Mode
To enter interactive mode, run:
```sh
python main.py interactive
```
You can then paste multiple YouTube video URLs. Type `exit` to quit.

### Playlist Mode
To summarize all videos in a YouTube playlist, run:
```sh
python main.py playlist <YouTube playlist URL>
```
Example:
```sh
python main.py playlist https://www.youtube.com/playlist?list=PLynG1JpD5GQ

## Configuration
Set up the following environment variables in `config.py`:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `YOUTUBE_API_KEY`
- `OUTPUT_FOLDER`

## Contributing
Guidelines for contributing to the project.

## License
License information.
