from flask import Flask, send_file, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from sunburst import generate_sunburst

app = Flask(__name__)
CORS(app)

# 获取当前文件的绝对路径目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path == "":
        return send_file('index.html')
    elif os.path.exists(os.path.join(CURRENT_DIR, path)):
        return send_file(path)
    else:
        return send_file('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        data = request.get_json()
        print("\n=== 接收到的数据 ===")
        print("Data:", data)
        
        if not data:
            return jsonify({"error": "没有收到数据"}), 400
            
        # 验证数据格式
        print("\n=== 数据验证 ===")
        required_fields = ['labels_list', 'values', 'title', 'cmap']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
            if not data[field]:  # 检查空值
                return jsonify({"error": f"字段 {field} 不能为空"}), 400
            print(f"{field}: {data[field]}")
        
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
            
        # 获取字体大小和颜色参��
        font_size = data.get('font_size', 10)
        label_color = data.get('label_color', '#000000')
        
        # 生成旭日图
        print("\n=== 生成图表 ===")
        svg_content = generate_sunburst(
            labels_list=labels_list,
            values=values,
            title=data['title'],
            cmap=data['cmap'],
            font_size=font_size,
            label_color=label_color
        )
        
        if svg_content is None:
            return jsonify({"error": "生成图表失败，请检查数据格式"}), 500
            
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}
        
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

def find_free_port():
    """找到一个可用的端口"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

if __name__ == '__main__':
    try:
        port = find_free_port()
        print(f"服务器运行目录: {CURRENT_DIR}")
        print(f"服务器将在端口 {port} 上运行")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"启动服务器失败: {e}")
