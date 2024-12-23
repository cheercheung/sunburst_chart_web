import webbrowser
import subprocess
import time
import os
import sys
import platform
import signal
import psutil

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

def start_server():
    try:
        # 获取当前脚本的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 根据系统类型选择 Python 命令
        python_cmd = 'python3' if platform.system() in ['Darwin', 'Linux'] else 'python'
        
        print(f"当前工作目录: {current_dir}")
        print(f"使用 Python 命令: {python_cmd}")
        
        try:
            # 先关闭已存在的服务器
            print("检查并关闭已存在的服务器...")
            kill_existing_server()
            
            # 检查依赖是否安装
            print("检查依赖...")
            subprocess.check_call([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            
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
        
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败：{e}")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == '__main__':
    try:
        # 添加 psutil 依赖
        subprocess.check_call([
            'python3' if platform.system() in ['Darwin', 'Linux'] else 'python',
            '-m', 'pip', 'install', 'psutil'
        ])
        start_server()
    except Exception as e:
        print(f"程序异常退出：{e}")
        input("按回车键退出...")
    
