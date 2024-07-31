from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

MODULES = {
    'youtube_to_mp4': {
        'module': 'modules.youtube_to_mp4',
        'category': 'videos',
        'input_type': 'url'
    },
    'youtube_to_mp3': {
        'module': 'modules.youtube_to_mp3',
        'category': 'audio',
        'input_type': 'url'
    },
    'ai_to_png': {
        'module': 'modules.ai_to_png',
        'category': 'images',
        'input_type': 'file'
    },
    'ai_to_svg': {
        'module': 'modules.ai_to_svg',
        'category': 'images',
        'input_type': 'file'
    }
}

@app.route('/api/modules', methods=['GET'])
def list_modules():
    return jsonify([{"id": k, "name": v['module'].split('.')[-1].replace('_', ' ').title(), "category": v['category'], "input_type": v['input_type']} for k, v in MODULES.items()])

@app.route('/api/convert/<module_id>', methods=['POST'])
def convert_file(module_id):
    if module_id not in MODULES:
        return jsonify({"error": "Module not found"}), 404

    module = importlib.import_module(MODULES[module_id]['module'])

    if MODULES[module_id]['input_type'] == 'file':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        return module.process(file)
    elif MODULES[module_id]['input_type'] == 'url':
        if 'url' not in request.json:
            return jsonify({"error": "No URL provided"}), 400
        url = request.json['url']
        if url == '':
            return jsonify({"error": "No URL provided"}), 400
        return module.process(url)
    else:
        return jsonify({"error": "Invalid input type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
