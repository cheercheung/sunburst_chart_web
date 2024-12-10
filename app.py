from flask import Flask, send_file, request, send_from_directory
from flask_cors import CORS
import os
import logging  # 添加日志支持

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    app.logger.info("访问首页")
    return send_file('index.html')

@app.route('/<path:path>')
def serve_static(path):
    app.logger.info(f"请求路径: {path}")
    if path == 'generate_chart':
        app.logger.info("重定向到图表生成")
        return generate_chart()
    if os.path.exists(path):
        app.logger.info(f"提供文件: {path}")
        return send_file(path)
    app.logger.error(f"文件未找到: {path}")
    return f"File not found: {path}", 404

@app.route('/generate_chart', methods=['POST'])
@app.route('/api/generate_chart', methods=['POST'])
def generate_chart():
    """处理图表生成请求"""
    try:
        app.logger.info("接收到图表生成请求")
        data = request.get_json()
        if not data:
            app.logger.error("未收到数据")
            return "No data received", 400
        app.logger.info("图表生成成功")
        return {"message": "success"}, 200
    except Exception as e:
        app.logger.error(f"图表生成错误: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/api/health')
def health_check():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.logger.info("启动服务器...")
    app.run(host='0.0.0.0', port=5000, debug=True)
