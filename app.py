from flask import Flask, request, jsonify, send_file, render_template
import io
import os
import sys
import matplotlib
matplotlib.use('Agg')  # 设置后端为 Agg

# 直接导入 rose_chart
from rose_chart import generate_rose_chart

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

print(f"Current directory: {current_dir}")

# 创建 Flask 应用，使用当前目录作为静态文件目录
app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    try:
        print("Attempting to serve index.html")
        # 使用你的 index.html
        return send_file('index.html')
    except Exception as e:
        print(f"Error serving index.html: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/styles.css')
def styles():
    return send_file('styles.css')

@app.route('/script.js')
def script():
    return send_file('script.js')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    try:
        print("Received chart generation request")
        data = request.get_json()
        if not data:
            print("No data received")
            return "No data received", 400
            
        print(f"Data received: {data}")
        labels = data.get('labels', [])
        values = data.get('values', [])
        title = data.get('title', '南丁格尔玫瑰图')
        color = data.get('color', '#4CAF50')
        
        if not labels or not values:
            print("Missing labels or values")
            return "Missing labels or values", 400
            
        # 确保 values 是数值列表
        try:
            values = [float(v) for v in values]
        except (ValueError, TypeError) as e:
            print(f"Error converting values to float: {str(e)}")
            return "Invalid numeric values", 400
            
        print(f"Generating chart with labels: {labels} and values: {values}")
        
        try:
            svg_content = generate_rose_chart(labels, values, title, color)
            if not svg_content:
                print("generate_rose_chart returned None")
                return "Failed to generate chart", 500
        except Exception as e:
            import traceback
            print("Error in generate_rose_chart:")
            print(traceback.format_exc())
            return f"Error in chart generation: {str(e)}", 500
            
        print("Chart generated successfully")
        print(f"SVG content length: {len(svg_content)}")
        
        return svg_content, 200, {'Content-Type': 'image/svg+xml'}
        
    except Exception as e:
        import traceback
        print(f"Error in generate_chart endpoint: {str(e)}", file=sys.stderr)
        print("Full traceback:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return f"Error generating chart: {str(e)}", 500

if __name__ == '__main__':
    print("\nStarting Flask application...")
    app.run(debug=True, port=5000) 