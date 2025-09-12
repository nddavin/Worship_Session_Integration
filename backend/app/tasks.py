from celery import Celery
import time

CELERY_BROKER_URL = "redis://redis:6379/0"
app = Celery("tasks", broker=CELERY_BROKER_URL)

@app.task
def transcode_and_extract_task(audio_id: int, key: str):
    # Placeholder: add FFmpeg transcoding, metadata extraction, waveform
    time.sleep(2)
    print(f"Processed audio {audio_id} with key {key}")
