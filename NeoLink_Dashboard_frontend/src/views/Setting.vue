<script setup lang='ts'>
// import { useEventListener } from '@vueuse/core';
import { ref, onMounted } from 'vue'
import Edition_logs from '../components/Edition_logs.vue';
import { RouterLink } from 'vue-router';

var errorinfo = ref('错误信息：\n')
var info = ref(' 一些信息')
var version = ref<string>('')
var EL = ref<string>('')

// 添加NLVersion响应式变量
const NLVersion = ref<string>('')

const theme = ref<string>('dark');
const language = ref<string>('zh-CN');
const autoUpdateCheck = ref<boolean>(true);

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
})

</script>

<!-- template and style sections remain unchanged -->

<template>
  <div class="main-content">
    <!-- 基本设置 -->
    <div class="setting-section">
      <div class="section-title">基本设置</div>
      <div class="setting-item">
        <div class="item-label">语言</div>
        <div class="item-value">
          <select v-model="language">
            <option value="zh-CN">中文</option>
            <!-- <option value="en-US">English</option> -->
          </select>
        </div>
      </div>
      <div class="setting-item">
        <div class="item-label">主题</div>
        <div class="item-value">
          <select v-model="theme">
            <option value="dark">深色</option>
            <!-- <option value="light">浅色</option> -->
          </select>
        </div>
      </div>
      <div class="setting-item">
        <div class="item-label">自动更新检查</div>
        <div class="item-value">
          <select v-model="autoUpdateCheck">
            <option value="true">开启</option>
            <option value="false">关闭</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 高级设置
    <div class="setting-section">
      <div class="section-title">高级设置</div>
      <div class="setting-item">
        <div class="item-label">服务器地址</div>
        <div class="item-value">
          <input type="text" v-model="serverAddress" placeholder="http://localhost:23104" />
        </div>
      </div>
      <div class="setting-item">
        <div class="item-label">超时时间（秒）</div>
        <div class="item-value">
          <input type="number" v-model="timeout" min="1" max="300" />
        </div>
      </div>
      <div class="setting-item">
        <div class="item-label">日志级别</div>
        <div class="item-value">
          <select v-model="logLevel">
            <option value="info">信息</option>
            <option value="warning">警告</option>
            <option value="error">错误</option>
          </select>
        </div>
      </div>
    </div>

      网络设置 
    <div class="setting-section">
      <div class="section-title">网络设置</div>
      <div class="setting-item">
        <div class="item-label">代理服务器</div>
        <div class="item-value">
          <input type="text" v-model="proxyServer" placeholder="http://proxy.example.com:8080" />
        </div>
      </div>
      <div class="setting-item">
        <div class="item-label">使用系统代理</div>
        <div class="item-value">
          <input type="checkbox" v-model="useSystemProxy" />
        </div>
      </div>
    </div> -->

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button class="save-button">保存设置</button>
      <button class="reset-button">重置为默认</button>
    </div>
  </div>

</template>

