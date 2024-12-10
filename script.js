document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const dataTable = document.getElementById('dataTable');
    const addRowBtn = document.getElementById('addRow');
    const generateBtn = document.getElementById('generateChart');
    const downloadBtn = document.getElementById('downloadChart');
    let chart = null; // 保存图表实例

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

    // 生成图表
    generateBtn.addEventListener('click', async function() {
        const data = collectData();
        if (data.labels.length === 0) {
            alert('请至少输入一组数据');
            return;
        }

        // 销毁旧图表
        if (chart) {
            chart.destroy();
        }

        try {
            const response = await fetch('/api/generate_chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            // 创建新图表
            const ctx = document.getElementById('chartContainer').getContext('2d');
            chart = new Chart(ctx, {
                type: 'polarArea',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: Array(data.values.length).fill(data.color + '80'),
                        borderColor: Array(data.values.length).fill(data.color),
                        borderWidth: 1,
                        borderAlign: 'inner'
                    }]
                },
                options: {
                    plugins: {
                        title: {
                            display: true,
                            text: data.title,
                            font: {
                                size: 16
                            }
                        },
                        legend: {
                            position: 'right'
                        }
                    },
                    scales: {
                        r: {
                            beginAtZero: true,
                            spacing: 5
                        }
                    },
                    layout: {
                        padding: 10
                    },
                    elements: {
                        arc: {
                            borderWidth: 1,
                            spacing: 10
                        }
                    }
                }
            });

            // 启用下载按钮
            downloadBtn.disabled = false;
        } catch (error) {
            console.error('Error:', error);
            alert('生成图表时发生错误，请检查网络连接');
        }
    });

    // 颜色选择器同步
    const colorPicker = document.getElementById('chartColor');
    const colorHexInput = document.getElementById('colorHex');

    if (colorPicker && colorHexInput) { // 添加空值检查
        colorPicker.addEventListener('input', function(e) {
            colorHexInput.value = e.target.value;
        });

        colorHexInput.addEventListener('input', function(e) {
            const value = e.target.value;
            if (/^#[0-9A-F]{6}$/i.test(value)) {
                colorPicker.value = value;
            }
        });
    }

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

    // 下载图表
    downloadBtn.addEventListener('click', function() {
        if (chart) {
            const url = chart.toBase64Image();
            const link = document.createElement('a');
            link.download = 'rose_chart.png';
            link.href = url;
            link.click();
        }
    });
});