import subprocess
import threading
from utils import download_drive_file
from keep_alive import keep_alive

VIDEO_DRIVE_ID = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"
AUDIO_DRIVE_ID = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"
STREAM_KEY = "2c4f-5sy5-q7tx-cz4t-0c8r"

video_file = download_drive_file(VIDEO_DRIVE_ID, "video.mp4")
audio_file = download_drive_file(AUDIO_DRIVE_ID, "audio.mp3")

# ===== Video Loop Process =====
video_process = subprocess.Popen([
    "ffmpeg", "-stream_loop", "-1", "-i", video_file, "-c:v", "copy", "-an",
    "-f", "mpegts", "video.ts"
])

# ===== Audio Process (dynamic) =====
audio_process = None
def play_audio(audio_file):
    global audio_process
    if audio_process:
        audio_process.terminate()
    audio_process = subprocess.Popen([
        "ffmpeg", "-re", "-i", audio_file, "-c:a", "aac", "-f", "mpegts", "audio.ts"
    ])

# ===== Merge Video + Audio → YouTube =====
merge_process = subprocess.Popen([
    "ffmpeg",
    "-i", "video.ts",
    "-i", "audio.ts",
    "-c:v", "copy",
    "-c:a", "aac",
    "-f", "flv",
    f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"
])

# ===== Keep Audio Changing Example =====
def audio_changer():
    import time
    while True:
        # Update audio file dynamically from Drive
        new_audio = download_drive_file("NEW_AUDIO_DRIVE_ID", "audio.mp3")
        play_audio(new_audio)
        time.sleep(3600)  # 1 hour baad next audio

threading.Thread(target=audio_changer).start()

# ===== Keep Server Alive for Render =====
keep_alive()
