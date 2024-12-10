document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const dataTable = document.getElementById('dataTable');
    const addRowBtn = document.getElementById('addRow');
    const generateBtn = document.getElementById('generateChart');
    const downloadBtn = document.getElementById('downloadSVG');

    // 添加新行
    addRowBtn.addEventListener('click', function() {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="label-input" placeholder="输入标签"></td>
            <td><input type="number" class="value-input" placeholder="输入数值"></td>
            <td><button class="delete-row">删除</button></td>
        `;
        dataTable.querySelector('tbody').appendChild(newRow);
    });

    // 删除行
    dataTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-row')) {
            const row = e.target.closest('tr');
            if (dataTable.querySelectorAll('tbody tr').length > 1) {
                row.remove();
            }
        }
    });

    // 生成图���
    generateBtn.addEventListener('click', async function() {
        const data = collectData();
        if (data.labels.length === 0) {
            alert('请至少输入一组数据');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/generate_chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // 确保服务器处理 JSON 数据
                },
                body: JSON.stringify(data),
            });

            // 检查响应状态
            if (response.ok) {
                const svgContent = await response.text(); // 获取返回的 SVG 内容
                document.getElementById('chartContainer').innerHTML = svgContent; // 在页面显示 SVG
                downloadBtn.disabled = false; // 启用下载按钮
            } else if (response.status === 400) {
                const errorMessage = await response.text();
                alert(`请求失败：${errorMessage}`); // 显示后端返回的错误信息
            } else {
                alert(`生成图表失败，HTTP 状态码：${response.status}`); // 通用错误提示
            }
        } catch (error) {
            console.error('Error:', error); // 在控制台记录详细错误信息
            alert('生成图表时发生错误，请检查网络连接或后端服务是否正常运行');
        }
    });

    // 颜色选择器同步
    document.getElementById('chartColor').addEventListener('input', function(e) {
        document.getElementById('colorHex').value = e.target.value;
    });

    document.getElementById('colorHex').addEventListener('input', function(e) {
        const value = e.target.value;
        if (/^#[0-9A-F]{6}$/i.test(value)) {
            document.getElementById('chartColor').value = value;
        }
    });

    // 收集表格数据
    function collectData() {
        const rows = dataTable.querySelectorAll('tbody tr');
        const labels = [];
        const values = [];
        const title = document.getElementById('chartTitle').value.trim() || '南丁格尔玫瑰图';
        const color = document.getElementById('colorHex').value;

        rows.forEach(row => {
            const label = row.querySelector('.label-input').value.trim();
            const value = parseFloat(row.querySelector('.value-input').value);

            if (label && !isNaN(value)) {
                labels.push(label);
                values.push(value);
            }
        });

        return { labels, values, title, color };
    }

    // 下载SVG
    downloadBtn.addEventListener('click', function() {
        const svg = document.querySelector('#chartContainer svg');
        if (svg) {
            const svgData = new XMLSerializer().serializeToString(svg);
            const blob = new Blob([svgData], { type: 'image/svg+xml' });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = 'rose_chart.svg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }
    });
});
