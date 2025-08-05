<template>
  <div class="trajectory-viewer">
    <div class="upload-section">
      <el-upload
        class="upload-area"
        drag
        :before-upload="handleFileUpload"
        :auto-upload="false"
        accept=".json"
        :show-file-list="false"
      >
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">
          将轨迹文件拖到此处，或<em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            只能上传 JSON 格式的轨迹文件
          </div>
        </template>
      </el-upload>
    </div>

    <div v-if="trajectoryData.length > 0" class="trajectory-content">
      <div class="trajectory-header">
        <h2>轨迹对话记录</h2>
        <div class="stats">
          <el-tag>总步骤: {{ trajectoryData.length }}</el-tag>
          <el-tag type="success">
            对话轮次: {{ totalConversations }}
          </el-tag>
        </div>
      </div>

      <div class="trajectory-list">
        <div 
          v-for="(step, index) in trajectoryData" 
          :key="index" 
          class="step-item"
        >
          <!-- 步骤标题 -->
          <div class="step-header">
            <div class="step-number">步骤 {{ step.step || index + 1 }}</div>
            <div class="step-meta">
              <el-tag v-if="step.timing" size="small">
                耗时: {{ formatDuration(step.timing.duration) }}
              </el-tag>
              <el-tag v-if="step.token_usage" size="small" type="info">
                Token: {{ step.token_usage.total_tokens }}
              </el-tag>
              <el-tag v-if="step.error" size="small" type="danger">
                错误
              </el-tag>
            </div>
          </div>

          <!-- 任务内容 -->
          <div v-if="step.task" class="task-section">
            <div class="section-title">任务</div>
            <div class="task-content">
              {{ step.task }}
            </div>
          </div>

          <!-- 对话消息 -->
          <div v-if="step.model_input_messages" class="messages-section">
            <div class="section-title">对话消息</div>
            <div class="messages-list">
              <div 
                v-for="(message, msgIndex) in step.model_input_messages" 
                :key="msgIndex"
                :class="['message-item', `message-${message.role}`]"
              >
                <div class="message-header">
                  <div class="role-badge" :class="`role-${message.role}`">
                    {{ getRoleDisplayName(message.role) }}
                  </div>
                </div>
                <div class="message-content">
                  <div 
                    v-for="(content, contentIndex) in message.content" 
                    :key="contentIndex"
                    class="content-block"
                  >
                    <div v-if="content.type === 'text'" class="text-content">
                      <pre>{{ content.text }}</pre>
                    </div>
                    <div v-else-if="content.type === 'image'" class="image-content">
                      <img :src="content.image_url?.url" alt="上传的图片" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 工具调用 -->
          <div v-if="step.tool_calls && step.tool_calls.length > 0" class="tools-section">
            <div class="section-title">工具调用</div>
            <div class="tools-list">
              <div 
                v-for="(tool, toolIndex) in step.tool_calls" 
                :key="toolIndex"
                class="tool-item"
              >
                <div class="tool-header">
                  <el-tag type="warning">{{ tool.function?.name || tool.type }}</el-tag>
                </div>
                <div v-if="tool.function?.arguments" class="tool-args">
                  <pre>{{ formatToolArgs(tool.function.arguments) }}</pre>
                </div>
              </div>
            </div>
          </div>

          <!-- 模型输出 -->
          <div v-if="step.model_output_message" class="output-section">
            <div class="section-title">模型输出</div>
            <div class="output-content">
              <div class="message-item message-assistant">
                <div class="message-header">
                  <div class="role-badge role-assistant">Assistant</div>
                </div>
                <div class="message-content">
                  <pre>{{ step.model_output_message.content || JSON.stringify(step.model_output_message, null, 2) }}</pre>
                </div>
              </div>
            </div>
          </div>

          <!-- 错误信息 -->
          <div v-if="step.error" class="error-section">
            <div class="section-title">错误信息</div>
            <div class="error-content">
              <el-alert 
                :title="step.error" 
                type="error" 
                :closable="false"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <el-empty description="请上传轨迹文件开始查看" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 轨迹数据
const trajectoryData = ref<any[]>([])

// 计算总对话轮次
const totalConversations = computed(() => {
  return trajectoryData.value.reduce((count, step) => {
    if (step.model_input_messages && step.model_input_messages.length > 0) {
      return count + 1
    }
    return count
  }, 0)
})

