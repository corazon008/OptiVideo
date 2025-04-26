from enum import Enum

class FfmpegState(Enum):
    NOT_STARTED = "Not started"
    IN_PROGRESS = "Processing"
    PENDING = "Waiting"
    COMPLETED = "Completed"
    FAILED = "Failed"