// 添加在文件开头，DOMContentLoaded 事件之前
const translations = {
    cn: {
        title: "玫瑰图生成器",
        subtitle: "轻松创建精美的玫瑰图,请注意至少选择2组及以上的数据，最好是6-12组的数据",
        titleLabel: "标题：",
        titleTip: "（可自定义修改图表标题）",
        chartTitle: "南丁格尔玫瑰图",
        colorLabel: "图表颜色：",
        colorTip: "（支持十六进制颜色代码，例如：#FF0000 表示红色）",
        label: "标签",
        value: "数值",
        operation: "操作",
        inputLabel: "输入标签",
        inputValue: "输入数值",
        deleteBtn: "删除",
        addRowBtn: "添加行",
        generateBtn: "生成图表",
        downloadBtn: "下载图表",
        chartTitleSection: "图表标题设置",
        colorSection: "图表颜色设置",
        dataSection: "数据输入",
        warmColors: "暖色系：",
        coolColors: "冷色系：",
        natureColors: "自然色系：",
    },
    en: {
        title: "Rose Chart Generator",
        subtitle: "Create Beautiful Rose Charts Easily, please note that at least 2 sets of data are required, preferably 6-12 sets",
        titleLabel: "Title:",
        titleTip: "(You can customize the chart title)",
        chartTitle: "polar area Rose Chart",
        colorLabel: "Chart Color:",
        colorTip: "(Supports hexadecimal color code, e.g., #FF0000 for red)",
        label: "Label",
        value: "Value",
        operation: "Operation",
        inputLabel: "Enter label",
        inputValue: "Enter value",
        deleteBtn: "Delete",
        addRowBtn: "Add Row",
        generateBtn: "Generate Chart",
        downloadBtn: "Download Chart",
        chartTitleSection: "Chart Title Settings",
        colorSection: "Chart Color Settings",
        dataSection: "Data Input",
        warmColors: "Warm Colors:",
        coolColors: "Cool Colors:",
        natureColors: "Nature Colors:",
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // 首先获取所有DOM元素
    const dataTable = document.getElementById('dataTable');
    const addRowBtn = document.getElementById('addRow');
    const generateBtn = document.getElementById('generateChart');
    const downloadBtn = document.getElementById('downloadChart');
    const colorPicker = document.getElementById('chartColor');
    const colorHexInput = document.getElementById('colorHex');
    const languageToggle = document.getElementById('languageToggle');
    const colorPreview = document.getElementById('colorPreview');
    let chart = null;

    // 检查必要的元素是否存在
    if (!dataTable || !addRowBtn || !generateBtn || !downloadBtn || !colorPicker || !colorHexInput || !languageToggle || !colorPreview) {
        console.error('找不到必要的DOM元素');
        return;
    }

    // 语言切换相关函数
    let currentLang = 'cn';

    function updateLanguage(lang) {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            if (translations[lang][key]) {
                if (element.tagName === 'INPUT') {
                    element.placeholder = translations[lang][key];
                    if (element.id === 'chartTitle') {
                        element.value = translations[lang]['chartTitle'];
                    }
                } else {
                    element.textContent = translations[lang][key];
                }
            }
        });

        // 更新动态添加的行的占位符文本
        const labelInputs = document.querySelectorAll('.label-input');
        const valueInputs = document.querySelectorAll('.value-input');
        const deleteButtons = document.querySelectorAll('.delete-row');

        labelInputs.forEach(input => {
            input.placeholder = translations[lang]['inputLabel'];
        });
        valueInputs.forEach(input => {
            input.placeholder = translations[lang]['inputValue'];
        });
        deleteButtons.forEach(button => {
            button.textContent = translations[lang]['deleteBtn'];
        });
    }

    function createNewRow(lang) {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="label-input" placeholder="${translations[lang]['inputLabel']}" data-i18n="inputLabel"></td>
            <td><input type="number" class="value-input" placeholder="${translations[lang]['inputValue']}" data-i18n="inputValue"></td>
            <td><button class="delete-row" data-i18n="deleteBtn">${translations[lang]['deleteBtn']}</button></td>
        `;
        return newRow;
    }

    // 设置事件监听器
    languageToggle.addEventListener('click', function() {
        currentLang = currentLang === 'cn' ? 'en' : 'cn';
        updateLanguage(currentLang);
        this.textContent = currentLang === 'cn' ? 'English' : '中文';
    });

    addRowBtn.addEventListener('click', function() {
        const newRow = createNewRow(currentLang);
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

        try {
            const response = await fetch('/api/generate_chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // 销毁旧图表
            if (chart) {
                chart.destroy();
            }

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
                            spacing: 10
                        }
                    },
                    layout: {
                        padding: 20
                    },
                    elements: {
                        arc: {
                            borderWidth: 2,
                            spacing: 20,
                            borderAlign: 'inner',
                            weight: 1
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
    colorPicker.addEventListener('input', function(e) {
        const color = e.target.value;
        colorHexInput.value = color;
        colorPreview.style.backgroundColor = color;
    });

    colorHexInput.addEventListener('input', function(e) {
        const value = e.target.value;
        if (/^#[0-9A-F]{6}$/i.test(value)) {
            colorPicker.value = value;
            colorPreview.style.backgroundColor = value;
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

    // 色板点击事件处理
    document.querySelectorAll('.color-chip').forEach(chip => {
        // 设置初始背景色
        chip.style.backgroundColor = chip.dataset.color;

        // 添加点击事件
        chip.addEventListener('click', function() {
            const color = this.dataset.color;
            colorPicker.value = color;
            colorHexInput.value = color;
            colorPreview.style.backgroundColor = color;
        });
    });
});