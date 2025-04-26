import os

INPUT_VIDEO_FOLDER = '/srv/samba/OptiVideo/videos/input'
OUTPUT_VIDEO_FOLDER = '/srv/samba/OptiVideo/videos/output'

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Extensions de fichiers vidéo prises en charge
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mkv', '.mov')