from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import os

# 获取当前文件的绝对路径目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file(os.path.join(CURRENT_DIR, 'index.html'))

@app.route('/<path:path>')
def serve_static(path):
    try:
        file_path = os.path.join(CURRENT_DIR, path)
        if os.path.exists(file_path):
            return send_file(file_path)
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_chart', methods=['POST'])
@app.route('/api/generate_chart', methods=['POST'])
def generate_chart():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print(f"服务器运行目录: {CURRENT_DIR}")
    app.run(host='0.0.0.0', port=5000, debug=True)
