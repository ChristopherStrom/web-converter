import os
import tempfile
from flask import send_file, jsonify
from pytubefix import YouTube

TEMP_DIR = '/home/ubuntu/web-converter/temp/'

def download_video(youtube_url, output_path):
    """
    Download YouTube video as MP4.
    """
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(file_extension='mp4').first()
    stream.download(output_path=output_path, filename='video')
    mp4_path = os.path.join(output_path, 'video.mp4')
    # Explicitly rename the file to ensure it has the correct extension
    if not os.path.exists(mp4_path):
        os.rename(os.path.join(output_path, 'video'), mp4_path)
    return mp4_path

def convert_to_mp3(mp4_file, output_path):
    """
    Convert MP4 file to MP3 using ffmpeg.
    """
    mp3_file = os.path.join(output_path, 'audio.mp3')
    command = f'ffmpeg -i "{mp4_file}" -q:a 0 -map a "{mp3_file}"'
    os.system(command)
    return mp3_file

def process(url):
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_dir = tempfile.mkdtemp(dir=TEMP_DIR)
    try:
        mp4_file = download_video(url, temp_dir)
        mp3_file = convert_to_mp3(mp4_file, temp_dir)
        return send_file(mp3_file, as_attachment=True, download_name='audio.mp3')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(temp_dir)
