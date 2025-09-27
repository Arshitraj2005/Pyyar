import argparse, subprocess

def drive_url(file_id):
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--stream-key", required=True)
    p.add_argument("--video-drive", required=True)
    p.add_argument("--audio-drive", required=True)
    args = p.parse_args()

    video_url = drive_url(args.video_drive)
    audio_url = drive_url(args.audio_drive)
    rtmp = f"rtmp://a.rtmp.youtube.com/live2/{args.stream_key}"

    cmd = [
        "ffmpeg", "-re",
        "-stream_loop", "-1", "-i", video_url,
        "-stream_loop", "-1", "-i", audio_url,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "libx264", "-preset", "veryfast",
        "-r", "25", "-g", "50", "-b:v", "2500k",
        "-c:a", "aac", "-b:a", "128k", "-ac", "2",
        "-f", "flv", rtmp
    ]

    print("Running:", " ".join(cmd))
    subprocess.call(cmd)

if __name__ == "__main__":
    main()
