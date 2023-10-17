from logger import logger
from query_service.query_engine import create_query_engine, query_summary
from resource_loader.json_loader import load_json_file_and_extract_text
from resource_loader.youtube_loader import YouTubeLoader
from transcription_service.transcriber import YouTubeTranscriber


# def youtube_loader(url, output_path_youtube, output_path_transcription):
#     # Resource Loader
#     yt_loader = YouTubeLoader(url, output_path_youtube)
#     yt_loader.download_youtube()
#
#     # Transcription Service
#     yt_transcriber = YouTubeTranscriber(yt_loader.media_id, yt_loader.filename, output_path_youtube,
#                                         output_path_transcription)
#     yt_transcriber.run()
#

import os


def check_file_exists(file_path):
    return os.path.exists(file_path)


def download_video(video_loader):
    logger.info("Initializing Resource Loader...")
    logger.info(f"Downloading video")
    video_loader.download()


def transcribe_video(video_loader, output_path, output_path_transcription):
    logger.info("Initializing Transcription Service...")
    yt_transcriber = YouTubeTranscriber(video_loader.media_id, video_loader.filename, output_path,
                                        output_path_transcription)
    logger.info(f"Transcribing video: {video_loader.media_id}")
    yt_transcriber.run()
    logger.info(f"Transcription completed and saved to {output_path_transcription}")


def load_transcription(yt_loader, output_path_transcription):
    logger.info("Loading JSON transcript...")
    document = load_json_file_and_extract_text(f"{output_path_transcription}/{yt_loader.media_id}.json")
    logger.info(f"JSON transcript loaded from {output_path_transcription}/{yt_loader.media_id}.json")
    return document


def create_and_query_engine(document):
    logger.info("Creating Query Engine...")
    query_engine = create_query_engine(document)
    logger.info("Query Engine created.")

    logger.info("Querying Summary...")
    response = query_summary(query_engine,
                             "What are the author's thoughts on the risks and benefits of AI for humanity")
    logger.info("Summary query completed.")
    return response
