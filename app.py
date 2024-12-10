from flask import Flask, send_file, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve(path):
    """提供静态文件"""
    try:
        return send_file(path)
    except Exception as e:
        if path == 'index.html':
            return send_file('index.html')
        return f"Error: {str(e)}", 404

@app.route('/api/generate_chart', methods=['POST'])
def generate_chart():
    """处理图表生成请求"""
    try:
        data = request.get_json()
        if not data:
            return "No data received", 400
        return {"message": "Chart generation is not available in demo mode"}, 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(port=5000)
