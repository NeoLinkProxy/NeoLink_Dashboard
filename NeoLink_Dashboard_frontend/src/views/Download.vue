<script setup lang='ts'>
import { ref, onMounted } from 'vue'
import Edition_logs from '../components/Edition_logs.vue';
import { RouterLink } from 'vue-router';

var errorinfo = ref('错误信息：\n')
var info = ref(' 一些信息')
var version = ref<string>('')
var EL = ref<string>('')

// 添加NLVersion响应式变量
const NLVersion = ref<string>('')

// 添加获取NLVersion的方法
const get_NLVersion = async () => {
  try {
    info.value = ' 正在获取NL版本'
    const response = await fetch('http://localhost:23104/GetNowUseNLV/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await response.json()
    if (response.ok) {
      NLVersion.value = data.version || '未知版本'
      info.value = ' 获取NL版本成功'
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error: unknown) {
    if (error instanceof Error) {
      errorinfo.value += `获取NL版本失败: ${error.message}。\n`
    } else {
      errorinfo.value += `获取NL版本失败: 未知错误。\n`
    }
    ReportError(error);
  }
}

const get_version = async () => {
  try {
    info.value = ' 正在获取版本'
    const response = await fetch('http://localhost:23104/version', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await response.json()
    if (response.ok) {
      version.value = data.version
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error: unknown) {
    // 类型检查
    if (error instanceof Error) {
      errorinfo.value += `获取版本失败: ${error.message}。\n`
    } else {
      errorinfo.value += `获取版本失败: 未知错误。\n`
    }
    ReportError(error);
  }
}

const ReportError = async (error_: any) => {
  try {
    alert(`发生错误，上报错误中：${error_}`)
    const response = await fetch('http://localhost:23104/error', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: error_.message,
        stack: error_.stack,
        name: error_.name,
        timestamp: new Date().toISOString()
      }),
    });
  } catch (error: unknown) {
    // 类型检查
    if (error instanceof Error) {
      errorinfo.value += `上报错误失败: ${error.message}。请复制内容并联系管理员\n`
      errorinfo.value += `详细错误: ${error_.message} ${error_.stack} ${error_.name} ${error_.message} ${error_.stack} ${error_.name}\n`;
    } else {
      errorinfo.value += `上报错误失败: 未知错误。请复制内容并联系管理员`
      errorinfo.value += `详细错误: 未知错误 ${error_.message} ${error_.stack} ${error_.name} ${error_.message} ${error_.stack} ${error_.name}\n`;
    }
    // console.error('详细错误:', error, error_);
  }
}

// 新增：获取支持的版本列表
const supportedVersions = ref<string[]>([]);
const getSupportedVersions = async () => {
  try {
    info.value = ' 正在获取支持的版本列表'
    const response = await fetch('http://localhost:23104/GetSupportedVersions/', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    const data = await response.json()
    if (response.ok) {
      supportedVersions.value = data.versions || [];
      info.value = ' 获取支持的版本列表成功'
    } else {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
  } catch (error: unknown) {
    if (error instanceof Error) {
      errorinfo.value += `获取支持的版本列表失败: ${error.message}。\n`
    } else {
      errorinfo.value += `获取支持的版本列表失败: 未知错误。\n`
    }
    ReportError(error);
  }
}

const get_EL = async () => {
  try {
    const response = await fetch('http://localhost:23104/Edition_logs', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
    
    const data = await response.json()
    
    if (response.ok) {
      EL.value = data.Edition_logs
    } else {
      let errorMessage = '';
      switch (response.status) {
        case 1001:
          errorMessage = '操作被取消';
          break;
        case 1002:
          errorMessage = '已存在';
          break;
        case 1003:
          errorMessage = '请求的资源不存在';
          break;
        case 500:
          errorMessage = '服务器发生错误';
          break;
        default:
          errorMessage = `HTTP error! status: ${response.status}`;
      }
      throw new Error(errorMessage);
    }
  } catch (error: unknown) {
    if (error instanceof Error) {
      errorinfo.value += `获取版本日志失败: ${error.message}。等待上报错误。\n`
    } else {
      errorinfo.value += `获取版本日志失败: 未知错误。等待上报错误。\n`
    }
    ReportError(error);
  }
}

const SendPopup = async (title: string, message: string, type: 'info' | 'warning' | 'error') => {
  try {
    const response = await fetch('http://localhost:23104/show/popup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: title,
        message: message,
        type: type,
      }),
    });

    if (!response.ok) {
      let errorMessage = '';
      switch (response.status) {
        case 1001:
          errorMessage = '操作被取消';
          break;
        case 1002:
          errorMessage = '已存在';
          break;
        case 1003:
          errorMessage = '请求的资源不存在';
          break;
        case 500:
          errorMessage = '服务器发生错误';
          break;
        default:
          errorMessage = `HTTP error! status: ${response.status}`;
      }
      throw new Error(errorMessage);
    }
  } catch (error: unknown) {
    if (error instanceof Error) {
      errorinfo.value += `发送弹窗失败: ${error.message}。等待上报错误。\n`
    } else {
      errorinfo.value += `发送弹窗失败: 未知错误。等待上报错误。\n`
    }
    ReportError(error);
  }
}

onMounted(async () => {
  get_EL();
  get_version();
  get_NLVersion();
  getSupportedVersions(); // 添加获取支持版本的调用
})
</script>

<template>
  <div class="main-content">
    <!-- 支持的版本信息 -->
    <div class="download-info">
      <div class="version-info">
        <div class="version-title">NeoLink</div>
        <div class="version-desc">一款内网穿透软件，专为 Minecraft 联机 / Server 而生。<br>
          NeoLink下载地址：<a href="https://github.com/NeoLinkProxy/NeoLink">https://github.com/NeoLinkProxy/NeoLink</a><br>
          本GUI支持的版本：NeoLink >= 3.2</div>
      </div>
      
      <div class="versions-list">
        <div class="list-title">可用版本列表：</div>
        <div v-if="supportedVersions.length > 0" class="version-items">
          <div v-for="(versionItem, index) in supportedVersions" :key="index" class="version-item">
            NeoLink 版本 {{ versionItem }}
          </div>
        </div>
        <div v-else class="no-versions">
          暂无可用版本
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
.logo {
  /* 330px X 200px */
  width: calc(330px * 0.4);
  height: calc(200px * 0.4);
}

.logo_all {
  display: grid;
  grid-template-columns: auto auto auto; /* 三列布局 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  gap: 10px; /* 可选：添加元素间距 */
}

.logo_frame {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: auto auto;
  justify-items: center;
  align-items: center;
}

.logo_des {
  font-size: xx-small;
}

.logo_des2 {
  color: #202020;
  font-size: xx-small;
  /* 让用户不可框选 */
  user-select: none;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none;    /* Firefox */
  -ms-user-select: none;     /* IE10+/Edge */
}

.nn1 {
  color: #181818;
  font-size: xx-small;
  /* 让用户不可框选 */
  user-select: none;
  -webkit-user-select: none; /* Safari */
  -moz-user-select: none;    /* Firefox */
  -ms-user-select: none;     /* IE10+/Edge */
}

.cancel-button {
  font-size: 16px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px;
}

.cancel-button:hover {
  background-color: #d32f2f;
}

.cancel-button:active {
  background-color: #b71c1c;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #181818;
  color: #fff;
}

.header {
  text-align: center;
  border-bottom: 1px solid #fff;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 2em;
}

.download-info {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 20px 0;
}

.version-info {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  border: 1px solid #585858;
  background-color: #181818;
  border-radius: 8px;
}

.version-title {
  font-weight: bold;
  font-size: 1.2em;
  color: #4CAF50;
}

.version-desc {
  color: #aaa;
}

.versions-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  border: 1px solid #585858;
  background-color: #181818;
  border-radius: 8px;
}

