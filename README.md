# 旭日图生成器 (Sunburst Chart Generator)

一个简单易用的旭日图生成工具，支持多层级数据可视化，提供丰富的自定义选项。

## 功能特点

- 支持 2-6 层级的数据结构
- 丰富的颜色方案选择
- 支持标签字体大小和颜色自定义
- 支持 SVG 格式导出
- 支持中英文界面切换
- 响应式设计，支持移动端

## 使用说明

1. **图表标题设置**
   - 自定义图表标题，将显示在图表顶部

2. **图表设置**
   - 选择层级数量（2-6层）
   - 选择颜色方案或使用随机配色
   - 调整标签字体大小（8-16px）
   - 自定义标签文字颜色

3. **数据输入**
   - 输入父级标签、子级标签和对应数值
   - 可动态添加或删除数据行

4. **图表预览与导出**
   - 实时预览生成的旭日图
   - 支持导出 SVG 格式

## 技术栈

- 前端：HTML5, CSS3, JavaScript
- 后端：Python, Flask
- 图表生成：Matplotlib

## 本地运行

1. 确保已安装 Python 3.12
2. 克隆仓库：
```bash
git clone https://github.com/yourusername/sunburst-chart-generator.git
cd sunburst-chart-generator
```

3. 创建并激活虚拟环境：
```bash
python3.12 -m venv venv
source venv/bin/activate
```

4. 安装依赖：
```bash
pip install -r requirements.txt
```

5. 运行启动脚本：
```bash
python start.py
```

6. 在浏览器中访问显示的地址（默认会自动打开）

## 部署到 Vercel

1. 注册 [Vercel](https://vercel.com/) 账号并安装 Vercel CLI
2. 克隆仓库并进入目录
3. 运行 `vercel` 命令，按提示操作即可

## 注意事项

- 确保系统安装了支持中文的字体
- 建议使用现代浏览器（Chrome, Firefox, Safari, Edge 等）

## 开发计划

- [ ] 支持数据导入导出
- [ ] 添加更多颜色方案
- [ ] 支持自定义图表大小
- [ ] 添加动画效果
- [ ] 支持数据分析功能

## 许可证

MIT License
