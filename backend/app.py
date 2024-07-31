from flask import Flask, request, jsonify, send_file
import importlib

app = Flask(__name__)

MODULES = {
    'youtube_to_mp4': {
        'module': 'modules.youtube_to_mp4',
        'category': 'videos'
    },
    'ai_to_png': {
        'module': 'modules.ai_to_png',
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

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        return module.process(file)
    elif 'url' in request.json:
        url = request.json['url']
        if url == '':
            return jsonify({"error": "No URL provided"}), 400
        return module.process(url)
    else:
        return jsonify({"error": "No file or URL part"}), 400

if __name__ == '__main__':
    app.run(debug=True)
