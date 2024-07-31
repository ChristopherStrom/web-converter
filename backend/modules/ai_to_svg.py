import os
import zipfile
import tempfile
import subprocess
from flask import send_file

def convert_to_svg(input_file, output_file):
    """
    Convert AI file to SVG using Inkscape.
    """
    command = ['inkscape', '--export-type=svg', input_file, '-o', output_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Converting {input_file} to SVG: {result.stdout}, {result.stderr}")

def process(file):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, 'converted_files.zip')
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        svg_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file_name in files:
                if file_name.endswith('.ai'):
                    input_path = os.path.join(root, file_name)
                    output_path = os.path.splitext(input_path)[0] + '.svg'
                    convert_to_svg(input_path, output_path)
                    svg_files.append(output_path)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for svg_file in svg_files:
                zipf.write(svg_file, os.path.relpath(svg_file, temp_dir))

        return send_file(zip_path, as_attachment=True, download_name='converted_files.zip')
