from flask import Flask, request, jsonify, send_file
import importlib

app = Flask(__name__)

# Increase maximum upload size
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 20 MB

# Configuration for available modules
MODULES = {
    "ai-to-png": {"module": "modules.ai_to_png", "category": "Images"},
    "docx-to-pdf": {"module": "modules.docx_to_pdf", "category": "Documents"}
}

@app.route('/api/modules', methods=['GET'])
def list_modules():
    return jsonify([{"id": k, "name": v['module'].split('.')[-1].replace('_', ' ').title(), "category": v['category']} for k, v in MODULES.items()])

@app.route('/api/convert/<module_id>', methods=['POST'])
def convert_file(module_id):
    if module_id not in MODULES:
        return jsonify({"error": "Module not found"}), 404

    module = importlib.import_module(MODULES[module_id]['module'])
    return module.process(request.files['file'])

if __name__ == '__main__':
    app.run(debug=True)
