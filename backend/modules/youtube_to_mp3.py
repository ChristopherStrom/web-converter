import os
import tempfile
from flask import send_file, jsonify
from pytubefix import YouTube

def download_audio(youtube_url, output_path):
    """
    Download YouTube video and extract audio as MP3.
    """
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(output_path=output_path, filename='audio')
    audio_file = os.path.join(output_path, 'audio.mp4')

    # Convert the downloaded file to mp3
    mp3_file = os.path.join(output_path, 'audio.mp3')
    os.system(f'ffmpeg -i "{audio_file}" "{mp3_file}"')
    return mp3_file

def process(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            mp3_file = download_audio(url, temp_dir)
            return send_file(mp3_file, as_attachment=True, download_name='audio.mp3')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
