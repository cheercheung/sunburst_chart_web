from flask import Flask, send_file, request
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """提供 index.html 主页面"""
    try:
        return send_file('index.html')
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件"""
    try:
        return send_file(filename)
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/api/generate_chart', methods=['POST'])
def generate_chart():
    """处理图表生成请求"""
    try:
        data = request.get_json()
        if not data:
            return "No data received", 400

        # 这里我们可以返回一个简单的响应
        return {"message": "Chart generation is not available in demo mode"}, 200

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(port=5000)
