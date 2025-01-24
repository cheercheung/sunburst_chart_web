const translations = {
    zh: {
        title: '旭日图',
        buttonText: 'English',
        noDataAlert: '请至少输入一组完整的数据',
        errorAlert: '生成图表时发生错误，请检查网络连接',
        deleteBtn: '删除',
        addRowBtn: '添加行',
        generateBtn: '生成图表',
        downloadBtn: '下载图表',
        chartTitle: '旭日图'
    },
    en: {
        title: 'Sunburst Chart',
        buttonText: '中文',
        noDataAlert: 'Please enter at least one complete set of data',
        errorAlert: 'Error generating chart, please check network connection',
        deleteBtn: 'Delete',
        addRowBtn: 'Add Row',
        generateBtn: 'Generate Chart',
        downloadBtn: 'Download Chart',
        chartTitle: 'Sunburst Chart'
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const dataTable = document.getElementById('dataTable');
    const addRowBtns = document.querySelectorAll('[id^="addRow-"]');
    const generateBtns = document.querySelectorAll('[id^="generateChart-"]');
    const downloadBtns = document.querySelectorAll('[id^="downloadChart-"]');
    const colorScheme = document.getElementById('colorScheme');
    const toggleLanguageBtn = document.getElementById('toggleLanguage');
    const chartContainer = document.getElementById('chartContainer');
    const colorPreview = document.getElementById('colorPreview');
    const randomColorBtn = document.getElementById('randomColor');
    let currentLang = 'zh';

    // 颜色方案列表
    const colorSchemes = [
        'viridis', 'plasma', 'inferno', 'magma', 'cividis',
        'rainbow', 'tab10', 'Set3', 'Paired', 'hsv'
    ];

    // 检查必要的元素是否存在
    if (!dataTable || !chartContainer) {
        console.error('Required DOM elements not found');
        return;
    }

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

    // 根据层级数量更新表格列数
    function updateTableColumns() {
        const levelCount = parseInt(document.getElementById('levelCount').value);
        const headerRow = document.querySelector('#dataTable thead tr');
        const sampleRow = document.querySelector('#dataTable tbody tr');

        // 清空表头和示例行
        headerRow.innerHTML = '';
        sampleRow.innerHTML = '';

        // 添加标签列
        for (let i = 1; i <= levelCount; i++) {
            headerRow.innerHTML += `
                <th data-lang="zh">标签${i}</th>
                <th data-lang="en" style="display: none;">Label ${i}</th>
            `;
            sampleRow.innerHTML += `
                <td><input type="text" class="label-input" data-placeholder-zh="输入标签${i}" data-placeholder-en="Enter label ${i}" placeholder="输入标签${i}"></td>
            `;
        }

        // 添加数值列和操作列
        headerRow.innerHTML += `
            <th data-lang="zh">数值</th>
            <th data-lang="en" style="display: none;">Value</th>
            <th></th>
        `;
        sampleRow.innerHTML += `
            <td><input type="number" class="value-input" data-placeholder-zh="输入数值" data-placeholder-en="Enter value" placeholder="输入数值"></td>
            <td>
                <button class="delete-row" data-lang="zh">删除</button>
                <button class="delete-row" data-lang="en" style="display: none;">Delete</button>
            </td>
        `;
    }

    // 添加层级数量选择事件监听器
    document.getElementById('levelCount').addEventListener('change', updateTableColumns);

    // 添加新行函数
    function addNewRow(lang) {
        const newRow = document.createElement('tr');
        newRow.innerHTML = document.querySelector('#dataTable tbody tr').innerHTML;
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

    // 收集表格数据
    function getTableData() {
        const valueMap = {};
        const levelCount = parseInt(document.getElementById('levelCount').value);
        const title = document.getElementById('chartTitle').value.trim() || translations[currentLang].chartTitle;
        const cmap = colorScheme.value;
        const fontSize = parseInt(document.getElementById('fontSize').value);
        const labelColor = document.getElementById('labelColor').value;

        const rows = document.querySelectorAll('#dataTable tbody tr');
        console.log('表格行数：', rows.length);

        rows.forEach((row, index) => {
            const labels = Array.from(row.querySelectorAll('.label-input')).map(input => input.value);
            const value = parseFloat(row.querySelector('.value-input').value);

            console.log(`第 ${index + 1} 行 - 标签: ${labels.join('/')}, 值: ${value}`);

            valueMap[labels.join('/')] = value;
        });

        console.log('值映射：', valueMap);

        const labels = Object.keys(valueMap).map(path => path.split('/'));
        const values = Object.values(valueMap);

        const labels_list = [];
        for (let i = 0; i < levelCount; i++) {
            labels_list[i] = labels.map(path => path[i]);
        }

        console.log('标签列表：', labels);
        console.log('值列表：', values);

        return { labels_list, values, title, cmap, font_size: fontSize, label_color: labelColor };
    }

    // 生成图表
    async function generateChart(data) {
        try {
            console.log('发送数据:', data);
            const response = await fetch('/api/generate-chart', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    labels_list: data.labels_list,
                    values: data.values,
                    title: data.title,
                    cmap: data.cmap,
                    font_size: parseInt(data.font_size),
                    label_color: data.label_color
                })
            });

            const contentType = response.headers.get('content-type');
            if (!response.ok) {
                const errorData = contentType && contentType.includes('application/json') ?
                    await response.json() : { error: 'Unknown error' };
                console.error('服务器错误:', errorData);
                throw new Error(errorData.error || 'Network response was not ok');
            }

            if (!contentType || !contentType.includes('image/svg+xml')) {
                console.error('意外的响应类型:', contentType);
                throw new Error('Unexpected response type');
            }

            const svgContent = await response.text();
            if (!svgContent.includes('<svg')) {
                console.error('效的 SVG 内容:', svgContent);
                throw new Error('Invalid SVG content');
            }

            chartContainer.innerHTML = svgContent;
            updateDownloadButtons(true);

        } catch (error) {
            console.error('错误:', error);
            alert(translations[currentLang].errorAlert + '\n' + error.message);
            updateDownloadButtons(false);
        }
    }

    // 生成图表事件监听
    generateBtns.forEach(btn => {
        btn.addEventListener('click', async function() {
            const data = getTableData();
            if (data.values.length === 0) {
                alert(translations[currentLang].noDataAlert);
                return;
            }
            await generateChart(data);
        });
    });

    // 下载 SVG 格式
    function downloadSVG() {
        const svg = chartContainer.querySelector('svg');
        if (svg) {
            const svgData = new XMLSerializer().serializeToString(svg);
            const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(svgBlob);

            const link = document.createElement('a');
            link.href = url;
            link.download = 'sunburst_chart.svg';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }
    }

    // 下载 PNG 格式
    async function downloadPNG() {
        const svg = chartContainer.querySelector('svg');
        if (svg) {
            try {
                // 创建一个 canvas
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');

                // 获取 SVG 的尺寸
                const svgData = new XMLSerializer().serializeToString(svg);
                const svgBlob = new Blob([svgData], { type: 'image/svg+xml;charset=utf-8' });
                const svgUrl = URL.createObjectURL(svgBlob);

                // 创建图片对象
                const img = new Image();
                img.src = svgUrl;

                await new Promise((resolve, reject) => {
                    img.onload = () => {
                        // 设置 canvas 尺寸
                        canvas.width = img.width * 2; // 2倍大小以获得更好的质量
                        canvas.height = img.height * 2;
                        ctx.scale(2, 2);

                        // 绘制白色背景
                        ctx.fillStyle = 'white';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);

                        // 绘制 SVG
                        ctx.drawImage(img, 0, 0);

                        // 转换为 PNG 并下载
                        canvas.toBlob((blob) => {
                            const url = URL.createObjectURL(blob);
                            const link = document.createElement('a');
                            link.href = url;
                            link.download = 'sunburst_chart.png';
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                            URL.revokeObjectURL(url);
                            URL.revokeObjectURL(svgUrl);
                            resolve();
                        }, 'image/png');
                    };
                    img.onerror = reject;
                });
            } catch (error) {
                console.error('PNG 导出错误:', error);
                alert('PNG 导出失败，请尝试使用 SVG 格式');
            }
        }
    }

    // 更新下载按钮状态
    function updateDownloadButtons(enabled) {
        document.querySelectorAll('[id^="downloadSVG-"]').forEach(btn => btn.disabled = !enabled);
        document.querySelectorAll('[id^="downloadPNG-"]').forEach(btn => btn.disabled = !enabled);
    }

    // 添加下载按钮事件监听
    document.querySelectorAll('[id^="downloadSVG-"]').forEach(btn => {
        btn.addEventListener('click', downloadSVG);
    });

    document.querySelectorAll('[id^="downloadPNG-"]').forEach(btn => {
        btn.addEventListener('click', downloadPNG);
    });

    // 颜色选择器同步
    colorScheme.addEventListener('input', e => {
        const value = e.target.value;
        if (/^#[0-9A-F]{6}$/i.test(value)) {
            colorScheme.value = value;
        }
    });

    // 色板点击事件
    document.querySelectorAll('.palette-color').forEach(color => {
        color.addEventListener('click', function() {
            const selectedColor = this.dataset.color;
            colorScheme.value = selectedColor;
        });
    });

    // 更新颜色预览
    function updateColorPreview(schemeName) {
        // 清空预览区域
        colorPreview.innerHTML = '';

        // 创建临时 canvas 获取颜色
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 100, 0);

        // 获取5个代表色
        for (let i = 0; i < 5; i++) {
            const color = getColorFromScheme(schemeName, i / 4);
            const sample = document.createElement('div');
            sample.className = 'color-sample';
            sample.style.backgroundColor = color;
            sample.title = color;
            colorPreview.appendChild(sample);
        }
    }

    // 从配色方案获取色
    function getColorFromScheme(scheme, position) {
        const colors = {
            'viridis': ['#440154', '#414487', '#2a788e', '#22a884', '#7ad151'],
            'plasma': ['#0d0887', '#6a00a8', '#b12a90', '#e16462', '#fca636'],
            'inferno': ['#000004', '#420a68', '#932667', '#dd513a', '#fca50a'],
            'magma': ['#000004', '#3b0f70', '#8c2981', '#de4968', '#fdb42f'],
            'cividis': ['#00224e', '#274d8f', '#6c8a94', '#b5b17d', '#ffe945'],
            'rainbow': ['#6e40aa', '#1c80e7', '#00c6a6', '#97d42a', '#ff0000'],
            'tab10': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
            'Set3': ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3'],
            'Paired': ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99'],
            'hsv': ['#ff0000', '#ffff00', '#00ff00', '#00ffff', '#0000ff']
        };

        return colors[scheme][Math.floor(position * 5)];
    }

    // 随机选择颜色方案
    function randomizeColorScheme() {
        const randomIndex = Math.floor(Math.random() * colorSchemes.length);
        const newScheme = colorSchemes[randomIndex];
        colorScheme.value = newScheme;
        updateColorPreview(newScheme);
    }

    // 添加事件监听器
    colorScheme.addEventListener('change', () => updateColorPreview(colorScheme.value));
    randomColorBtn.addEventListener('click', randomizeColorScheme);

    // 初始化颜色预览
    updateColorPreview(colorScheme.value);

    // 添加字体大小滑块事件监听
    const fontSizeSlider = document.getElementById('fontSize');
    const fontSizeValue = document.getElementById('fontSizeValue');

    fontSizeSlider.addEventListener('input', function() {
        fontSizeValue.textContent = `${this.value}px`;
    });

    // 添加颜色输入同步
    const labelColor = document.getElementById('labelColor');
    const labelColorHex = document.getElementById('labelColorHex');

    labelColor.addEventListener('input', function() {
        labelColorHex.value = this.value;
    });

    labelColorHex.addEventListener('input', function() {
        const value = this.value;
        if (/^#[0-9A-F]{6}$/i.test(value)) {
            labelColor.value = value;
        }
    });

    // 初始化表格列数
    updateTableColumns();
});