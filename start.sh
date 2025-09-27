#!/bin/bash
apt-get update -y && apt-get install -y ffmpeg
chmod +x stream.py
python3 main.py
