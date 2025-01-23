import matplotlib
matplotlib.use('Agg')  # 这行必须在其他 matplotlib 相关导入之前

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import io
import os

# 设置中文字体
def get_chinese_font():
    """获取中文字体"""
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansCJKsc-Regular.otf')
    if os.path.exists(font_path):
        print(f"使用字体: {font_path}")
        return FontProperties(fname=font_path)
    else:
        print("警告: 未找到中文字体，使用系统默认字体")
        return FontProperties()

# 获取字体
font = get_chinese_font()

def create_hierarchical_data(labels_list, values):
    """
    将多列标签数据转换为层次化的字典结构
    :param labels_list: 标签列表的列表，每个子列表代表一个层级的标签
    :param values: 最底层的数值列表
    :return: 层次化的字典数据
    """
    def nested_dict():
        """创建嵌套字典的辅助函数"""
        return {'children': {}, 'value': 0}

    hierarchy = nested_dict()
    
    # 遍历所有数据点
    for i, labels in enumerate(zip(*labels_list)):
        current = hierarchy
        # 遍历每个层级的标签
        for label in labels[:-1]:  # 除了最后一个标签
            if label not in current['children']:
                current['children'][label] = nested_dict()
            current = current['children'][label]
        
        # 处理最后一个标签（叶子节点）
        last_label = labels[-1]
        if last_label not in current['children']:
            current['children'][last_label] = {'value': values[i]}
        
        # 向上累加值
        temp = hierarchy
        for label in labels:
            temp['value'] += values[i]
            if label in temp['children']:
                temp = temp['children'][label]
    
    return hierarchy

def get_level_colors(parent_color, num_children):
    """
    根据父级颜色生成一组浅色
    :param parent_color: 父级颜色（RGBA格式）
    :param num_children: 子集数量
    :return: 子集颜色列表
    """
    base_rgb = parent_color[:3]  # 获取RGB部分
    alphas = np.linspace(0.4, 0.8, num_children)  # 生成不同的透明度
    return [(*base_rgb, alpha) for alpha in alphas]

def plot_level(data_dict, start_angle, total_value, ax, level=0, max_level=None, cmap='viridis', parent_color=None, font_size=10, label_color='#000000'):
    """递归绘制每个层级"""
    if not data_dict['children']:  # 叶子节点
        return
    
    if max_level is None:
        max_level = 6  # 最大支持6层
    
    # 计算当前层的半径范围
    inner_radius = level * (1.0 / max_level)
    outer_radius = (level + 1) * (1.0 / max_level)
    
    current_angle = start_angle
    items = sorted(data_dict['children'].items())
    
    # 获取颜色
    if level == 0:  # 第一层使用主色调
        if matplotlib.__version__ >= '3.7':
            colormap = matplotlib.colormaps[cmap]
        else:
            colormap = plt.cm.get_cmap(cmap)
        colors = colormap(np.linspace(0, 1, len(items)))
    else:  # 子层使用父级颜色的浅色版本
        colors = get_level_colors(parent_color, len(items))
    
    for i, (label, child_dict) in enumerate(items):
        # 计算扇形角度
        angle = 2 * np.pi * child_dict['value'] / total_value
        current_color = colors[i]
        
        # 绘制扇形
        ax.bar([current_angle + angle/2], [outer_radius - inner_radius],
               width=angle, bottom=inner_radius,
               color=current_color,
               edgecolor='white',
               linewidth=1)
        
        # 添加标签
        if angle > 0.1:
            label_angle = current_angle + angle/2
            label_radius = (inner_radius + outer_radius) / 2
            rotation = np.rad2deg(label_angle)
            if 90 <= rotation <= 270:
                rotation += 180
            
            plt.text(label_angle, label_radius, label,
                    ha='center', va='center',
                    rotation=rotation,
                    fontproperties=font,
                    fontsize=font_size,
                    color=label_color)
        
        # 递归处理下一层，传递当前颜色作为父级颜色
        if isinstance(child_dict, dict) and 'children' in child_dict:
            plot_level(child_dict, current_angle, total_value, ax,
                      level + 1, max_level, cmap, current_color, font_size, label_color)
        
        current_angle += angle

def generate_sunburst(labels_list, values, title, cmap='viridis', font_size=10, label_color='#000000'):
    """
    生成旭日图
    
    Args:
        labels_list (list): 标签列表的列表，每个子列表代表一层
        values (list): 数值列表
        title (str): 图表标题
        cmap (str): 颜色映射名称
        font_size (int): 字体大小
        label_color (str): 标签颜色
        
    Returns:
        str: SVG 格式的图表内容，如果生成失败则返回 None
    """
    try:
        # 数据验证
        if not labels_list or not values:
            print("错误: 空数据")
            return None
            
        # 验证数据类型
        if not isinstance(values, list):
            print("错误: values 必须是列表类型")
            return None
            
        # 转换数值为浮点数
        try:
            values = [float(v) for v in values]
        except (TypeError, ValueError) as e:
            print(f"错误: 数值转换失败 - {str(e)}")
            return None
            
        # 验证数据长度一致性
        if not all(len(level) == len(values) for level in labels_list):
            print("错误: 数据长度不一致")
            print(f"标签长度: {[len(level) for level in labels_list]}")
            print(f"数值长度: {len(values)}")
            return None

        # 清除之前的图表
        plt.clf()
        plt.close('all')
        
        # 创建图表
        try:
            # 选择一个可用的样式，不再打印样式列表
            if 'seaborn-v0_8' in plt.style.available:
                plt.style.use('seaborn-v0_8')
            elif 'seaborn' in plt.style.available:
                plt.style.use('seaborn')
            else:
                plt.style.use('default')
            
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='polar')
            
            # 创建层次化数据
            data = create_hierarchical_data(labels_list, values)
            if not data:
                print("错误: 创建层次化数据失败")
                return None
                
            # 计算总值
            total_value = data['value']
            if total_value <= 0:
                print("错误: 总值必须大于0")
                return None
            
            # 开始递归绘制
            plot_level(data, 0, total_value, ax, 
                      max_level=len(labels_list), 
                      cmap=cmap,
                      font_size=font_size,
                      label_color=label_color)
            
            # 设置图表样式
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
            ax.set_rticks([])
            ax.set_xticks([])
            
            plt.title(title, fontproperties=font, pad=20, fontsize=14, 
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
            
            # 保存为SVG
            svg_io = io.BytesIO()
            plt.savefig(svg_io, format='svg', bbox_inches='tight')
            svg_content = svg_io.getvalue().decode('utf-8')
            
            plt.close(fig)
            svg_io.close()
            
            return svg_content
            
        except Exception as e:
            print(f"错误: 生成图表时发生异常 - {str(e)}")
            import traceback
            print(traceback.format_exc())
            return None
            
    except Exception as e:
        print(f"生成旭日图时出错: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None

# 测试代码
if __name__ == "__main__":
    print("请运行 app.py 启动服务器")
