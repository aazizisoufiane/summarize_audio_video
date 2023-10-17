from abc import ABC, abstractmethod


class VideoLoaderInterface(ABC):

    @abstractmethod
    def download(self):
        pass

    @property
    @abstractmethod
    def extract_filename(self):
        pass
