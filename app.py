from flask import Flask, send_file, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path == 'generate_chart':  # 重定向旧路径到新路径
        return generate_chart()
    if os.path.exists(path):
        return send_file(path)
    return f"File not found: {path}", 404

@app.route('/generate_chart', methods=['POST'])
@app.route('/api/generate_chart', methods=['POST'])
def generate_chart():
    """处理图表生成请求"""
    try:
        data = request.get_json()
        if not data:
            return "No data received", 400
        return {"message": "success"}, 200
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/health')
def health_check():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
