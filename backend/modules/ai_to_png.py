import os
from flask import jsonify
from werkzeug.utils import secure_filename

def process(file):
    filename = secure_filename(file.filename)
    input_path = os.path.join('/tmp', filename)
    output_path = os.path.join('/tmp', f"{os.path.splitext(filename)[0]}.png")
    
    file.save(input_path)
    
    # Perform conversion using Inkscape or another tool
    os.system(f"inkscape {input_path} --export-png={output_path}")
    
    return jsonify({"message": "File converted successfully", "output_file": output_path})
