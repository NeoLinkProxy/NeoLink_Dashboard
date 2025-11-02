<script setup lang="ts">
import './assets/main.css'
import { ref, onMounted, computed, reactive } from 'vue'
import { useRouter, useRoute  } from 'vue-router';
import Edition_logs from './components/Edition_logs.vue';
import { RouterLink } from 'vue-router';
import GreatDialog from './components/GreatDialog.vue'



onMounted(() => {
  const router = useRouter()
  const urlParams = new URLSearchParams(window.location.search)
  const refresh = urlParams.get('refresh')

  if (refresh) {
    router.push(decodeURIComponent(refresh))
  }

})

// import { useEventListener } from '@vueuse/core'

const errorinfo = ref('错误信息：\n')
const info = ref(' 一些信息')
const EL = ref<string>('')
const greatDialog = ref<InstanceType<typeof GreatDialog>>(GreatDialog)
// 创建全局可访问的状态对象
const globalState = reactive({
  info: info,
  errorinfo: errorinfo,
  updateInfo: (newInfo: string) => {
    info.value = newInfo;
  },
  updateErrorInfo: (newErrorInfo: string) => {
    errorinfo.value = newErrorInfo;
  },
  appendErrorInfo: (newErrorInfo: string) => {
    errorinfo.value += newErrorInfo;
  },
  updateIsChinaUser: (newIsChinaUser: boolean) => {
    window.IsChinaUser = newIsChinaUser;
  },
  GetIsChinaUser: async () => {
    try {
      const response = await fetch('http://localhost:23104/Get_is_china_user', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      if (response.ok) {
        const data = await response.json()
        globalState.updateIsChinaUser(data.IsChinaUser)
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
      // 类型检查
      if (error instanceof Error) {
        errorinfo.value += `获取用户是否在中国内地失败: ${error.message}。请复制内容并联系管理员\n`
        errorinfo.value += `详细错误: ${error.message} ${error.stack} ${error.name}\n`;
      } else {
        errorinfo.value += `获取用户是否在中国内地失败: 未知错误。请复制内容并联系管理员`
        errorinfo.value += `详细错误: 未知错误\n`;
      }
      // console.error('详细错误:', error, error_);
    }
  },
  greatDialog: greatDialog
});

// 将全局状态暴露到 window 对象上，供外部访问
onMounted(() => {
  window.appState = globalState;
});
const ReportError = async (error_: any) => {
  try {
    // alert(`发生错误，上报错误中：${error_}`)
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
        case 1004:
          errorMessage = '传递的信息不符合规范';
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
        case 1004:
          errorMessage = '传递的信息不符合规范';
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

const route = useRoute();

// 控制 nav-bar 是否显示
const showNavBar = computed(() => {
  return route.path !== '/Check';
});

onMounted(async () => {
  get_EL();
})

</script>

<template>
  <GreatDialog ref="greatDialog"></GreatDialog>
  <!-- <div class="logo_all">
    <div class="logo_frame">
      <img src="/Images/Sign_23XR_Bigger.png" alt="Sign_23XR_Bigger.png" class="logo" />
      <span class="logo_des">（开发方）</span>
      <span class="logo_des2">__________</span>
    </div>
  </div>
  <br> -->

  <div class="container">
    <div v-if="showNavBar" class="nav-bar">
      <RouterLink to="/" custom v-slot="{ href, route, isActive }">
        <a :href="href" :class="{ 'nav-item': true, 'active': isActive }">
          <span>NeoLink 仪表盘 NeoLink Dashboard</span>
        </a>
      </RouterLink>
      <RouterLink to="/Home" custom v-slot="{ href, route, isActive }">
        <a :href="href" :class="{ 'nav-item': true, 'active': isActive }">
          <span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 32 32">
              <path fill="currentColor" d="M16.612 2.214a1.01 1.01 0 0 0-1.242 0L1 13.419l1.243 1.572L4 13.621V26a2.004 2.004 0 0 0 2 2h20a2.004 2.004 0 0 0 2-2V13.63L29.757 15L31 13.428ZM18 26h-4v-8h4Zm2 0v-8a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v8H6V12.062l10-7.79l10 7.8V26Z"></path>
            </svg>
            主页
          </span>
        </a>
      </RouterLink>
      <RouterLink to="/Download/" custom v-slot="{ href, route, isActive }">
        <a :href="href" :class="{ 'nav-item': true, 'active': isActive }">
          <span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
              <path fill="currentColor" d="M19 9h-4V3H9v6H5l7 8zM4 19h16v2H4z"></path>
            </svg>
            下载
          </span>
        </a>
      </RouterLink>
      <RouterLink to="/Setting/" custom v-slot="{ href, route, isActive }">
        <a :href="href" :class="{ 'nav-item': true, 'active': isActive }">
          <span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 48 48">
              <defs>
                <mask id="ipTSetting0">
                  <g fill="#555" stroke="#fff" stroke-linejoin="round" stroke-width="4" data-swindex="0">
                    <path d="M36.686 15.171a15.37 15.37 0 0 1 2.529 6.102H44v5.454h-4.785a15.37 15.37 0 0 1-2.529 6.102l3.385 3.385l-3.857 3.857l-3.385-3.385a15.37 15.37 0 0 1-6.102 2.529V44h-5.454v-4.785a15.37 15.37 0 0 1-6.102-2.529l-3.385 3.385l-3.857-3.857l3.385-3.385a15.37 15.37 0 0 1-2.529-6.102H4v-5.454h4.785a15.37 15.37 0 0 1 2.529-6.102l-3.385-3.385l3.857-3.857l3.385 3.385a15.37 15.37 0 0 1 6.102-2.529V4h5.454v4.785a15.37 15.37 0 0 1 6.102 2.529l3.385-3.385l3.857 3.857z"></path>
                    <path d="M24 29a5 5 0 1 0 0-10a5 5 0 0 0 0 10Z"></path>
                  </g>
                </mask>
              </defs>
              <path fill="currentColor" d="M0 0h48v48H0z" mask="url(#ipTSetting0)"></path>
            </svg>
            设置
          </span>
        </a>
      </RouterLink>
      <RouterLink to="/More/" custom v-slot="{ href, route, isActive }">
        <a :href="href" :class="{ 'nav-item': true, 'active': isActive }">
          <span>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 48 48">
              <g fill="none">
                <path stroke="currentColor" stroke-linejoin="round" stroke-width="4" data-swindex="0" d="M24 44c11.046 0 20-8.954 20-20S35.046 4 24 4S4 12.954 4 24s8.954 20 20 20Z"></path>
                <circle cx="14" cy="24" r="3" fill="currentColor"></circle>
                <circle cx="24" cy="24" r="3" fill="currentColor"></circle>
                <circle cx="34" cy="24" r="3" fill="currentColor"></circle>
              </g>
            </svg>
            更多
          </span>
        </a>
      </RouterLink>
    </div>

    <RouterView />

    <div class="info">
      <p>{{ info }}</p>
    </div>

    <div class="error-info">
      <p>{{ errorinfo }}</p>
    </div>
  </div>
  <div class="poem">
    <span class="poem-line">有人视枯叶为华章</span>
    <span class="poem-line2">有人弃新枝为浊秧</span>
  </div>
</template>

<style>
body {
  background-color: #181818;
  margin: 0;
  min-height: 100vh;
  font-family: 'SmileySans-Oblique';
}
.poem {
  text-align: center;
  margin-top: 20px;
  padding: 20px;
  color: transparent;
}

.poem-line, .poem-line2 {
  color: #191919;
  font-size: 14px;
  /* display: inline-block; */
  display: block;
  color: transparent;
}

.poem-line {
  margin-left: -1.5em;
}

.poem-line2 {
  margin-left: 1.5em;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .poem-line {
    font-size: 12px;
  }
}

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
}

.nav-bar a{
  text-decoration: none;
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
</style>
