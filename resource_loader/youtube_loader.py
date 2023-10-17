from urllib.parse import urlparse, parse_qs

from pytube import YouTube

from logger import logger
from resource_loader.video_loader_interface import VideoLoaderInterface


class YouTubeLoader(VideoLoaderInterface):
    def __init__(self, url, output_path_youtube):
        self.filename = None
        self.media_id = None
        self.url = url
        self.output_path_youtube = output_path_youtube
        self.yt = YouTube(url)
        self.extract_filename()

    def extract_filename(self):
        parsed_url = urlparse(self.url)
        domain_parts = parsed_url.netloc.split(".")
        main_domain = domain_parts[-2] if len(domain_parts) >= 2 else None
        query_params = parse_qs(parsed_url.query)
        media_id = query_params.get("v", [None])[0]
        self.media_id = f"{main_domain}_{media_id}"
        self.filename = f"{self.media_id}.mp3"

    def download(self):
        audio_stream = self.yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=self.output_path_youtube, filename=self.filename)
        logger.info(f"Audio downloaded to {self.output_path_youtube}/{self.filename}")
