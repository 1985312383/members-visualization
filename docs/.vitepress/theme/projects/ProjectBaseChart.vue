<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
    extraConfig: {
        type: Object,
        required: true,
    },
    loadChartData: {
        type: Function,
        required: true,
    },
})

let chartInstance = null;
const chartRef = ref(null)
const chartDataSource = ref(null)
const loading = ref(false)
const error = ref(null)
const isDark = ref(false)

const checkDarkMode = () => {
    if (typeof window !== 'undefined') {
        isDark.value = document.documentElement.classList.contains('dark')
    }
}

const getEChartsTheme = () => {
    return isDark.value ? 'dark' : 'light'
}


const generateSeriesList = async (dataSource) => {
    const seriesList = [];
    dataSource.forEach((item) => {
        // 检查 monthly_total_stars 是否存在且有效
        if (!item.monthly_total_stars || typeof item.monthly_total_stars !== 'object') {
            console.warn(`项目 ${item.name} 缺少 monthly_total_stars 数据，跳过该项目`);
            return;
        }

        const data = Object.keys(item.monthly_total_stars).map((month) => item.monthly_total_stars[month] || 0);
        if (data.some((value, index) => index > 0 && value === 0 && data[index - 1] !== 0)) {
            return
        }
        seriesList.push({
            name: item.name,
            type: 'line',
            smooth: true,
            endLabel: {
                show: true,
                formatter: (params) => {
                    const name = params.seriesName;
                    return name.length > 10 ? name.substring(0, 10) + '...' : name;
                },
                distance: 20,
            },
            data: data,
            source: item
        });
    });
    return { seriesList };
};

const getChartOption = async (dataSource) => {
    const { seriesList } = await generateSeriesList(dataSource)

    // 处理空数据的情况
    if (!dataSource || dataSource.length === 0 || seriesList.length === 0) {
        throw new Error('没有可用的数据来显示图表');
    }

    // 获取第一个有效的数据项的月份数据
    let xAxisData = [];
    for (const item of dataSource) {
        if (item.monthly_total_stars && typeof item.monthly_total_stars === 'object') {
            xAxisData = Object.keys(item.monthly_total_stars);
            break;
        }
    }

    if (xAxisData.length === 0) {
        throw new Error('无法获取月份数据');
    }

    const option = {
        tooltip: {
            trigger: 'item'
        },
        legend: {
            type: 'scroll',
            orient: 'horizontal',
            data: seriesList.map((item) => item.name),
            left: 0,
            top: 30,
        },
        grid: {
            left: 0,
            right: 150,
            bottom: 30,
            top: 100,
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xAxisData
        },
        yAxis: {
            type: 'value',
        },
        series: seriesList,
        ...props.extraConfig,
    };
    return option
}

const initChart = async () => {
    try {
        loading.value = true
        error.value = null
        chartDataSource.value = await props.loadChartData()

        // 检查数据是否为空
        if (!chartDataSource.value || chartDataSource.value.length === 0) {
            error.value = '暂无数据可显示。这可能是首次运行或历史数据缺失。'
            return;
        }

        const chartOption = await getChartOption(chartDataSource.value)
        chartInstance = echarts.init(chartRef.value, getEChartsTheme())
        chartInstance.setOption(chartOption)
    } catch (err) {
        console.error('图表初始化错误:', err);
        error.value = err.message || '加载数据时出错'
    } finally {
        loading.value = false
    }
}

const refreshChart = async (theme) => {
    chartInstance.dispose()
    const chartOption = await getChartOption(chartDataSource.value)
    chartInstance = echarts.init(chartRef.value, getEChartsTheme())
    chartInstance.setOption(chartOption)
}

// 监听主题变化
const observeThemeChange = () => {
    if (typeof window !== 'undefined') {
        const observer = new MutationObserver(() => {
            const newIsDark = document.documentElement.classList.contains('dark')
            if (newIsDark !== isDark.value) {
                isDark.value = newIsDark
                refreshChart()
            }
        })
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['class']
        })
    }
}

onMounted(async () => {
    checkDarkMode()
    observeThemeChange()

    await nextTick()
    await initChart()
})
</script>

<template>
    <div class="wrapper">
        <div v-if="loading" class="loading">
            <p>正在加载数据...</p>
        </div>

        <div v-else-if="error" class="error">
            <p>⚠️ {{ error }}</p>
            <p style="font-size: 14px; margin-top: 10px; opacity: 0.8;">
                提示：首次运行时可能没有历史数据用于对比。请等待下次数据更新。
            </p>
        </div>

        <div v-else ref="chartRef" class="chart"></div>
    </div>
</template>

<style scoped>
.wrapper {
    width: 100%;
    padding: 20px 0;
}

.chart {
    width: 100%;
    height: 600px;
}

.loading,
.error {
    text-align: center;
    padding: 60px;
    font-size: 18px;
    border-radius: 12px;
    margin: 20px 0;
}

.error {
    color: #e74c3c;
    background: #fdf2f2;
    border: 1px solid #fecaca;
}

.loading {
    color: #3498db;
    background: #f0f9ff;
    border: 1px solid #bae6fd;
}
</style>
