from flask import Flask, send_file, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import logging
import traceback  # 添加堆栈跟踪

app = Flask(__name__)
CORS(app)

# 配置详细的日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/')
def index():
    try:
        app.logger.info("访问首页")
        return send_file('index.html')
    except Exception as e:
        app.logger.error(f"首页错误: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/<path:path>')
def serve_static(path):
    try:
        app.logger.info(f"请求路径: {path}")
        if path == 'generate_chart':
            return generate_chart()
        
        # 检查文件是否存在
        file_path = os.path.join(os.path.dirname(__file__), path)
        app.logger.info(f"尝试访问文件: {file_path}")
        
        if os.path.exists(file_path):
            app.logger.info(f"提供文件: {path}")
            return send_file(file_path)
            
        app.logger.error(f"文件未找到: {path}")
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        app.logger.error(f"静态文件错误: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500
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
