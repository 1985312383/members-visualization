<script setup>
import { ref, watch } from 'vue'

// 接收organizationData作为props
const props = defineProps({
  organizationData: {
    type: Array,
    default: () => []
  }
})

// 表格数据状态
const tableData = ref(props.organizationData)

// 格式化数字（添加千位分隔符）
const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 当props变化时更新表格数据
watch(() => props.organizationData, (newData) => {
  tableData.value = newData
}, { deep: true })
</script>

<template>
  <div>
    <!-- 空数据提示 -->
    <div v-if="!tableData || tableData.length === 0" class="no-data">
      <p>暂无组织数据可显示</p>
      <p style="font-size: 14px; opacity: 0.7; margin-top: 10px;">
        这可能是首次运行或数据缺失。请等待下次数据更新。
      </p>
    </div>

    <!-- 数据表格 -->
    <table v-else class="organization-table">
      <thead>
        <tr>
          <th>排名</th>
          <th>组织名称</th>
          <th>Star数</th>
          <th>新增Star</th>
          <th>排名变化</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="item in tableData"
          :key="item.name"
          :class="{ 'highlight-row': item.name === 'datawhalechina' }"
        >
          <td>
            <span class="rank-number">{{ item.rank }}</span>
          </td>
          <td class="name-cell">
            <!-- 只有datawhalechina添加链接 -->
            <template v-if="item.name === 'datawhalechina'">
              <a
                href="https://github.com/datawhalechina"
                target="_blank"
                rel="noopener noreferrer"
                class="datawhale-link"
              >
                {{ item.name }}
              </a>
            </template>
            <template v-else>
              {{ item.name }}
            </template>
          </td>
          <td>{{ formatNumber(item.star_count) }}</td>
          <td>+{{ formatNumber(item.starAdd || 0) }}</td>
          <td>
            <span :class="{ 'positive': item.rankAdd > 0, 'negative': item.rankAdd < 0 }">
              {{ item.rankAdd > 0 ? '+' : '' }}{{ item.rankAdd || 0 }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.organization-table {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
}

.organization-table th {
  padding: 14px 16px;
  text-align: left;
  font-weight: 600;
  font-size: 14px;
}

.organization-table td {
  padding: 12px 16px;
  font-size: 14px;
}

.rank-number {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  background: var(--vp-c-brand-1);
  color: white;
  border-radius: 50%;
  font-size: 14px;
}

.name-cell {
  font-weight: 500;
}

/* 链接样式 */
.datawhale-link {
  color: rgb(34, 101, 203);
  text-decoration: none; /* 去除下划线 */
  transition: all 0.2s ease;
}

.datawhale-link:hover {
  text-decoration: underline; /* 悬浮时显示下划线 */
}

.positive {
  color: var(--vp-c-success-1);
  font-weight: 500;
}

.negative {
  color: var(--vp-c-danger-1);
  font-weight: 500;
}

.no-data {
  text-align: center;
  padding: 60px 20px;
  border-radius: 12px;
  background: #f5f5f5;
  color: #666;
  font-size: 16px;
}

:deep(.dark) .no-data {
  background: #2a2a2a;
  color: #999;
}

/* 高亮行样式 - 整体边框和阴影 */
.highlight-row {
  background-color: rgba(78, 205, 196, 0.1);
  border: 2px solid #4ecdc4;
  box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
  transition: all 0.3s ease;
}

/* 文字样式 */
.highlight-row .name-cell {
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  font-size: 15px;
  transition: all 0.3s ease;
}

/* 悬浮效果增强 */
.highlight-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(78, 205, 196, 0.4);
  border-color: #38b2ac;
}

.highlight-row:hover .name-cell {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .search-box {
    max-width: 100%;
  }

  .organization-table {
    font-size: 13px;
  }

  .organization-table th,
  .organization-table td {
    padding: 10px 8px;
  }

  .rank-number {
    width: 24px;
    height: 24px;
    line-height: 24px;
    font-size: 12px;
  }

  .highlight-row {
    border-width: 1.5px;
    box-shadow: 0 3px 8px rgba(78, 205, 196, 0.25);
  }
}
</style>
