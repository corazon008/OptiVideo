from flask import Flask, jsonify, render_template
from threading import Thread

from ffmpegProcess.FfmpegManager import FfmpegManager
from video.VideosManager import VideosManager
app = Flask(__name__)

def background_task(hash:str):
    FfmpegManager.startFfmpeg(hash)
@app.route('/')
def index():
    VideosManager.refreshDatabase()
    return render_template("index.html", videos=VideosManager.videos.values())

@app.route('/start/<hash>')
def start_task(hash:str):
    Thread(target=background_task, args=(hash,)).start()
    return jsonify({'status': 'started'})

@app.route('/progresses')
def get_all_progress():
    progresses = {}
    for hash in VideosManager.videos.keys():
        progresses[hash] = {
            'progress': FfmpegManager.getProgress(hash),
            'state': FfmpegManager.getStatus(hash),
            'time': str(FfmpegManager.getTimeRemaining(hash))
        }
    return jsonify(progresses)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
