from typing import Dict, List

from ffmpegProcess.FfmpegHandler import FfmpegHandler
from ffmpegProcess.FfmpegState import FfmpegState


class FfmpegManager:
    running_processes: Dict[str, FfmpegHandler] = dict()
    waiting_processes: List[str] = list()
    completed_processes: Dict[str, FfmpegHandler] = dict()

    @staticmethod
    def startFfmpeg(hash: str):
        if hash in FfmpegManager.running_processes:
            raise Exception("Process already running")

        if len(FfmpegManager.running_processes) > 0:
            FfmpegManager.addToWaitingQueue(hash)
            return

        ffmpeg_handler = FfmpegHandler(hash)
        FfmpegManager.running_processes[hash] = ffmpeg_handler
        ffmpeg_handler.start()

        FfmpegManager.completed_processes[hash] = ffmpeg_handler
        del FfmpegManager.running_processes[hash]

        if len(FfmpegManager.waiting_processes) > 0:
            next_hash = FfmpegManager.waiting_processes.pop(0)
            FfmpegManager.startFfmpeg(next_hash)

    @staticmethod
    def addToWaitingQueue(hash: str):
        if hash in FfmpegManager.running_processes:
            raise Exception("Process already running")
        FfmpegManager.waiting_processes.append(hash)

    @staticmethod
    def _getProcess(hash: str) -> FfmpegHandler | None:
        if hash in FfmpegManager.running_processes:
            return FfmpegManager.running_processes[hash]
        if hash in FfmpegManager.completed_processes:
            return FfmpegManager.completed_processes[hash]
        return None

    @staticmethod
    def getProgress(hash: str) -> float:
        process = FfmpegManager._getProcess(hash)
        if process is None:
            return 0

        return process.getProgress()

    @staticmethod
    def getStatus(hash: str) -> str:
        process = FfmpegManager._getProcess(hash)
        if process is not None:
            return process.getState().value
        if hash in FfmpegManager.waiting_processes:
            return FfmpegState.PENDING.value

        return ""

    @staticmethod
    def getTimeRemaining(hash: str) -> str:
        process = FfmpegManager._getProcess(hash)
        if process is not None:
            return process.getTimeRemaining()
        if hash in FfmpegManager.waiting_processes:
            return f"Place : {FfmpegManager.waiting_processes.index(hash) + 1}"

        return ""
