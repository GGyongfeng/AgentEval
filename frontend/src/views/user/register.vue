<script setup lang="ts">
import { ref } from 'vue'

const form = ref({
  username: '',
  password: '',
  confirmPassword: '',
  email: ''
})

const handleRegister = () => {
  console.log('注册表单提交', form.value)
}
</script>

<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <h2 class="register-title">用户注册</h2>
      </template>
      
      <el-form :model="form" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>

        <el-form-item label="确认密码">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" />
        </el-form-item>

        <el-form-item label="邮箱">
          <el-input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleRegister" style="width: 100%">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.register-card {
  width: 100%;
  max-width: 400px;
}

.register-title {
  text-align: center;
  margin: 0;
  color: #333;
}
</style> 