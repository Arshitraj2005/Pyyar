import os, subprocess, signal, time
from flask import Flask, request, jsonify
from keep_alive import keep_alive

app = Flask(__name__)
PROCESS_FILE = "/tmp/stream.pid"

def is_running():
    if not os.path.exists(PROCESS_FILE):
        return False
    try:
        pid = int(open(PROCESS_FILE).read())
        os.kill(pid, 0)
        return True
    except:
        return False

@app.route("/start")
def start():
    if is_running():
        return jsonify({"ok": False, "msg": "Already streaming"})

    # Fixed user details
    stream_key = "2c4f-5sy5-q7tx-cz4t-0c8r"
    video_id = "1zOqir9W5hYTbHMAAolrs5Dh71XwZHX7l"
    audio_id = "1fO8xVEIKALIZAMMYcFEMQK4Rk0cFtBp6"

    cmd = [
        "python3", "stream.py",
        "--stream-key", stream_key,
        "--video-drive", video_id,
        "--audio-drive", audio_id
    ]

    proc = subprocess.Popen(cmd, preexec_fn=os.setsid)
    open(PROCESS_FILE, "w").write(str(proc.pid))
    time.sleep(1)
    return jsonify({"ok": True, "msg": "Started", "pid": proc.pid})

@app.route("/stop")
def stop():
    if not is_running():
        return jsonify({"ok": False, "msg": "Not running"})
    pid = int(open(PROCESS_FILE).read())
    os.killpg(pid, signal.SIGTERM)
    os.remove(PROCESS_FILE)
    return jsonify({"ok": True, "msg": "Stopped"})

@app.route("/status")
def status():
    return jsonify({"running": is_running()})

if __name__ == "__main__":
    keep_alive()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
