from flask import Flask
import threading

app = Flask("")

@app.route("/")
def home():
    return "Alive!"

def keep_alive():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()
