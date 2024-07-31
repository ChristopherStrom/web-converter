from flask import Flask, request, jsonify, send_file
import importlib
import zipfile

app = Flask(__name__)

MODULES = {
    'ai_to_png': {
        'module': 'modules.ai_to_png',
        'category': 'images'
    },
    'ai_to_jpeg': {
        'module': 'modules.ai_to_jpeg',
        'category': 'images'
    },
    'ai_to_svg': {
        'module': 'modules.ai_to_svg',
        'category': 'images'
    }
}

@app.route('/api/modules', methods=['GET'])
def list_modules():
    return jsonify([{"id": k, "name": v['module'].split('.')[-1].replace('_', ' ').title(), "category": v['category']} for k, v in MODULES.items()])

@app.route('/api/convert/<module_id>', methods=['POST'])
def convert_file(module_id):
    if module_id not in MODULES:
        return jsonify({"error": "Module not found"}), 404

    module = importlib.import_module(MODULES[module_id]['module'])

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    return module.process(file)

if __name__ == '__main__':
    app.run(debug=True)
