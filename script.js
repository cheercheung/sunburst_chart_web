// 在文件开头添加语言配置
const translations = {
    zh: {
        title: '南丁格尔玫瑰图',
        buttonText: 'English',
        noDataAlert: '请至少输入一组数据',
        errorAlert: '生成图表时发生错误，请检查网络连接'
    },
    en: {
        title: 'polar area Rose Chart',
        buttonText: '中文',
        noDataAlert: 'Please enter at least one set of data',
        errorAlert: 'Error generating chart, please check network connection'
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // 添加语言切换功能
    const toggleLanguageBtn = document.getElementById('toggleLanguage');
    let currentLang = 'zh';

    function switchLanguage() {
        currentLang = currentLang === 'zh' ? 'en' : 'zh';

        // 更新按钮文本
        toggleLanguageBtn.textContent = translations[currentLang].buttonText;

        // 更新所有带有 data-lang 属性的元素
        document.querySelectorAll('[data-lang]').forEach(element => {
            const elementLang = element.getAttribute('data-lang');
            if (elementLang === currentLang) {
                element.style.display = '';
            } else {
                element.style.display = 'none';
            }
        });

        // 更新所有输入框的 placeholder
        document.querySelectorAll('[data-placeholder-zh]').forEach(input => {
            input.placeholder = input.getAttribute(`data-placeholder-${currentLang}`);
        });

        // 更新图表标题默认值
        const chartTitle = document.getElementById('chartTitle');
        if (chartTitle.value === translations.zh.title || chartTitle.value === translations.en.title) {
            chartTitle.value = translations[currentLang].title;
        }

        // 更新表格中已有行的删除按钮
        dataTable.querySelectorAll('tbody tr').forEach(row => {
            const deleteButtons = row.querySelectorAll('.delete-row');
            deleteButtons.forEach(button => {
                if (button.getAttribute('data-lang') === currentLang) {
                    button.style.display = '';
                } else {
                    button.style.display = 'none';
                }
            });
        });

        // 更新下载按钮状态
        downloadBtns.forEach(btn => {
            if (chart) {
                btn.disabled = false;
            }
        });
    }

    toggleLanguageBtn.addEventListener('click', switchLanguage);

    // 获取DOM元素 - 更新选择器
    const dataTable = document.getElementById('dataTable');
    const addRowBtns = document.querySelectorAll('[id^="addRow-"]');
    const generateBtns = document.querySelectorAll('[id^="generateChart-"]');
    const downloadBtns = document.querySelectorAll('[id^="downloadChart-"]');
    let chart = null;

    // 为所有添加行按钮添加事件监听
    addRowBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const newRow = document.createElement('tr');
            const lang = btn.getAttribute('data-lang');
            newRow.innerHTML = `
                <td><input type="text" class="label-input" data-placeholder-zh="输入标签" data-placeholder-en="Enter label" placeholder="${lang === 'zh' ? '输入标签' : 'Enter label'}"></td>
                <td><input type="number" class="value-input" data-placeholder-zh="输入数值" data-placeholder-en="Enter value" placeholder="${lang === 'zh' ? '输入数值' : 'Enter value'}"></td>
                <td>
                    <button class="delete-row" data-lang="zh" ${lang === 'en' ? 'style="display: none;"' : ''}>删除</button>
                    <button class="delete-row" data-lang="en" ${lang === 'zh' ? 'style="display: none;"' : ''}>Delete</button>
                </td>
            `;
            dataTable.querySelector('tbody').appendChild(newRow);
        });
    });

    // 为所有生成图表按钮添加事件监听
    generateBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            const data = collectData();
            if (data.labels.length === 0) {
                alert(translations[currentLang].noDataAlert);
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
                            borderAlign: 'inner',
                            spacing: 10
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
                                spacing: 5,
                                ticks: {
                                    stepSize: 10
                                }
                            }
                        },
                        layout: {
                            padding: 20
                        },
                        elements: {
                            arc: {
                                borderWidth: 1,
                                borderColor: '#fff',
                                spacing: 10,
                                angle: 10
                            }
                        },
                        radius: 0.8
                    }
                });

                // 启用下载按钮
                downloadBtns.forEach(btn => {
                    btn.disabled = false;
                });
            } catch (error) {
                console.error('Error:', error);
                alert('生成图表时发生错误，请检查网络连接');
            }
        });
    });

    // 为所有下载按钮添加事件监听
    downloadBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            if (chart) {
                const url = chart.toBase64Image();
                const link = document.createElement('a');
                link.download = 'rose_chart.png';
                link.href = url;
                link.click();
            }
        });
    });

    // 获取颜色选择器元素
    const colorPicker = document.getElementById('chartColor');
    const colorHexInput = document.getElementById('colorHex');

    // 修改色板功能部分
    const paletteColors = document.querySelectorAll('.palette-color');

    paletteColors.forEach(colorBtn => {
        colorBtn.addEventListener('click', function() {
            const selectedColor = this.dataset.color;
            colorPicker.value = selectedColor;
            colorHexInput.value = selectedColor;
        });
    });

    // 颜色选择器同步
    if (colorPicker && colorHexInput) {
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

    // 添加删除行功能
    dataTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-row')) {
            const row = e.target.closest('tr');
            if (dataTable.querySelectorAll('tbody tr').length > 1) {
                row.remove();
            }
        }
    });
});

// 修改错误提示使用翻译
function showError(message) {
    const errorElement = document.querySelector('#error-message');
    if (errorElement) {
        errorElement.textContent = translations[currentLang][message] || message;
        errorElement.style.display = 'block';
    }
}