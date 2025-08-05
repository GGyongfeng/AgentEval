<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Document, 
  Operation, 
  Cpu, 
  Timer 
} from '@element-plus/icons-vue'

const router = useRouter()

// 模拟统计数据
const stats = ref({
  totalTrajectories: 12,
  avgSteps: 8.5,
  totalTokens: 125680,
  avgDuration: 4.2
})

// 功能卡片数据
const features = [
  {
    title: '轨迹可视化',
    description: '上传和查看 Agent 执行轨迹的详细对话记录',
    icon: 'Document',
    path: '/trajectory',
    color: '#409EFF'
  },
  {
    title: '数据分析',
    description: '分析 Agent 性能指标和执行效率',
    icon: 'TrendCharts',
    path: '/analysis',
    color: '#67C23A'
  },
  {
    title: '报告生成',
    description: '生成详细的评估报告和可视化图表',
    icon: 'Document',
    path: '/reports',
    color: '#E6A23C'
  }
]

const navigateToFeature = (path: string) => {
  router.push(path)
}
</script>

<template>
  <div class="home-page">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <h1>Agent 评估系统</h1>
      <p class="welcome-text">
        欢迎使用 Agent 评估系统，您可以上传轨迹文件进行可视化分析，查看 Agent 的执行过程和性能指标。
      </p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-section">
      <el-col :span="6" :sm="12" :xs="24">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalTrajectories }}</div>
            <div class="stat-label">轨迹文件</div>
          </div>
          <el-icon class="stat-icon" color="#409EFF"><Document /></el-icon>
        </el-card>
      </el-col>
      <el-col :span="6" :sm="12" :xs="24">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.avgSteps }}</div>
            <div class="stat-label">平均步骤数</div>
          </div>
          <el-icon class="stat-icon" color="#67C23A"><Operation /></el-icon>
        </el-card>
      </el-col>
      <el-col :span="6" :sm="12" :xs="24">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ (stats.totalTokens / 1000).toFixed(1) }}K</div>
            <div class="stat-label">总 Token 数</div>
          </div>
          <el-icon class="stat-icon" color="#E6A23C"><Cpu /></el-icon>
        </el-card>
      </el-col>
      <el-col :span="6" :sm="12" :xs="24">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.avgDuration.toFixed(1) }}s</div>
            <div class="stat-label">平均执行时间</div>
          </div>
          <el-icon class="stat-icon" color="#F56C6C"><Timer /></el-icon>
        </el-card>
      </el-col>
    </el-row>

    <!-- 功能区域 -->
    <div class="features-section">
      <h2>主要功能</h2>
      <el-row :gutter="20">
        <el-col 
          v-for="feature in features" 
          :key="feature.title"
          :span="8" 
          :sm="12" 
          :xs="24"
        >
          <el-card 
            class="feature-card" 
            shadow="hover"
            @click="navigateToFeature(feature.path)"
          >
            <div class="feature-content">
              <div class="feature-icon" :style="{ color: feature.color }">
                <el-icon size="40"><Document /></el-icon>
              </div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
              <el-button type="primary" :color="feature.color" size="small">
                立即使用
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快速开始 -->
    <div class="quick-start-section">
      <el-card>
        <template #header>
          <div class="card-header">
            <h3>快速开始</h3>
          </div>
        </template>
        <el-steps :active="0" finish-status="success">
          <el-step title="上传文件" description="选择并上传轨迹 JSON 文件" />
          <el-step title="查看轨迹" description="以对话形式查看 Agent 执行过程" />
          <el-step title="分析数据" description="查看性能指标和统计信息" />
          <el-step title="生成报告" description="导出分析报告和可视化图表" />
        </el-steps>
        <div class="quick-action">
          <el-button 
            type="primary" 
            size="large" 
            @click="navigateToFeature('/trajectory')"
          >
            开始使用轨迹可视化
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.home-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 40px;
}

.welcome-section h1 {
  font-size: 2.5rem;
  color: #303133;
  margin-bottom: 16px;
}

.welcome-text {
  font-size: 1.1rem;
  color: #606266;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
}

.stats-section {
  margin-bottom: 40px;
}

.stat-card {
  position: relative;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-content {
  padding: 10px 0;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-label {
  color: #909399;
  font-size: 0.9rem;
}

.stat-icon {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 2rem;
  opacity: 0.3;
}

.features-section {
  margin-bottom: 40px;
}

.features-section h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #303133;
}

.feature-card {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: #409EFF;
  box-shadow: 0 8px 25px rgba(64, 158, 255, 0.2);
}

.feature-content {
  text-align: center;
  padding: 20px 10px;
}

.feature-icon {
  margin-bottom: 16px;
}

.feature-content h3 {
  color: #303133;
  margin-bottom: 12px;
  font-size: 1.2rem;
}

.feature-content p {
  color: #606266;
  line-height: 1.5;
  margin-bottom: 20px;
  font-size: 0.9rem;
}

.quick-start-section {
  margin-bottom: 40px;
}

.card-header {
  display: flex;
  justify-content: center;
}

.card-header h3 {
  margin: 0;
  color: #303133;
}

.quick-action {
  text-align: center;
  margin-top: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-page {
    padding: 15px;
  }
  
  .welcome-section h1 {
    font-size: 2rem;
  }
  
  .stats-section {
    margin-bottom: 30px;
  }
  
  .stat-card {
    margin-bottom: 15px;
  }
  
  .features-section {
    margin-bottom: 30px;
  }
  
  .feature-card {
    margin-bottom: 20px;
  }
}
</style> 