import os
import zipfile
import tempfile
import subprocess
from flask import send_file

def convert_to_png(input_file, output_file):
    """
    Convert AI file to PNG using Inkscape.
    """
    command = ['inkscape', '--export-type=png', input_file, '-o', output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process(file):
    if zipfile.is_zipfile(file):
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, 'converted_files.zip')
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            png_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file_name in files:
                    if file_name.endswith('.ai'):
                        input_path = os.path.join(root, file_name)
                        output_path = os.path.splitext(input_path)[0] + '.png'
                        convert_to_png(input_path, output_path)
                        png_files.append(output_path)

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for png_file in png_files:
                    zipf.write(png_file, os.path.relpath(png_file, temp_dir))

            return send_file(zip_path, as_attachment=True, download_name='converted_files.zip')
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = os.path.join(temp_dir, file.filename)
            file.save(input_path)
            output_path = os.path.splitext(input_path)[0] + '.png'
            convert_to_png(input_path, output_path)
            return send_file(output_path, as_attachment=True, download_name=os.path.basename(output_path))
