import hashlib

from config import output_path_video
from logger import logger
from resource_loader.video_loader_interface import VideoLoaderInterface


class UploadedVideoLoader(VideoLoaderInterface):
    def __init__(self, uploaded_video_stream, original_name):
        self.uploaded_video_stream = uploaded_video_stream
        self.original_name = original_name
        self.video_id = None
        self.filename = None
        self.extract_filename()

    def extract_filename(self):
        self.filename = self.original_name.split(" - ", 1)[1]

        # Remove the file extension to get the video name
        self.video_id = self.filename.rsplit(".", 1)[0]  # return self.original_name

    def _hash_filename(self, original_name):
        return hashlib.sha256(original_name.encode()).hexdigest()

    def download(self):
        # Here you can implement how you want to handle or process the downloaded video
        # For now, I'll just log the filename
        with open(f"{output_path_video}/{self.filename}", "wb") as f:
            f.write(self.uploaded_video_stream.getvalue())
        logger.info(f"Video processed: {self.original_name}")
