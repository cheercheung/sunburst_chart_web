const translations = {
    zh: {
        title: '南丁格尔玫瑰图',
        buttonText: 'English',
        noDataAlert: '请至少输入一组数据',
        errorAlert: '生成图表时发生错误，请检查网络连接',
        deleteBtn: '删除',
        addRowBtn: '添加行',
        generateBtn: '生成图表',
        downloadBtn: '下载图表',
        chartTitle: '南丁格尔玫瑰图'
    },
    en: {
        title: 'Polar Area Rose Chart',
        buttonText: '中文',
        noDataAlert: 'Please enter at least 2 sets of data',
        errorAlert: 'Error generating chart, please check network connection',
        deleteBtn: 'Delete',
        addRowBtn: 'Add Row',
        generateBtn: 'Generate Chart',
        downloadBtn: 'Download Chart',
        chartTitle: 'Polar Area Rose Chart'
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // 获取所有需要的DOM元素
    const dataTable = document.getElementById('dataTable');
    const addRowBtns = document.querySelectorAll('[id^="addRow-"]');
    const generateBtns = document.querySelectorAll('[id^="generateChart-"]');
    const downloadBtns = document.querySelectorAll('[id^="downloadChart-"]');
    const colorPicker = document.getElementById('chartColor');
    const colorHexInput = document.getElementById('colorHex');
    const toggleLanguageBtn = document.getElementById('toggleLanguage');
    let chart = null;
    let currentLang = 'zh';

    // 语言切换函数
    function switchLanguage() {
        currentLang = currentLang === 'zh' ? 'en' : 'zh';

        // 更新按钮文本
        toggleLanguageBtn.textContent = translations[currentLang].buttonText;

        // 更新所有带有 data-lang 属性的元素
        document.querySelectorAll('[data-lang]').forEach(element => {
            const elementLang = element.getAttribute('data-lang');
            element.style.display = elementLang === currentLang ? '' : 'none';
        });

        // 更新所有输入框的 placeholder
        document.querySelectorAll('[data-placeholder-zh]').forEach(input => {
            input.placeholder = input.getAttribute(`data-placeholder-${currentLang}`);
        });

        // 更新图表标题
        const chartTitle = document.getElementById('chartTitle');
        if (chartTitle && (chartTitle.value === translations.zh.chartTitle || chartTitle.value === translations.en.chartTitle)) {
            chartTitle.value = translations[currentLang].chartTitle;
        }

        // 更新表格中的删除按钮
        dataTable.querySelectorAll('tbody tr').forEach(row => {
            const deleteButtons = row.querySelectorAll('.delete-row');
            deleteButtons.forEach(button => {
                const buttonLang = button.getAttribute('data-lang');
                button.style.display = buttonLang === currentLang ? '' : 'none';
            });
        });

        // 更新所有操作按钮
        document.querySelectorAll('.action-button').forEach(button => {
            const buttonLang = button.getAttribute('data-lang');
            button.style.display = buttonLang === currentLang ? '' : 'none';
        });

        // 更新表头
        document.querySelectorAll('th[data-lang]').forEach(header => {
            const headerLang = header.getAttribute('data-lang');
            header.style.display = headerLang === currentLang ? '' : 'none';
        });

        // 更新下载按钮
        downloadBtns.forEach(btn => {
            const btnLang = btn.getAttribute('data-lang');
            btn.style.display = btnLang === currentLang ? '' : 'none';
            btn.disabled = !chart;
        });
    }

    // 添加语言切换事件监听器
    toggleLanguageBtn.addEventListener('click', switchLanguage);

    // 添加新行函数
    function addNewRow(lang) {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td><input type="text" class="label-input" data-placeholder-zh="输入标签" data-placeholder-en="Enter label" placeholder="${lang === 'zh' ? '输入标签' : 'Enter label'}"></td>
            <td><input type="number" class="value-input" data-placeholder-zh="输入数值" data-placeholder-en="Enter value" placeholder="${lang === 'zh' ? '输入数值' : 'Enter value'}"></td>
            <td>
                <button class="delete-row" data-lang="zh" ${lang === 'en' ? 'style="display: none;"' : ''}>删除</button>
                <button class="delete-row" data-lang="en" ${lang === 'zh' ? 'style="display: none;"' : ''}>Delete</button>
            </td>
        `;
        dataTable.querySelector('tbody').appendChild(newRow);
    }

    // 添加行按钮事件监听
    addRowBtns.forEach(btn => {
        btn.addEventListener('click', () => addNewRow(currentLang));
    });

    // 删除行事件监听
    dataTable.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-row')) {
            const row = e.target.closest('tr');
            if (dataTable.querySelectorAll('tbody tr').length > 1) {
                row.remove();
            }
        }
    });

    // 收集表��据
    function collectData() {
        const rows = dataTable.querySelectorAll('tbody tr');
        const labels = [];
        const values = [];
        const title = document.getElementById('chartTitle').value.trim() || translations[currentLang].chartTitle;
        const color = colorHexInput.value;

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

    // 生成图表事件监听
    generateBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            const data = collectData();
            if (data.labels.length === 0) {
                alert(translations[currentLang].noDataAlert);
                return;
            }

            if (chart) {
                chart.destroy();
            }

            try {
                // 不需要发送到后端，直接在前端生成图表
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
                                font: { size: 16 }
                            },
                            legend: { position: 'right' }
                        },
                        scales: {
                            r: {
                                beginAtZero: true,
                                spacing: 5
                            }
                        },
                        layout: { padding: 10 },
                        elements: {
                            arc: {
                                borderWidth: 1,
                                spacing: 10
                            }
                        }
                    }
                });

                // 启用下载按钮
                downloadBtns.forEach(btn => btn.disabled = false);
            } catch (error) {
                console.error('Error:', error);
                alert(translations[currentLang].errorAlert);
            }
        });
    });

    // 下载图表事件监听
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

    // 颜色选择器同步
    colorPicker.addEventListener('input', e => colorHexInput.value = e.target.value);
    colorHexInput.addEventListener('input', e => {
        const value = e.target.value;
        if (/^#[0-9A-F]{6}$/i.test(value)) {
            colorPicker.value = value;
        }
    });

    // 色板点击事件
    document.querySelectorAll('.palette-color').forEach(color => {
        color.addEventListener('click', function() {
            const selectedColor = this.dataset.color;
            colorPicker.value = selectedColor;
            colorHexInput.value = selectedColor;
        });
    });
});