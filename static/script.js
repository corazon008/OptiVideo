function refreshPage() {
    location.reload();
}

function startTranscode(taskId) {
    fetch(`/start/${taskId}`).then(() => {
        console.log(`Transcoding started for task ${taskId}`);
    });
}

function pollAllProgress() {
    const interval = setInterval(() => {
        fetch(`/progresses`).then(res => res.json())
            .then(data => {
                for (const [hash, info] of Object.entries(data)) {

                    const bar = document.getElementById(`progress-${hash}`);
                    bar.value = info.progress;

                    const state = document.getElementById(`state-${hash}`);
                    state.innerText = info.state;

                    const time = document.getElementById(`time-${hash}`);
                    time.innerText = info.time;
                }
            });
    }, 1000);
}

pollAllProgress();