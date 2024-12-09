import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import matplotlib
matplotlib.use('Agg')  # 设置后端为 Agg
import io
import os

# 设置中文字体
def get_chinese_font():
    # macOS 可能的字体路径
    mac_font_paths = [
        '/System/Library/Fonts/PingFang.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/Library/Fonts/Arial Unicode.ttf'
    ]
    
    # Windows 可能的字体路径
    windows_font_paths = [
        'C:\\Windows\\Fonts\\SimSun.ttc',
        'C:\\Windows\\Fonts\\SimHei.ttf',
        'C:\\Windows\\Fonts\\Microsoft YaHei.ttf'
    ]
    
    # 尝试所有可能的字体路径
    for font_path in mac_font_paths + windows_font_paths:
        if os.path.exists(font_path):
            print(f"Found font: {font_path}")
            return FontProperties(fname=font_path)
    
    print("Warning: No Chinese font found, using default font")
    return FontProperties()

# 获取字体
font = get_chinese_font()

def generate_rose_chart(labels, values, title='南丁格尔玫瑰图', color='#4CAF50'):
    """
    生成极面积图（Polar Area Chart）
    :param labels: 标签列表
    :param values: 数值列表
    :param title: 图表标题
    :param color: 图表颜色（十六进制格式）
    :return: SVG格式的图表
    """
    try:
        print(f"Starting chart generation with labels: {labels} and values: {values}")
        
        # 清除之前的图表
        plt.clf()
        plt.close('all')
        
        # 创建图表
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='polar')
        
        # 确保数据是数值类型
        values = np.array(values, dtype=float)
        print(f"Converted values to numpy array: {values}")
        
        # 计算角度和半径
        angles = np.linspace(0, 2*np.pi, len(values), endpoint=False)
        radii = np.sqrt(values)
        width = (2*np.pi / len(values)) * 0.8  # 80% 宽度
        
        print("Plotting bars...")
        # 绘制极面积图
        bars = ax.bar(angles, radii, width=width, alpha=0.7, bottom=0, color=color)
        
        print("Setting labels...")
        # 设置标签
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, fontproperties=font)
        
        # 设置标题
        plt.title(title, fontproperties=font, pad=20)
        
        # 只显示角度网格线，隐藏径向刻度线和网格
        ax.grid(True, which='major', axis='x', linestyle='-', alpha=0.3)  # 只显示 θ 轴网格线
        ax.grid(False, which='major', axis='y')  # 关闭 r 轴网格线
        ax.set_yticks([])  # 移除径向刻度线
        
        # 添加图例
        legend_labels = [f'{label}: {value}' for label, value in zip(labels, values)]
        plt.legend(bars, legend_labels, loc='center left', bbox_to_anchor=(1.2, 0.5),
                  prop=font)
        
        print("Saving to SVG...")
        # 将图表转换为SVG格式
        svg_io = io.BytesIO()
        plt.savefig(svg_io, format='svg', bbox_inches='tight')
        svg_content = svg_io.getvalue().decode('utf-8')
        
        # 清理
        plt.close(fig)
        svg_io.close()
        
        print("Chart generation completed successfully")
        return svg_content
        
    except Exception as e:
        import traceback
        print(f"Error generating rose chart: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        return None

# 测试代码
if __name__ == "__main__":
    # 测试数据
    test_labels = ["类别A", "类别B", "类别C", "类别D", "类别E"]
    test_values = [30, 50, 20, 40, 60]
    
    print("Running test...")
    svg_content = generate_rose_chart(test_labels, test_values)
    if svg_content:
        # 保存测试图表
        with open('test_rose_chart.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print("Test chart generated successfully: test_rose_chart.svg")
    else:
        print("Test failed")
