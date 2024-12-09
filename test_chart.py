from rose_chart import generate_rose_chart
import traceback
import sys

def test_chart():
    # 测试数据
    test_labels = ["测试A", "测试B", "测试C"]
    test_values = [100, 200, 300]
    
    print("开始测试生成图表...")
    print(f"Python version: {sys.version}")
    print(f"测试数据: labels={test_labels}, values={test_values}")
    
    try:
        print("调用 generate_rose_chart...")
        svg_content = generate_rose_chart(test_labels, test_values)
        
        if svg_content:
            print(f"生成的 SVG 内容长度: {len(svg_content)}")
            # 保存到文件
            try:
                with open('test_output.svg', 'w', encoding='utf-8') as f:
                    f.write(svg_content)
                print("测试成功：图表已保存到 test_output.svg")
                return True
            except Exception as e:
                print(f"保存文件时出错: {str(e)}")
                print(traceback.format_exc())
                return False
        else:
            print("测试失败：generate_rose_chart 返回 None")
            return False
    except Exception as e:
        print(f"测试出错：{str(e)}")
        print("错误详情：")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    # 检查依赖
    try:
        import matplotlib
        print(f"Matplotlib version: {matplotlib.__version__}")
        print(f"Matplotlib backend: {matplotlib.get_backend()}")
        
        import numpy
        print(f"Numpy version: {numpy.__version__}")
    except Exception as e:
        print(f"导入依赖时出错: {str(e)}")
    
    print("\n开始测试...")
    success = test_chart()
    print(f"\n测试结果: {'成功' if success else '失败'}") 