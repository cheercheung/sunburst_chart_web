import webbrowser
import subprocess
import time
import os
import sys

def start_app():
    # 使用 python3 而不是 python
    python_cmd = 'python3' if sys.platform == 'darwin' else 'python'
    
    # 启动 Flask 服务器
    print("启动服务器...")
    flask_process = subprocess.Popen([python_cmd, 'app.py'], cwd=os.path.dirname(__file__))
    
    # 等待服务器启动
    time.sleep(2)
    
    # 打开浏览器
    print("打开浏览器...")
    webbrowser.open('http://127.0.0.1:5000')
    
    try:
        # 等待用户手动关闭（按 Ctrl+C）
        print("服务器已启动。按 Ctrl+C 关闭服务器...")
        flask_process.wait()
    except KeyboardInterrupt:
        # 优雅地关闭服务器
        print("\n关闭服务器...")
        flask_process.terminate()
        flask_process.wait()

if __name__ == '__main__':
    start_app() 
    
    
