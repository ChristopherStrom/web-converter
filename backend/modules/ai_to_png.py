import os
import zipfile
import tempfile
import subprocess
import datetime
from flask import send_file, jsonify
from werkzeug.utils import secure_filename

def convert_to_png(input_file, output_file):
    """
    Convert AI file to PNG using Inkscape.
    """
    command = ['inkscape', '--export-type=png', input_file, '-o', output_file]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise Exception(f"Error converting file: {result.stderr.decode('utf-8')}")

def process(file):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    processing_dir = os.path.join(tempfile.gettempdir(), f"processing_{timestamp}")
    os.makedirs(processing_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    input_path = os.path.join(processing_dir, filename)
    file.save(input_path)

    if zipfile.is_zipfile(input_path):
        return process_zip(input_path, processing_dir)
    else:
        return process_single_file(input_path, processing_dir)

def process_single_file(input_path, processing_dir):
    output_path = os.path.join(processing_dir, f"{os.path.splitext(os.path.basename(input_path))[0]}.png")
    try:
        convert_to_png(input_path, output_path)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not os.path.exists(output_path):
        return jsonify({"error": "File conversion failed"}), 500

    return send_file(output_path, as_attachment=True, download_name=os.path.basename(output_path))

def process_zip(input_zip, processing_dir):
    extract_dir = os.path.join(processing_dir, "extracted")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(input_zip, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    output_dir = os.path.join(processing_dir, "converted")
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file.endswith('.ai'):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}.png")
                try:
                    convert_to_png(input_file, output_file)
                except Exception as e:
                    return jsonify({"error": str(e)}), 500

    output_zip = os.path.join(processing_dir, "converted_files.zip")
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_dir))

    return send_file(output_zip, as_attachment=True, download_name="converted_files.zip")
