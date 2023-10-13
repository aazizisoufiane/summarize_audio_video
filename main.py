from config import output_path_youtube, output_path_transcription
from keyword_retriever.keyword_retreiver import VideoRetriever
from logger import logger
from query_service.query_engine import create_query_engine, query_summary
from resource_loader.json_loader import load_json_file_and_extract_text
from resource_loader.youtube_loader import YouTubeLoader
from transcription_service.transcriber import YouTubeTranscriber


def youtube_loader(url, output_path_youtube, output_path_transcription):
    # Resource Loader
    yt_loader = YouTubeLoader(url, output_path_youtube)
    yt_loader.download_youtube()

    # Transcription Service
    yt_transcriber = YouTubeTranscriber(yt_loader.video_id, yt_loader.filename, output_path_video,
                                        output_path_transcription)
    yt_transcriber.run()


import os


def check_file_exists(file_path):
    return os.path.exists(file_path)


def download_video(yt_loader, output_path_youtube):
    logger.info("Initializing Resource Loader...")
    logger.info(f"Downloading video from URL: {yt_loader.url}")
    yt_loader.download_youtube()
    logger.info(f"Video downloaded to {output_path_youtube}")


def transcribe_video(yt_loader, output_path_youtube, output_path_transcription):
    logger.info("Initializing Transcription Service...")
    yt_transcriber = YouTubeTranscriber(yt_loader.video_id, yt_loader.filename, output_path_youtube,
                                        output_path_transcription)
    logger.info(f"Transcribing video: {yt_loader.video_id}")
    yt_transcriber.run()
    logger.info(f"Transcription completed and saved to {output_path_transcription}")


def load_transcription(yt_loader, output_path_transcription):
    logger.info("Loading JSON transcript...")
    document = load_json_file_and_extract_text(f"{output_path_transcription}/{yt_loader.video_id}.json")
    logger.info(f"JSON transcript loaded from {output_path_transcription}/{yt_loader.video_id}.json")
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


def factory(url):
    yt_loader = YouTubeLoader(url, output_path_youtube)

    video_file_path = os.path.join(output_path_youtube, f"{yt_loader.video_id}.mp3")
    transcription_file_path = os.path.join(output_path_transcription, f"{yt_loader.video_id}.json")

    if not check_file_exists(video_file_path):
        download_video(yt_loader, output_path_youtube)
    else:
        logger.info(f"Video already downloaded: {video_file_path}")

    if not check_file_exists(transcription_file_path):
        transcribe_video(yt_loader, output_path_youtube, output_path_transcription)
    else:
        logger.info(f"Transcription already exists: {transcription_file_path}")

    docs = load_transcription(yt_loader, output_path_transcription)

    logger.info(f"Build retriever")

    retriever = VideoRetriever(video_id=f"transcriptions/{yt_loader.video_id}")
    return retriever

    result = create_and_query_engine(docs)
    print(result)


if __name__ == "__main__":
    main("https://www.youtube.com/watch?v=vw-KWfKwvTQ")
