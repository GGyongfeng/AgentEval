import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import './assets/styles/main.scss'

const currentVersion = import.meta.env.VITE_APP_VERSION;
const cachedVersion = localStorage.getItem('app_version');

// 增加鲁棒性：确保版本号读取成功后才进行版本对比
if (currentVersion) {
  if (cachedVersion && cachedVersion !== currentVersion) {
    // 版本号不一致时清除缓存和刷新
    localStorage.clear();
    localStorage.setItem('app_version', currentVersion);
    window.location.reload();
  } else if (!cachedVersion) {
    // 首次访问时设置版本号
    localStorage.setItem('app_version', currentVersion);
  }
}else {
  console.warn('当前版本号未定义，请检查环境变量设置');
}

// 标题调用.env.VITE_APP_TITLE
document.title = import.meta.env.VITE_APP_TITLE || 'My Vue App';

const app = createApp(App);
app.use(router);
app.use(ElementPlus);
app.mount('#app');
