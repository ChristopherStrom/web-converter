import os
import subprocess
from pathlib import Path
from flask import send_file
import zipfile
import tempfile

def convert_to_png(input_file, output_file):
    """
    Convert AI file to png using Inkscape.
    
    Parameters:
    - input_file: Path to the input AI file.
    - output_file: Path to save the output png file.
    """
    command = ['inkscape', '--export-type=png', input_file, '-o', output_file]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def process(file):
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, 'uploaded.zip')
        file.save(zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        output_dir = os.path.join(temp_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        for root, _, files in os.walk(temp_dir):
            for name in files:
                if name.endswith('.ai'):
                    input_file = os.path.join(root, name)
                    base_name = os.path.splitext(name)[0]
                    output_file = os.path.join(output_dir, f"{base_name}.png")
                    convert_to_png(input_file, output_file)
        
        output_zip_path = os.path.join(temp_dir, 'output.zip')
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for root, _, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))
        
        return send_file(output_zip_path, as_attachment=True, download_name='converted_files.zip')
