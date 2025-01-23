from flask import Flask, send_file, request, jsonify
from flask_cors import CORS
import os
from sunburst import generate_sunburst
import logging
from matplotlib.font_manager import FontProperties

# 配置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    try:
        if path == "":
            logger.info("访问首页")
            return send_file('index.html')
        elif os.path.exists(path):
            logger.info(f"访问文件: {path}")
            return send_file(path)
        else:
            logger.warning(f"文件不存在，返回首页: {path}")
            return send_file('index.html')
    except Exception as e:
        logger.error(f"服务静态文件时出错: {str(e)}")
        return jsonify({"error": "服务器内部错误"}), 500

@app.route('/api/generate-chart', methods=['POST'])
def generate_chart():
    try:
        data = request.get_json()
        logger.info("\n=== 接收到的数据 ===")
        logger.info(f"Data: {data}")
        
        if not data:
            logger.warning("未收到数据")
            return jsonify({"error": "未收到数据"}), 400
            
        # 验证数据格式
        logger.info("\n=== 数据验证 ===")
        required_fields = ['labels_list', 'values', 'title', 'cmap']
        for field in required_fields:
            if field not in data:
                logger.warning(f"缺少必要字段: {field}")
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
            if not data[field]:
                logger.warning(f"字段 {field} 不能为空")
                return jsonify({"error": f"字段 {field} 不能为空"}), 400
            logger.info(f"{field}: {data[field]}")
        
        # 验证数据类型
        if not isinstance(data['values'], list):
            return jsonify({"error": "数值必须是列表类型"}), 400
            
        try:
            values = [float(v) for v in data['values']]
        except (TypeError, ValueError):
            return jsonify({"error": "数值必须是有效的数字"}), 400
            
        # 验证数据长度一致性
        labels_list = data['labels_list']
        if not all(len(level) == len(data['values']) for level in labels_list):
            return jsonify({"error": "所有数据数组长度必须相同"}), 400
            
        if len(data['values']) == 0:
            return jsonify({"error": "至少需要一组完整的数据"}), 400
            
        # 生成旭日图
        logger.info("\n=== 生成图表 ===")
        svg_content = generate_sunburst(
            labels_list=labels_list,
            values=values,
            title=data['title'],
            cmap=data['cmap'],
            font_size=data.get('font_size', 10),
            label_color=data.get('label_color', '#000000')
        )
        
        if svg_content is None:
            return jsonify({"error": "生成图表失败，请检查数据格式"}), 500
            
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}
        
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

def get_chinese_font():
    """获取中文字体"""
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJKsc-Regular.otf')
    if os.path.exists(font_path):
        print(f"使用字体: {font_path}")
        return

if __name__ == '__main__':
    import socket
    
    def find_free_port():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    port = find_free_port()
    logger.info(f"\n服务器将在端口 {port} 上启动")
    app.run(port=port)
