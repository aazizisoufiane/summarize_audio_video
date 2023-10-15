import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


script_dir = os.path.dirname(os.path.realpath(__file__))

# Define the output paths
output_path_video = os.path.join(script_dir, "videos")
output_path_transcription = os.path.join(script_dir, "transcriptions")

# Check if the directories exist, create them if they don't
if not os.path.exists(output_path_video):
    os.makedirs(output_path_video)

if not os.path.exists(output_path_transcription):
    os.makedirs(output_path_transcription)