<style scoped>
.cancel-button {
  /* padding: 10px 20px; */
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
  /* background-color: #000; */
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
.games {
  display: grid;
  border: 1px solid #fff;
  height: 100%;
  /* 布局：一列，行数根据内部元素来定，可以动态切换的 */
  grid-template-columns: 1fr;
  /* gap: 1rem; */
}

.game {
  border: 1px solid #888888;
  margin: 1rem;
  display: grid;
  /* 实现图片在左，两个文字在右的布局 */
  grid-template-columns: 0.125fr 0.25fr;
  /* grid-template-rows: auto auto; */
  gap: 0.5rem;
  /* 让内容顶部对齐 */
  align-items: start;
  padding: 0.5rem;
}

/* 图片占据第一行到第二行，第一列 */
.game img {
  grid-column: 1;
  grid-row: 1 / span 3;
  /* width: 100%;
  height: 100%; */
  object-fit: cover;
  height: 128px;
  width: 128px;
}

/* 第一个文字元素在第二列第一行 */
.game p:first-of-type {
  grid-column: 2;
  grid-row: 1;
  margin: 0;
}

.game:nth-child(2) {
  grid-column: 2;
  grid-row: 2;
  margin: 0;
}

/* 第二个文字元素在第二列第二行 */
.game p:last-of-type {
  grid-column: 2;
  grid-row: 3;
  margin: 0;
}

.game.ig button {
  grid-column: 3;
  grid-row: 2;
  margin: 0;
  width: fit-content; /* 或者指定一个具体的宽度值，例如 100px */
  max-width: 100px; /* 防止按钮过度拉伸 */
}

.game.wg button {
  grid-column: 3;
  grid-row: 2;
  margin: 0;
  width: fit-content; /* 或者指定一个具体的宽度值，例如 100px */
  max-width: 100px; /* 防止按钮过度拉伸 */
}

.game button:first-of-type {
  grid-column: 3;
  grid-row: 1;
  margin: 0;
  width: fit-content; /* 或者指定一个具体的宽度值，例如 100px */
  max-width: 100px; /* 防止按钮过度拉伸 */
}

.game.ig button:last-of-type {
  grid-column: 3;
  grid-row: 3;
  margin: 0;
  width: fit-content; /* 或者指定一个具体的宽度值，例如 100px */
  max-width: 100px; /* 防止按钮过度拉伸 */
}

.game p {
  margin: 0;
  padding: 0; /* 确保没有内边距 */
}

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

.error-info {
  margin-top: 20px;
  padding: 10px;
  background-color: #222;
  border: 1px solid #444;
  font-size: 0.9em;
  color: #aaa;
}

.debug-info {
  margin-top: 20px;
  padding: 10px;
  background-color: #222;
  border: 1px solid #444;
  font-size: 0.9em;
  color: #aaa;
  /* display: none; */
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

.control-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin: 10px;
}

.control-button:hover {
  background-color: #459e48;
}

.control-button:active {
  background-color: #39833b;
}

.progress-container {
  grid-column: 1 / span 3;
  grid-row: 4;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.progress-bar {
  width: 100%;
  height: 20px;
  background-color: #333;
  border-radius: 10px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.3s ease;
}

.progress-text {
  white-space: nowrap;
  font-size: 14px;
}

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

.launch-section {
  display: flex;
  justify-content: center;
}

.launch-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px;
  border: 1px solid #585858;
  background-color: #181818;
  min-width: 200px;
  border-radius: 23%;
}

.launch-text {
  font-size: 1.5em;
  margin-bottom: 15px;
}

.nl-version {
  /* margin-bottom: 20px; */
  color: #4CAF50;
}

/* .launch-button {
  padding: 10px 30px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
} */

.launch-button:hover {
  background-color: #459e48;
}

.version-section {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.version-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border: 1px solid #585858;
  background-color: #181818;
  min-width: 150px;
  border-radius: 23%;
}

.box-title {
  font-weight: bold;
  margin-bottom: 15px;
}

.box-content {
  color: #aaa;
}

.setting-section {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #585858;
  background-color: #181818;
  border-radius: 8px;
}

.section-title {
  font-weight: bold;
  font-size: 1.2em;
  color: #4CAF50;
  margin-bottom: 15px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #444;
}

.item-label {
  flex: 1;
  color: #444444;
  white-space: nowrap;
}

.item-value {
  flex: 2;
  text-align: right;
  color: #292929;
}

.item-value select {
  padding: 5px 10px;
  font-size: 14px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #3a3a3a;
  color: #5e5e5e;
}

.item-value select:focus {
  background-color: #111111;
}

.setting-item:last-child {
  border-bottom: none;
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: flex-end;
  margin-top: 20px;
}

.save-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.save-button:hover {
  background-color: #459e48;
}

.reset-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.reset-button:hover {
  background-color: #d32f2f;
}
</style>
