import os
import tempfile
from flask import send_file, jsonify
from pytubefix import YouTube

def download_audio(youtube_url, output_path):
    """
    Download YouTube video as MP3.
    """
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    audio_path = stream.download(output_path=output_path)
    base, ext = os.path.splitext(audio_path)
    new_file = base + '.mp3'
    os.rename(audio_path, new_file)
    return new_file

def process(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            audio_file = download_audio(url, temp_dir)
            return send_file(audio_file, as_attachment=True, download_name=os.path.basename(audio_file))
        except Exception as e:
            return jsonify({"error": str(e)}), 500
