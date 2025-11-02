<script setup lang='ts'>
import router from '@/router/index.ts';
import { ReportError } from './tools/tools.ts'
import { onMounted, ref } from 'vue'

const props = defineProps<{
  onMountApp?: (IsChinaUser: boolean) => void
}>()

const IsChinaUser = ref<boolean>(false);
const CheckIsOk = ref<boolean>(false);
const CheckIsEnd = ref<boolean>(false);

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
      window.appState?.appendErrorInfo(`发送弹窗失败: ${error.message}。等待上报错误。\n`)
    } else {
      window.appState?.appendErrorInfo(`发送弹窗失败: 未知错误。等待上报错误。\n`)
    }
    ReportError(error);
  }
}

const CheckChinaUser = async () => {
  try {
    const response = await fetch('http://localhost:23104/check_china_user', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
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
    const data = await response.json();
    IsChinaUser.value = data.ischinauser
    CheckIsOk.value = true;
    CheckIsEnd.value = true;
    window.IsChinaUser = IsChinaUser.value
    window.appState?.updateIsChinaUser(IsChinaUser.value)
  } catch (error: unknown) {
    if (error instanceof Error) {
      window.appState?.appendErrorInfo(`检测是否为中国用户失败: ${error.message}。等待上报错误。\n`)
    } else {
      window.appState?.appendErrorInfo(`检测是否为中国用户失败: 未知错误。等待上报错误。\n`)
    }
    CheckIsOk.value = false;
    CheckIsEnd.value = true
    ReportError(error);
  }
}

onMounted(async () => {
  await CheckChinaUser()
  setTimeout(() => {
    // 调用 props 回调
    if (props.onMountApp) {
      props.onMountApp(IsChinaUser.value)
    }
    // 延迟路由跳转
    setTimeout(() => {
      router.push('/Home')
    }, 100)
  }, 3000)
})

</script>

<template>
  <div class="main-content">
    <!--加载中的东西-->
    <div class="loading">
      <div class="loading-bar"></div>
      <div v-if="!CheckIsEnd" class="loading-text">检测中，请耐心等待...</div>
      <p v-else class="loading-text">
        检测完成！
      </p>
      <p v-if="CheckIsOk && CheckIsEnd" class="loading-text">
        检测成功！
      </p>
      <p v-else-if="!CheckIsOk && CheckIsEnd" class="loading-text">
        检测失败！
      </p>
      <p v-else class="loading-text">
        _
      </p>
    </div>
  </div>

</template>

<style scoped>
/* 加载状态容器 */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  gap: 20px;
}

/* 加载动画条 */
.loading-bar {
  width: 200px;
  height: 4px;
  background-color: #333;
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.loading-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #4CAF50, #8BC34A);
  animation: loading 1.5s infinite;
}

/* 加载文本 */
.loading-text {
  color: #aaa;
  font-size: 16px;
  text-align: center;
}

/* 加载动画关键帧 */
@keyframes loading {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin: 20px 0;
}

</style>
