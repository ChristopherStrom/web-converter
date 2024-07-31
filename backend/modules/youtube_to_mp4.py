import os
import tempfile
from flask import send_file, jsonify
from pytubefix import YouTube

def download_video(youtube_url, output_path):
    """
    Download YouTube video as MP4.
    """
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(output_path=output_path)

def process(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            download_video(url, temp_dir)
            video_filename = os.listdir(temp_dir)[0]
            video_path = os.path.join(temp_dir, video_filename)
            return send_file(video_path, as_attachment=True, download_name=video_filename)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
