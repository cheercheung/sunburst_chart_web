exports.handler = async function(event, context) {
    // 只允许 POST 请求
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const data = JSON.parse(event.body);
        const { labels, values } = data;

        // 验证数据
        if (!labels || !values || labels.length === 0 || values.length === 0) {
            return {
                statusCode: 400,
                body: JSON.stringify({ error: 'Invalid data format' })
            };
        }

        // 直接返回处理后的数据
        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                labels: labels,
                values: values
            })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Server error' })
        };
    }
};