.list-title {
  font-weight: bold;
  color: #4CAF50;
  margin-bottom: 10px;
}

.version-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.version-item {
  padding: 8px 12px;
  background-color: #222;
  border: 1px solid #444;
  border-radius: 4px;
  color: #fff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.version-item:hover {
  background-color: #333;
  transform: translateY(-1px);
}

.no-versions {
  color: #aaa;
  text-align: center;
  padding: 20px;
}

/* 保持原有样式不变 */
.nav-bar {
  display: grid;
  background-color: #222;
  border: 1px solid #3d3d3d;
  margin-bottom: 20px;
}

.nav-bar * {
  display: inline;
  grid-column: auto;
  grid-row: 1;
}

.nav-item {
  padding: 10px 20px;
  cursor: pointer;
  display: table;
  transition: all 0.2s ease;
  border-radius: 4px;
  margin: 0 5px;
  grid-column: auto;
  grid-row: 1;
}

.nav-item:hover {
  background-color: #333;
  transform: translateY(-1px);
}

.nav-item:active {
  background-color: #444;
  transform: translateY(0);
  font-weight: bold;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}

.nav-item.active {
  background-color: #444;
  font-weight: bold;
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3);
}

.nav-item:last-child {
  border-right: none;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin: 20px 0;
}

.info {
  margin-top: 20px;
  padding: 10px;
  background-color: #222;
  border: 1px solid #444;
  font-size: 0.9em;
  color: #aaa;
  border-radius: 23px;
}

.error-info {
  margin-top: 20px;
  padding: 10px;
  background-color: #222;
  border: 1px solid #444;
  font-size: 0.9em;
  color: #aaa;
}
</style>