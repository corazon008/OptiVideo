from pathlib import Path

from const import *

def durationStringToSeconds(duration: str) -> float:
    """
    Convert a duration string in the format "HH:MM:SS" to seconds.
    """
    if not isinstance(duration, str):
        raise ValueError("Duration must be a string in the format 'HH:MM:SS'")

    parts = duration.split(":")
    if len(parts) != 3:
        raise ValueError("Duration must be in the format 'HH:MM:SS'")

    hours, minutes, seconds = map(float, parts)
    return hours * 3600 + minutes * 60 + seconds