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
    stream.download(output_path=output_path, filename='video')
    return os.path.join(output_path, 'video.mp4')

def convert_to_mp3(mp4_file, output_path):
    """
    Convert MP4 file to MP3 using ffmpeg.
    """
    mp3_file = os.path.join(output_path, 'audio.mp3')
    command = f'ffmpeg -i "{mp4_file}" -q:a 0 -map a "{mp3_file}"'
    os.system(command)
    return mp3_file

def process(url):
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            mp4_file = download_video(url, temp_dir)
            mp3_file = convert_to_mp3(mp4_file, temp_dir)
            return send_file(mp3_file, as_attachment=True, download_name='audio.mp3')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
