import webbrowser
import subprocess
import time
import os
import sys
import platform
import signal
import psutil

# 全局定义 python_cmd
python_cmd = 'python3.10' if platform.system() == 'Darwin' else ('python3' if platform.system() == 'Linux' else 'python')

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
        result = subprocess.run(
            [python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("安装依赖失败，错误信息：")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"检查依赖时出错：{e}")
        return False

def start_server():
    try:
        # 获取当前脚本的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        print(f"当前工作目录: {current_dir}")
        print(f"使用 Python 命令: {python_cmd}")
        
        try:
            # 先关闭已存在的服务器
            print("检查并关闭已存在的服务器...")
            kill_existing_server()
            
            # 检查依赖
            if not check_dependencies():
                raise Exception("依赖安装失败")
            
            # 启动服务器
            print(f"\n启动服务器...")
            process = subprocess.Popen([python_cmd, 'app.py'], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     universal_newlines=True)
            
            # 等待并读取端口信息
            for line in process.stdout:
                print(line.strip())
                if "服务器将在端口" in line:
                    port = line.split()[-2]
                    url = f"http://localhost:{port}"
                    print(f"服务器已启动，正在打开浏览器...")
                    webbrowser.open(url)
                    
                    # 保持服务器运行
                    print("\n服务器运行中... 按 Ctrl+C 关闭服务器")
                    try:
                        while True:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n正在关闭服务器...")
                        process.terminate()
                    break
                
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
        if sys.version_info > (3, 12):
            print("警告: Python 版本过高，建议使用 3.10-3.12 之间的版本")
            print("请安装 Python 3.10 版本并重试")
            sys.exit(1)
        elif sys.version_info < (3, 10):
            print("警告: Python 版本过低，建议使用 3.10-3.12 之间的版本")
            print("请安装 Python 3.10 版本并重试")
            sys.exit(1)
        
        # 添加 psutil 依赖
        subprocess.check_call([python_cmd, '-m', 'pip', 'install', 'psutil'])
        start_server()
    except Exception as e:
        print(f"程序异常退出：{e}")
        input("按回车键退出...")
    
