from flask import Flask, request, jsonify, send_file
import os
import matplotlib
from flask_cors import CORS
from rose_chart import generate_rose_chart

matplotlib.use('Agg')

app = Flask(__name__, static_folder='.')
CORS(app)

@app.route('/')
def index():
    """提供 index.html 主页面"""
    try:
        return send_file('index.html')
    except Exception as e:
        app.logger.error(f"Error serving index.html: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件"""
    try:
        return send_file(filename)
    except Exception as e:
        app.logger.error(f"Error serving {filename}: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/api/generate_chart', methods=['POST'])
def generate_chart():
    """处理图表生成请求"""
    try:
        data = request.get_json()
        if not data:
            return "No data received", 400

        labels = data.get('labels', [])
        values = data.get('values', [])
        title = data.get('title', '南丁格尔玫瑰图')
        color = data.get('color', '#4CAF50')

        if not labels or not values:
            return "Missing labels or values", 400

        try:
            values = [float(v) for v in values]
        except (ValueError, TypeError):
            return "Invalid numeric values", 400

        svg_content = generate_rose_chart(labels, values, title, color)
        if not svg_content:
            return "Failed to generate chart", 500

        return svg_content, 200, {'Content-Type': 'image/svg+xml'}

    except Exception as e:
        return f"Error generating chart: {str(e)}", 500
