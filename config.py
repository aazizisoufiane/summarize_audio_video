import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


script_dir = os.path.dirname(os.path.realpath(__file__))
output_path_youtube = os.path.join(script_dir, "youtube_videos")
output_path_transcription = os.path.join(script_dir, "transcriptions")

url = "https://www.youtube.com/watch?v=5p248yoa3oE"
