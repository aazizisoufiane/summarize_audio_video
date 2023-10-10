from urllib.parse import urlparse, parse_qs

from pytube import YouTube

from logger import logger


class YouTubeLoader:
    def __init__(self, url, output_path_youtube):
        self.url = url
        self.output_path_youtube = output_path_youtube
        self.yt = YouTube(url)
        self.filename = None
        self.video_id = None
        self.extract_main_domain_and_video_id()


    def extract_main_domain_and_video_id(self):
        parsed_url = urlparse(self.url)
        domain_parts = parsed_url.netloc.split(".")
        main_domain = domain_parts[-2] if len(domain_parts) >= 2 else None
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [None])[0]
        self.video_id = f"{main_domain}_{video_id}"

    def extract_main_domain_and_video_id(self):
        parsed_url = urlparse(self.url)
        domain_parts = parsed_url.netloc.split(".")
        main_domain = domain_parts[-2] if len(domain_parts) >= 2 else None
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get("v", [None])[0]
        self.video_id = f"{main_domain}_{video_id}"

    def download_youtube(self):
        self.extract_main_domain_and_video_id()
        self.filename = f"{self.video_id}.mp3"
        audio_stream = self.yt.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=self.output_path_youtube, filename=self.filename)
        logger.info(f"Audio downloaded to {self.output_path_youtube}/{self.filename}")
