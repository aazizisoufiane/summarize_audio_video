from config import output_path_video, output_path_audio
from logger import logger
from resource_loader.video_loader_interface import VideoLoaderInterface


class UploadedMediaLoader(VideoLoaderInterface):
    def __init__(self, uploaded_stream, original_name, media_type='video'):
        self.uploaded_stream = uploaded_stream
        self.original_name = original_name
        self.media_type = media_type  # 'video' or 'audio'
        self.media_id = None
        self.filename = None
        self.output_path = None
        self.extract_filename()
        self.set_output_path()

    def extract_filename(self):
        self.filename = self.original_name.split(" - ", 1)[1]
        self.media_id = self.filename.rsplit(".", 1)[0]

    def set_output_path(self):
        if self.media_type == 'video':
            self.output_path = output_path_video
        elif self.media_type == 'audio':
            self.output_path = output_path_audio
        else:
            raise ValueError("Invalid media type")

    def download(self):
        with open(f"{self.output_path}/{self.filename}", "wb") as f:
            f.write(self.uploaded_stream.getvalue())
        logger.info(f"{self.media_type.capitalize()} processed: {self.original_name}")
