import webbrowser
import subprocess
import time
import os
import sys
import platform

def start_app():
    # 根据系统类型选择 Python 命令
    if platform.system() == 'Darwin':  # macOS
        python_cmd = 'python3'
    elif platform.system() == 'Windows':
        python_cmd = 'python'
    else:
        python_cmd = 'python3'
    
    print(f"使用 Python 命令: {python_cmd}")
    print(f"当前工作目录: {os.path.dirname(os.path.abspath(__file__))}")
    
    # 启动 Flask 服务器
    print("启动服务器...")
    flask_process = subprocess.Popen(
        [python_cmd, 'app.py'],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # 等待服务器启动
    time.sleep(2)
    
    # 打开浏览器
    print("打开浏览器...")
    webbrowser.open('http://127.0.0.1:5000')
    
    try:
        print("服务器已启动。按 Ctrl+C 关闭服务器...")
        flask_process.wait()
    except KeyboardInterrupt:
        print("\n关闭服务器...")
        flask_process.terminate()
        flask_process.wait()

if __name__ == '__main__':
    start_app()
    
