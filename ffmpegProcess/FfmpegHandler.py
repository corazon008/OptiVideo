import datetime, time

from ffmpeg import FFmpeg, Progress

from video.VideosManager import VideosManager
from ffmpegProcess.FfmpegState import FfmpegState


class FfmpegHandler:
    def __init__(self, hash: str):
        self.hash = hash
        self.video = VideosManager.getVideo(hash)

        self.ffmpeg = (
            FFmpeg()
            .option("y")
            .input(self.video.getInputPath())
            .output(
                self.video.getOutputPath(),
                {"codec:v": "libx265", "codec:a": "aac", "b:a": "128k"},
                preset="medium",
                #vf="scale=-2:1080", # disable to keep original resolution
                crf=23,
            )
        )

        self.speed = -1
        self._progress: float = 0

        self._time_remaining: datetime.timedelta = datetime.timedelta(seconds=0)
        self._state: FfmpegState = FfmpegState.NOT_STARTED

        @self.ffmpeg.on("progress")
        def on_progress(progress: Progress):
            self._progress = progress.time / self.video.duration * 100
            self._elapsed_time = datetime.timedelta(seconds=int(progress.time.seconds))
            if self.speed <= 0 or (self.video.duration.seconds - progress.time.seconds) <= 0.1:
                self._time_remaining = 0
            else:
                self._time_remaining = datetime.timedelta(seconds=int((self.video.duration.seconds - progress.time.seconds) / self.speed))
            self.speed = progress.speed

    def start(self):
        self._state = FfmpegState.IN_PROGRESS
        print(f"{self.video.name} transcoding started")
        self.started_time = time.time()
        self.ffmpeg.execute()
        self._state = FfmpegState.COMPLETED
        print(f"{self.video.name} transcoding completed")
        self.finished_time = time.time()

    def getProgress(self) -> float:
        return self._progress

    def getState(self) -> FfmpegState:
        return self._state

    def getTimeRemaining(self) -> str | datetime.timedelta:
        if self.speed == 0:
            return "Error"
        if self._time_remaining == 0:
            return  datetime.timedelta(seconds=int(self.finished_time - self.started_time))
        return self._time_remaining


if __name__ == '__main__':
    from video.Video import Video

    video = Video("/srv/samba/OptiVideo/videos/input/sony-pictures-4k-movies1.mkv")
    ffmpeg_handler = FfmpegHandler(video.hash)
    ffmpeg_handler.start()
