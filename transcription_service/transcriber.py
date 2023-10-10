import json

import torch
import whisper

from logger import logger


class YouTubeTranscriber:
    def __init__(self, video_id, filename, output_path_youtube, output_path_transcription, device=None):
        self.video_id = video_id
        self.filename = filename
        self.output_path_transcription = output_path_transcription
        self.transcription = None
        self.output_path_youtube = output_path_youtube
        if not device:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def transcribe_audio(self, model_name):
        audio = whisper.load_audio(f"{self.output_path_youtube}/{self.filename}")
        model = whisper.load_model(model_name, device=self.device)
        self.transcription = whisper.transcribe(model, audio, word_timestamps=True)

    def write_to_json(self):
        with open(f"{self.output_path_transcription}/{self.video_id}.json", "w") as f:
            json.dump(self.transcription, f)
        logger.info(f"Transcription downloaded to {self.output_path_transcription}/{self.video_id}.json")

    def merge_segments(self, num_to_merge):
        merged_segments = []
        segments = self.transcription["segments"]
        for i in range(0, len(segments), num_to_merge):
            merged_dict = {}
            slice_ = segments[i: i + num_to_merge]

            # Merging the 'text' fields
            merged_dict["text"] = " ".join(item["text"] for item in slice_)

            # Get the 'start' time from the first dictionary and the 'end' time from the last dictionary
            merged_dict["start"] = int(slice_[0]["start"])
            merged_dict["end"] = int(slice_[-1]["end"])

            merged_segments.append(merged_dict)

        self.transcription["merged_segments"] = merged_segments

    def run(self, number_to_merge=4, model_name="base"):
        logger.info("transcribe_audio")
        self.transcribe_audio(model_name=model_name)

        logger.info("merge_segments")
        self.merge_segments(number_to_merge)

        logger.info("write_to_json")
        self.write_to_json()
