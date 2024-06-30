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
Set up the following environment variables in your environment (e.g., using a `.env` file or exporting them in your shell):
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `YOUTUBE_API_KEY`
- `OUTPUT_FOLDER`

## Contributing
We welcome contributions to the YouTube Video Summarization Tool! Please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with clear and concise messages.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

Please ensure your code adheres to the existing style and includes tests for any new functionality.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
