import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from sunburst import generate_sunburst

def handler(event, context):
    try:
        # 解析请求数据
        if event['httpMethod'] != 'POST':
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
        # 解析请求体
        body = json.loads(event['body'])
        
        # 生成图表
        svg_content = generate_sunburst(
            labels_list=body['labels_list'],
            values=body['values'],
            title=body['title'],
            cmap=body['cmap'],
            font_size=body.get('font_size', 10),
            label_color=body.get('label_color', '#000000')
        )
        
        if svg_content is None:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to generate chart'})
            }
            
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/svg+xml',
                'Access-Control-Allow-Origin': '*'  # 添加 CORS 头
            },
            'body': svg_content
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")  # 添加错误日志
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 