import webbrowser
import subprocess
import time
import os
import sys
import platform
import signal
import psutil
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 全局定义 python_cmd - 使用虚拟环境中的 Python
python_cmd = 'python' if os.path.exists('venv/bin/python') else '/usr/local/opt/python@3.12/bin/python3.12'

def kill_existing_server():
    """关闭已经运行的 Flask 服务器进程"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and 'python' in cmdline[0].lower() and 'app.py' in cmdline[-1]:
                print(f"关闭已存在的服务器进程 (PID: {proc.pid})")
                if platform.system() == 'Windows':
                    subprocess.run(['taskkill', '/F', '/PID', str(proc.pid)], capture_output=True)
                else:
                    os.kill(proc.pid, signal.SIGTERM)
                time.sleep(1)  # 等待进程完全关闭
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def check_dependencies():
    """检查并安装依赖"""
    try:
        print("检查依赖...")
        pip_cmd = 'pip'
        
        # 先显示当前已安装的包
        print("\n当前已安装的包：")
        subprocess.run([pip_cmd, 'list'], check=True)
        
        print("\n开始安装依赖...")
        result = subprocess.run(
            [pip_cmd, 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True,
            check=True  # 这会在命令失败时抛出异常
        )
        
        print(result.stdout)  # 显示安装输出
        
        # 验证关键包是否安装
        print("\n验证依赖安装：")
        for package in ['flask', 'flask-cors', 'matplotlib', 'numpy']:
            try:
                __import__(package.replace('-', '_'))
                print(f"✓ {package} 已安装")
            except ImportError as e:
                print(f"✗ {package} 安装失败: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"检查依赖时出错：{e}")
        return False

def start_server():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"当前工作目录: {current_dir}")
        print(f"使用 Python 命令: {python_cmd}")
        
        try:
            print("检查并关闭已存在的服务器...")
            kill_existing_server()
            
            if not check_dependencies():
                raise Exception("依赖安装失败")
            
            print(f"\n启动服务器...")
            process = subprocess.Popen([python_cmd, 'app.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True,
                                     bufsize=1)  # 设置行缓冲
            
            # 读取错误输出
            def print_stderr():
                for line in process.stderr:
                    # 只有真正的错误才加上"错误:"前缀
                    if "ERROR" in line or "Error" in line or "error" in line:
                        print(f"错误: {line.strip()}")
                    else:
                        print(line.strip())
            
            import threading
            error_thread = threading.Thread(target=print_stderr)
            error_thread.daemon = True
            error_thread.start()
            
            # 读取标准输出
            port = None
            for line in process.stdout:
                print(line.strip())
                if "服务器将在端口" in line:
                    try:
                        port = line.split()[-2]
                        url = f"http://localhost:{port}"
                        print(f"服务器已启动，正在打开浏览器... {url}")
                        time.sleep(1)  # 等待服务器完全启动
                        webbrowser.open(url)
                    except Exception as e:
                        print(f"打开浏览器时出错: {e}")
            
            if not port:
                raise Exception("未能获取服务器端口")
                
            print("\n服务器运行中... 按 Ctrl+C 关闭服务器")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n正在关闭服务器...")
                process.terminate()
                
        except Exception as e:
            print(f"启动服务器时出错: {str(e)}")
            if 'process' in locals():
                process.terminate()
        
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == '__main__':
    try:
        # 检查 Python 版本
        python_version = platform.python_version()
        print(f"当前 Python 版本: {python_version}")
        major, minor, _ = map(int, python_version.split('.'))
        
        if (major, minor) != (3, 12):
            print("警告: 请使用 Python 3.12 版本")
            print("当前使用的不是 Python 3.12")
            sys.exit(1)
        
        start_server()
    except Exception as e:
        print(f"程序异常退出：{e}")
        input("按回车键退出...")
    

def get_chinese_font():
    """获取中文字体"""
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJKsc-Regular.otf')
    if os.path.exists(font_path):
        print(f"使用字体: {font_path}")
        return FontProperties(fname=font_path)
    else:
        print("警告: 未找到中文字体，使用系统默认字体")
        return FontProperties()

# 设置全局字体
font = get_chinese_font()
plt.rcParams['font.family'] = font.get_name()

def plot_level(label_angle, label_radius, label, rotation, font_size, label_color):
    # 其他代码...
    plt.text(label_angle, label_radius, label,
             ha='center', va='center',
             rotation=rotation,
             fontproperties=font,
             fontsize=font_size,
             color=label_color)

def generate_sunburst(labels_list, values, title, cmap='viridis', font_size=10, label_color='#000000'):
    # 其他代码...
    plt.title(title, fontproperties=font, pad=20, fontsize=14, 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
