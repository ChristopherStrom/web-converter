import os
import zipfile
import tempfile
import subprocess
from flask import send_file

def convert_to_jpeg(input_file, output_file):
    """
    Convert AI file to JPEG using Inkscape.
    """
    command = ['inkscape', '--export-type=jpeg', input_file, '-o', output_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Converting {input_file} to JPEG: {result.stdout}, {result.stderr}")

def process(file):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, 'converted_files.zip')
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        jpeg_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file_name in files:
                if file_name.endswith('.ai'):
                    input_path = os.path.join(root, file_name)
                    output_path = os.path.splitext(input_path)[0] + '.jpeg'
                    convert_to_jpeg(input_path, output_path)
                    jpeg_files.append(output_path)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for jpeg_file in jpeg_files:
                zipf.write(jpeg_file, os.path.relpath(jpeg_file, temp_dir))

        return send_file(zip_path, as_attachment=True, download_name='converted_files.zip')
