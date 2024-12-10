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
    python_cmd = 'python3' if platform.system() in ['Darwin', 'Linux'] else 'python'
    
    print(f"当前工作目录: {current_dir}")
    print(f"使用 Python 命令: {python_cmd}")
    
    try:
        # 检查依赖是否安装
        print("检查依赖...")
        subprocess.check_call([python_cmd, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        # 启动 Flask 服务器
        print("启动服务器...")
        flask_process = subprocess.Popen(
            [python_cmd, 'app.py'],
            cwd=current_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 等待服务器启动
        time.sleep(2)
        
        # 检查服务器是否成功启动
        if flask_process.poll() is None:
            print("服务器启动成功！")
            # 打开浏览器
            print("打开浏览器...")
            webbrowser.open('http://127.0.0.1:5000')
            
            try:
                print("\n服务器运行中... 按 Ctrl+C 关闭服务器")
                while True:
                    # 检查服务器输出
                    output = flask_process.stdout.readline()
                    if output:
                        print(output.strip())
                    # 检查错误输出
                    error = flask_process.stderr.readline()
                    if error:
                        print(f"错误: {error.strip()}", file=sys.stderr)
                    # 检查服务器是否还在运行
                    if flask_process.poll() is not None:
                        break
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\n正在关闭服务器...")
            finally:
                flask_process.terminate()
                try:
                    flask_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    flask_process.kill()
                print("服务器已关闭")
        else:
            print("服务器启动失败！")
            error_output = flask_process.stderr.read()
            print(f"错误信息：\n{error_output}")
            
    except subprocess.CalledProcessError as e:
        print(f"安装依赖失败：{e}")
    except Exception as e:
        print(f"发生错误：{e}")
        if 'flask_process' in locals():
            flask_process.terminate()

if __name__ == '__main__':
    try:
        start_app()
    except Exception as e:
        print(f"程序异常退出：{e}")
        input("按回车键退出...")
    
