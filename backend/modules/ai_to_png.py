import os
import zipfile
import tempfile
from flask import jsonify, send_file
from werkzeug.utils import secure_filename

def process(file):
    filename = secure_filename(file.filename)
    input_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(input_path)
    
    if zipfile.is_zipfile(input_path):
        return process_zip(input_path)
    else:
        return process_single_file(input_path)

def process_single_file(input_path):
    output_path = os.path.join(tempfile.gettempdir(), f"{os.path.splitext(os.path.basename(input_path))[0]}.png")
    os.system(f"inkscape {input_path} --export-png={output_path}")
    return send_file(output_path, as_attachment=True)

def process_zip(input_zip):
    output_zip = os.path.join(tempfile.gettempdir(), "converted_files.zip")
    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        extract_dir = os.path.join(tempfile.gettempdir(), "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        zip_ref.extractall(extract_dir)

        output_dir = os.path.join(tempfile.gettempdir(), "converted")
        os.makedirs(output_dir, exist_ok=True)

        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.png")
                os.system(f"inkscape {input_file} --export-png={output_file}")

        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))

    return send_file(output_zip, as_attachment=True, download_name="converted_files.zip")
