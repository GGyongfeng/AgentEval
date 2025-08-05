<template>
  <div class="admin-layout-simple">
    <div class="sidebar-simple">
      <h3>导航</h3>
      <ul>
        <li><router-link to="/">首页</router-link></li>
        <li><router-link to="/trajectory">轨迹可视化</router-link></li>
      </ul>
    </div>
    <div class="main-content-simple">
      <router-view></router-view>
    </div>
  </div>
</template>

<script lang="ts" setup>
console.log('AdminLayout loaded')
</script>

<style scoped>
.admin-layout-simple {
  display: flex;
  height: 100vh;
}

.sidebar-simple {
  width: 200px;
  background: #304156;
  color: white;
  padding: 20px;
}

.sidebar-simple h3 {
  margin-bottom: 20px;
}

.sidebar-simple ul {
  list-style: none;
  padding: 0;
}

.sidebar-simple li {
  margin-bottom: 10px;
}

.sidebar-simple a {
  color: white;
  text-decoration: none;
  padding: 8px 12px;
  display: block;
  border-radius: 4px;
}

.sidebar-simple a:hover,
.sidebar-simple a.router-link-active {
  background: #409EFF;
}

.main-content-simple {
  flex: 1;
  padding: 20px;
  background: #f0f2f5;
  overflow-y: auto;
}
</style> 