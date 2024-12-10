import webbrowser
import subprocess
import time
import os
import sys
import platform

def start_app():
    # 获取当前脚本的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 根据系统类型选择 Python 命令
    python_cmd = 'python3' if platform.system() == 'Darwin' else 'python'
    
    print(f"当前工作目录: {current_dir}")
    print(f"使用 Python 命令: {python_cmd}")
    
    # 启动 Flask 服务器
    print("启动服务器...")
    flask_process = subprocess.Popen(
        [python_cmd, 'app.py'],
        cwd=current_dir
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
    