// 处理文件上传
const handleFileUpload = (file: File) => {
  if (!file.name.endsWith('.json')) {
    ElMessage.error('请上传 JSON 格式的文件')
    return false
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    try {
      const content = e.target?.result as string
      const data = JSON.parse(content)
      
      if (Array.isArray(data)) {
        trajectoryData.value = data
        ElMessage.success('轨迹文件加载成功')
      } else {
        ElMessage.error('轨迹文件格式不正确，应该是数组格式')
      }
    } catch (error) {
      ElMessage.error('JSON 文件解析失败')
    }
  }
  reader.readAsText(file)
  return false
}

// 获取角色显示名称
const getRoleDisplayName = (role: string) => {
  const roleMap: Record<string, string> = {
    'system': 'System',
    'user': 'User',
    'assistant': 'Assistant',
    'function': 'Function'
  }
  return roleMap[role] || role
}

// 格式化时长
const formatDuration = (duration: number) => {
  if (duration < 1) {
    return `${Math.round(duration * 1000)}ms`
  } else if (duration < 60) {
    return `${duration.toFixed(2)}s`
  } else {
    const minutes = Math.floor(duration / 60)
    const seconds = (duration % 60).toFixed(2)
    return `${minutes}m ${seconds}s`
  }
}

// 格式化工具参数
const formatToolArgs = (args: string | object) => {
  if (typeof args === 'string') {
    try {
      return JSON.stringify(JSON.parse(args), null, 2)
    } catch {
      return args
    }
  }
  return JSON.stringify(args, null, 2)
}
</script>

<style scoped>
.trajectory-viewer {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.upload-section {
  margin-bottom: 30px;
}

.upload-area {
  width: 100%;
}

.trajectory-content {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.trajectory-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.trajectory-header h2 {
  margin: 0;
  color: #303133;
}

.stats {
  display: flex;
  gap: 10px;
}

.trajectory-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.step-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 20px;
  background: #fafafa;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.step-number {
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
}

.step-meta {
  display: flex;
  gap: 8px;
}

.section-title {
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #f0f9ff;
  border-left: 4px solid #409eff;
  border-radius: 4px;
}

.task-section {
  margin-bottom: 20px;
}

.task-content {
  background: white;
  padding: 15px;
  border-radius: 6px;
  border: 1px solid #dcdfe6;
  white-space: pre-wrap;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  max-height: 200px;
  overflow-y: auto;
}

.messages-section {
  margin-bottom: 20px;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.message-item {
  border-radius: 8px;
  padding: 15px;
  margin: 10px 0;
}

.message-system {
  background: #f8f9fa;
  border-left: 4px solid #6c757d;
}

.message-user {
  background: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.message-assistant {
  background: #f1f8e9;
  border-left: 4px solid #4caf50;
}

.message-function {
  background: #fff3e0;
  border-left: 4px solid #ff9800;
}

.message-header {
  margin-bottom: 10px;
}

.role-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
}

.role-system {
  background: #6c757d;
  color: white;
}

.role-user {
  background: #2196f3;
  color: white;
}

.role-assistant {
  background: #4caf50;
  color: white;
}

.role-function {
  background: #ff9800;
  color: white;
}

.message-content {
  line-height: 1.6;
}

.content-block {
  margin-bottom: 10px;
}

.text-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 10px;
  border-radius: 4px;
}

.image-content img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.tools-section {
  margin-bottom: 20px;
}

.tools-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.tool-item {
  background: white;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  padding: 15px;
}

.tool-header {
  margin-bottom: 10px;
}

.tool-args {
  background: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
  max-height: 200px;
  overflow-y: auto;
}

.tool-args pre {
  margin: 0;
  white-space: pre-wrap;
}

.output-section {
  margin-bottom: 20px;
}

.output-content {
  background: white;
  border-radius: 6px;
  padding: 15px;
  border: 1px solid #dcdfe6;
}

.output-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  background: rgba(0, 0, 0, 0.05);
  padding: 10px;
  border-radius: 4px;
}

.error-section {
  margin-bottom: 20px;
}

.error-content {
  margin-top: 10px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .trajectory-viewer {
    padding: 10px;
  }
  
  .trajectory-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .step-header {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }
  
  .step-meta {
    flex-wrap: wrap;
  }
}
</style>
