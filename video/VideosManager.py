from typing import Dict
import os
from pathlib import Path

from video.Video import Video
from const import INPUT_VIDEO_FOLDER, VIDEO_EXTENSIONS

class VideosManager:
    videos: Dict[str, Video] = {}

    @staticmethod
    def refreshDatabase():
        VideosManager.videos.clear()
        for f in os.listdir(INPUT_VIDEO_FOLDER):
            if f.lower().endswith(VIDEO_EXTENSIONS):
                video = Video(Path(INPUT_VIDEO_FOLDER) / f)
                if video.hash not in VideosManager.videos:
                    VideosManager.videos[video.hash] = video

    @staticmethod
    def getVideo(hash: str) -> Video | None:
        return VideosManager.videos.get(hash, None)