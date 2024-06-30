# Running the YouTube Video Summarization Tool

## Overview
The YouTube Video Summarization Tool is a command-line application that leverages the Anthropic and OpenAI APIs, as well as the YouTube API, to generate summaries for YouTube videos. The tool supports three execution modes: single video, interactive mode, and playlist mode. The resulting summaries are saved in a specified output folder in Markdown format.

## Prerequisites
Ensure you have all the dependencies installed. You can install them using:
```sh
pip install -r requirements.txt
```

## Configuration
Set up the following environment variables in your environment (e.g., using a `.env` file or exporting them in your shell):
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `YOUTUBE_API_KEY`
- `LIEUTUBE_PARENT_DIRECTORY`

Example of setting environment variables in a `.env` file:
```sh
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key
YOUTUBE_API_KEY=your_youtube_api_key
LIEUTUBE_PARENT_DIRECTORY=output
```

## Running the Program

### Single Video Mode
To summarize a single YouTube video, run:
```sh
python main.py single <YouTube video URL>
```
Example:
```sh
python main.py single https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
This will fetch the transcript of the video, generate a summary, and save it in the specified output folder.

### Interactive Mode
To enter interactive mode, run:
```sh
python main.py interactive
```
You can then paste multiple YouTube video URLs. Type `exit` to quit.

Example:
```sh
python main.py interactive
Enter YouTube video URL (or 'exit' to quit): https://www.youtube.com/watch?v=dQw4w9WgXcQ
Enter YouTube video URL (or 'exit' to quit): exit
```
This will fetch the transcript of each video, generate a summary, and save it in the specified output folder.

### Playlist Mode
To summarize all videos in a YouTube playlist, run:
```sh
python main.py playlist <YouTube playlist URL>
```
Example:
```sh
python main.py playlist https://www.youtube.com/playlist?list=PLynG1JpD5GQ
```
This will fetch the transcripts of all videos in the playlist, generate summaries, and save them in the specified output folder.

## Advanced Configuration
You can specify the LLM provider and model to use for generating summaries. The supported providers are `openai` and `anthropic`.

### Specifying LLM Provider and Model
To specify the LLM provider and model, use the `--provider` and `--model` options:
```sh
python main.py single <YouTube video URL> --provider <provider> --model <model>
```
Example:
```sh
python main.py single https://www.youtube.com/watch?v=dQw4w9WgXcQ --provider openai --model gpt-4
```

### Verbose Logging
To enable verbose logging, use the `--verbose` option:
```sh
python main.py single <YouTube video URL> --verbose
```
Example:
```sh
python main.py single https://www.youtube.com/watch?v=dQw4w9WgXcQ --verbose
```

## Examples

### Example 1: Summarizing a Single Video
```sh
python main.py single https://www.youtube.com/watch?v=dQw4w9WgXcQ
```
Output:
```
Fetching transcript for video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Extracted video ID: dQw4w9WgXcQ
Making API request to URL: https://www.googleapis.com/youtube/v3/captions?videoId=dQw4w9WgXcQ&key=your_youtube_api_key
Received response with status code: 200
Summary saved to output/Video Title.md
```

### Example 2: Using Interactive Mode
```sh
python main.py interactive
```
Output:
```
Enter YouTube video URL (or 'exit' to quit): https://www.youtube.com/watch?v=dQw4w9WgXcQ
Fetching transcript for video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Extracted video ID: dQw4w9WgXcQ
Making API request to URL: https://www.googleapis.com/youtube/v3/captions?videoId=dQw4w9WgXcQ&key=your_youtube_api_key
Received response with status code: 200
Summary saved to output/Video Title.md
Enter YouTube video URL (or 'exit' to quit): exit
```

### Example 3: Summarizing a Playlist
```sh
python main.py playlist https://www.youtube.com/playlist?list=PLynG1JpD5GQ
```
Output:
```
Fetching videos for playlist URL: https://www.youtube.com/playlist?list=PLynG1JpD5GQ
Extracted playlist ID: PLynG1JpD5GQ
Making API request to URL: https://www.googleapis.com/youtube/v3/playlistItems?playlistId=PLynG1JpD5GQ&key=your_youtube_api_key&part=snippet&maxResults=50
Received response with status code: 200
Fetching transcript for video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Extracted video ID: dQw4w9WgXcQ
Making API request to URL: https://www.googleapis.com/youtube/v3/captions?videoId=dQw4w9WgXcQ&key=your_youtube_api_key
Received response with status code: 200
Summary saved to output/Video Title.md
...
```

## Conclusion
The YouTube Video Summarization Tool provides a convenient way to generate summaries for YouTube videos and playlists using advanced language models. By following the instructions and examples provided in this document, you can easily configure and run the tool to suit your needs.
