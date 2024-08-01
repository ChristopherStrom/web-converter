import os
import tempfile
from flask import send_file, jsonify
import subprocess

def convert_to_mp4(input_file, output_file):
    """
    Convert WebM file to MP4 using ffmpeg.
    """
    command = f'ffmpeg -i "{input_file}" -c:v libx264 -c:a aac "{output_file}"'
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process(file):
    os.makedirs('/home/ubuntu/web-converter/temp/', exist_ok=True)
    with tempfile.TemporaryDirectory(dir='/home/ubuntu/web-converter/temp/') as temp_dir:
        try:
            input_path = os.path.join(temp_dir, file.filename)
            file.save(input_path)
            output_path = os.path.join(temp_dir, 'output.mp4')
            convert_to_mp4(input_path, output_path)
            return send_file(output_path, as_attachment=True, download_name='output.mp4')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
