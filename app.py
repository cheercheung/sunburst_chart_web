from flask import Flask, request, jsonify, send_file
import io
import os
import sys
import matplotlib
from flask_cors import CORS  # 跨域支持
from rose_chart import generate_rose_chart  # 自定义的南丁格尔玫瑰图生成函数

matplotlib.use('Agg')  # 使用非交互式后端

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 创建 Flask 应用，使用当前目录作为静态文件目录
<<<<<<< HEAD
app = Flask(__name__, static_folder=current_dir)
=======
app = Flask(__name__, static_url_path='')
>>>>>>> 3f9fe23f301956e131e14c177a37e3c5ebfee482
CORS(app)  # 启用 CORS 支持

@app.route('/')
def index():
    """提供 index.html 主页面"""
    try:
<<<<<<< HEAD
        return send_file(os.path.join(current_dir, 'index.html'))
=======
        return send_file('index.html')
>>>>>>> 3f9fe23f301956e131e14c177a37e3c5ebfee482
    except Exception as e:
        app.logger.error(f"Error serving index.html: {str(e)}")
        return f"Error: {str(e)}", 500

<<<<<<< HEAD
@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件（如 CSS 和 JS）"""
    try:
        filepath = os.path.join(current_dir, filename)
        if not os.path.exists(filepath):
            app.logger.error(f"File not found: {filepath}")
            return f"File not found: {filename}", 404
        return send_file(filepath)
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
=======
@app.route('/styles.css')
def styles():
    """提供样式文件"""
    try:
        return send_file('styles.css')
    except Exception as e:
        app.logger.error(f"Error serving styles.css: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/script.js')
def script():
    """提供 JavaScript 文件"""
    try:
        return send_file('script.js')
    except Exception as e:
        app.logger.error(f"Error serving script.js: {str(e)}")
>>>>>>> 3f9fe23f301956e131e14c177a37e3c5ebfee482
        return f"Error: {str(e)}", 500

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    """处理图表生成请求"""
    try:
        data = request.get_json()
        if not data:
            app.logger.error("No data received")
            return "No data received", 400

        # 提取数据
        labels = data.get('labels', [])
        values = data.get('values', [])
        title = data.get('title', '南丁格尔玫瑰图')
        color = data.get('color', '#4CAF50')

        if not labels or not values:
            app.logger.error("Missing labels or values")
            return "Missing labels or values", 400

        # 确保 values 是浮点数列表
        try:
            values = [float(v) for v in values]
        except (ValueError, TypeError) as e:
            app.logger.error(f"Error converting values to float: {str(e)}")
            return "Invalid numeric values", 400

        app.logger.info(f"Generating chart with labels: {labels}, values: {values}")

        # 调用生成图表的函数
        try:
            svg_content = generate_rose_chart(labels, values, title, color)
            if not svg_content:
                app.logger.error("generate_rose_chart returned None")
                return "Failed to generate chart", 500
        except Exception as e:
            app.logger.error(f"Error in generate_rose_chart: {str(e)}", exc_info=True)
            return f"Error in chart generation: {str(e)}", 500

        app.logger.info("Chart generated successfully")
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}

    except Exception as e:
        app.logger.error(f"Error in generate_chart endpoint: {str(e)}", exc_info=True)
        return f"Error generating chart: {str(e)}", 500

if __name__ == '__main__':
    app.logger.info("Starting Flask application...")
    app.run(debug=True, port=5000)
