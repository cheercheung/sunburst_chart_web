import unittest
from sunburst import generate_sunburst

class TestSunburstChart(unittest.TestCase):
    def setUp(self):
        # 测试数据
        self.test_data = {
            'simple': {
                'labels_list': [
                    ["食物", "食物", "食物"],  # 父级标签
                    ["水果", "水果", "蔬菜"],  # 子级标签
                ],
                'values': [30, 20, 50],
                'title': "测试旭日图",
                'cmap': 'viridis'
            },
            'empty': {
                'labels_list': [[], []],
                'values': [],
                'title': "",
                'cmap': 'viridis'
            },
            'invalid_length': {
                'labels_list': [
                    ["食物", "食物"],  # 长度不匹配
                    ["水果", "水果", "蔬菜"],
                ],
                'values': [30, 20, 50],
                'title': "测试数据",
                'cmap': 'viridis'
            }
        }

    def test_normal_generation(self):
        """测试正常数据生成图表"""
        data = self.test_data['simple']
        svg_content = generate_sunburst(
            labels_list=data['labels_list'],
            values=data['values'],
            title=data['title'],
            cmap=data['cmap']
        )
        self.assertIsNotNone(svg_content)
        self.assertIn('<svg', svg_content)
        self.assertIn('</svg>', svg_content)

    def test_empty_data(self):
        """测试空数据处理"""
        data = self.test_data['empty']
        svg_content = generate_sunburst(
            labels_list=data['labels_list'],
            values=data['values'],
            title=data['title'],
            cmap=data['cmap']
        )
        self.assertIsNone(svg_content)

    def test_invalid_data_length(self):
        """测试数据长度不匹配的情况"""
        data = self.test_data['invalid_length']
        svg_content = generate_sunburst(
            labels_list=data['labels_list'],
            values=data['values'],
            title=data['title'],
            cmap=data['cmap']
        )
        self.assertIsNone(svg_content)

    def test_large_dataset(self):
        """测试大数据集"""
        large_data = {
            'labels_list': [
                ["分类A"] * 10 + ["分类B"] * 10,  # 父级标签
                [f"子类{i}" for i in range(20)],  # 子级标签
            ],
            'values': list(range(1, 21)),  # 1到20的数值
            'title': "大数据集测试",
            'cmap': 'viridis'
        }
        svg_content = generate_sunburst(**large_data)
        self.assertIsNotNone(svg_content)
        self.assertIn('<svg', svg_content)

if __name__ == '__main__':
    unittest.main() 