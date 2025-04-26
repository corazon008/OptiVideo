import os, hashlib, datetime
from ffmpeg import FFmpeg
import json
from pathlib import Path
from const import OUTPUT_VIDEO_FOLDER
from utils import durationStringToSeconds




class Video:
    def __init__(self, path: Path | str):
        if isinstance(path, str):
            path = Path(path)

        ffprobe = FFmpeg(executable="ffprobe").input(
            path,
            print_format="json",  # ffprobe will output the results in JSON format
            show_streams=None,
        )

        media = json.loads(ffprobe.execute())
        print(path.name)
        print(media)
        self.name: str = path.name
        self.size: float = round(os.path.getsize(path) / 10 ** 9, 2)
        self._path: Path = path
        duration = 0
        for stream in media['streams']:
            if 'duration' in list(stream.keys()):
                duration = stream['duration']
                break
            try:
                duration = durationStringToSeconds(stream["tags"]["DURATION"])
            except:
                pass
        self.duration: datetime.timedelta = datetime.timedelta(seconds=int(float(duration)))
        self.hash: str = hashlib.sha1(path.name.encode()).hexdigest()

    def getInputPath(self) -> Path:
        return self._path

    def getOutputPath(self) -> Path:
        name, ext = self._path.stem, self._path.suffix
        # Mettre tous dans des mp4
        output_path = Path(os.path.join(OUTPUT_VIDEO_FOLDER, name + ".mp4"))
        return output_path


if __name__ == "__main__":
    video = Video("/srv/samba/OptiVideo/videos/input/sony-pictures-4k-movies1.mkv")
    print(video.name)
    print(video.size)
    print(video.duration)
