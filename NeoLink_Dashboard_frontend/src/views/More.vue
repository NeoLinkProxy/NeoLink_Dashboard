<script setup lang='ts'>
// import { useEventListener } from '@vueuse/core';
import { ref, onMounted } from 'vue'
import Edition_logs from '../components/Edition_logs.vue';
import { RouterLink } from 'vue-router';
import { openInBrowser, ReportError, showSponsorDialog } from '../tools/tools.ts'
// import GreatDialog from '../components/GreatDialog.vue'

const version = ref<string>('')
const about = ref<HTMLDivElement | null>(null)
const treasure = ref<HTMLDivElement | null>(null)
const feedback = ref<HTMLDivElement | null>(null)
const vote = ref<HTMLDivElement | null>(null)

// 控制菜单展开/收起状态
const menuStates = ref({
  about: true,
  treasure: false,
  feedback: false,
  vote: false
})

// 切换菜单状态
const toggleMenu = (menuName: 'about' | 'treasure' | 'feedback' | 'vote') => {
  if (menuName === 'about') {
    menuStates.value.about = true
    menuStates.value.treasure = false
    menuStates.value.feedback = false
    menuStates.value.vote = false
    if (about.value) {about.value.classList.add('active')}
    if (treasure.value) {treasure.value.classList.remove('active')}
    if (feedback.value) {feedback.value.classList.remove('active')}
    if (vote.value) {vote.value.classList.remove('active')}
  } else if (menuName === 'treasure') {
    menuStates.value.about = false
    menuStates.value.treasure = true
    menuStates.value.feedback = false
    menuStates.value.vote = false
    if (about.value) {about.value.classList.remove('active')}
    if (treasure.value) {treasure.value.classList.add('active')}
    if (feedback.value) {feedback.value.classList.remove('active')}
    if (vote.value) {vote.value.classList.remove('active')}
  } else if (menuName === 'feedback') {
    menuStates.value.about = false
    menuStates.value.treasure = false
    menuStates.value.feedback = true
    menuStates.value.vote = false
    if (about.value) {about.value.classList.remove('active')}
    if (treasure.value) {treasure.value.classList.remove('active')}
    if (feedback.value) {feedback.value.classList.add('active')}
    if (vote.value) {vote.value.classList.remove('active')}
  } else if (menuName === 'vote') {
    menuStates.value.about = false
    menuStates.value.treasure = false
    menuStates.value.feedback = false
    menuStates.value.vote = true
    if (about.value) {about.value.classList.remove('active')}
    if (treasure.value) {treasure.value.classList.remove('active')}
    if (feedback.value) {feedback.value.classList.remove('active')}
    if (vote.value) {vote.value.classList.add('active')}
  }
}

const showDialog1 = () => {
  let h1 = document.createElement('h1')
  h1.innerText = '赞助'
  let p = document.createElement('p')
  p.innerText = '暂时没有 赞助 页面 （悲）'
  document.getElementById('greatDialogContent')?.appendChild(h1)
  document.getElementById('greatDialogContent')?.appendChild(p)
  showSponsorDialog()
  // 监听
  document.getElementById('greatDialog')?.addEventListener('close', () => {
    document.getElementById('greatDialogContent')?.removeChild(h1)
    document.getElementById('greatDialogContent')?.removeChild(p)
  })
}

const get_version = async () => {
  try {
    window.appState?.updateInfo(' 正在获取版本')
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
      window.appState?.appendErrorInfo(`获取版本失败: ${error.message}。\n`)
    } else {
      window.appState?.appendErrorInfo(`获取版本失败: 未知错误。\n`)
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
      window.appState?.appendErrorInfo(`发送弹窗失败: ${error.message}。等待上报错误。\n`)
    } else {
      window.appState?.appendErrorInfo(`发送弹窗失败: 未知错误。等待上报错误。\n`)
    }
    ReportError(error);
  }
}

onMounted(async () => {
  window.appState?.GetIsChinaUser()
  get_version();
  if (about.value) {about.value.classList.add('active')}
})

</script>

<!-- template and style sections remain unchanged -->

<template>
  <!-- <GreatDialog ref="greatDialog"> -->
  <GreatDialog ref="greatDialog"></GreatDialog>
  <div class="sidebar-container">
    <!-- 侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-menu">
        <br>
        <div ref="about" class="menu-item" @click="toggleMenu('about')">
          <div class="menu-icon">ⓘ</div>
          <div class="menu-text">关于与鸣谢</div>
          <div class="arrow">▼</div>
        </div>

        <!-- <div ref="treasure" class="menu-item" @click="toggleMenu('treasure')">
          <div class="menu-icon">📦</div>
          <div class="menu-text">百宝箱</div>
          <div class="arrow">▼</div>
        </div> -->

        <!-- <div ref="feedback" class="menu-item" @click="toggleMenu('feedback')">
          <div class="menu-icon">✉️</div>
          <div class="menu-text">反馈</div>
          <div class="arrow">▼</div>
        </div> -->

        <!-- <div ref="vote" class="menu-item" @click="toggleMenu('vote')">
          <div class="menu-icon">🗳️</div>
          <div class="menu-text">新功能投票</div>
          <div class="arrow">▼</div>
        </div> -->
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 关于与鸣谢内容 -->
      <div v-if="menuStates.about" class="content-section">
        <div class="section-header">
          <div class="section-title">关于</div>
          <div class="section-arrow">▲</div>
        </div>

        <div class="about-content">
          <div class="about-item">
            <div class="frame1">
              <div class="avatar"><img src="/Images/MyAvatar.png" alt="MyAvatar.png"></div>
              <div class="about-info">
                <div class="name">是星星与然然呀</div>
                <div class="role">NeoLink 仪表盘 NeoLink Dashboard 的开发者！</div>
              </div>
            </div>
            <div class="frame2"><div class="action-button" @click="showDialog1">赞助 NeoLinkDashboard！</div>
              <div class="action-button" @click="openInBrowser('https://github.com/NeoLinkProxy/NeoLink_Dashboard')">查看 NeoLink Dashboard 源代码</div>
              <div class="action-button" @click="openInBrowser('https://kkgithub.com/NeoLinkProxy/NeoLink_Dashboard')">查看 NeoLink Dashboard 源代码（镜像）</div>
            </div>
            <br>
            <div class="frame1">
              <div class="avatar"><img src="/Images/CeroxeAvatar.jpg" alt="CeroxeAvatar.jpg"></div>
              <div class="about-info">
                <div class="name">CeroxeAnivie</div>
                <div class="role">NeoLink 的开发者！</div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://github.com/CeroxeAnivie')">查看 CeroxeAnivie 主页</div>
              <div class="action-button" @click="openInBrowser('https://kkgithub.com/CeroxeAnivie')">查看 CeroxeAnivie 主页（镜像）</div>
            </div>
          </div>

          <div class="about-item">
            <div class="frame1">
              <div class="logo"><img src="/Images/NeoLink_仪表盘_NeoLink_Dashboard.png" alt="NeoLink_仪表盘_NeoLink_Dashboard.png"></div>
              <div class="about-info">
                <div class="name">NeoLinkDashboard</div>
                <div class="version">当前版本: {{ version || "加载中..." }}</div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://github.com/NeoLinkProxy/NeoLink_Dashboard')">查看源代码</div>
              <div class="action-button" @click="openInBrowser('https://kkgithub.com/NeoLinkProxy/NeoLink_Dashboard')">查看源代码（镜像）</div>
            </div>
          </div>

          <div class="about-item">
            <div class="frame1">
              <div class="logo_nl"><img src="/Images/NeoLink.png" alt="NeoLink.png"></div>
              <div class="about-info">
                <div class="name">NeoLink</div>
                <div class="version">一款好用的内网穿透软件！</div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://github.com/NeoLinkProxy/NeoLink')">查看 NeoLink 源代码</div>
              <div class="action-button" @click="openInBrowser('https://kkgithub.com/NeoLinkProxy/NeoLink')">查看 NeoLink 源代码（镜像）</div>
            </div>
          </div>
        </div>

        <div class="section-header">
          <div class="section-title">特别鸣谢</div>
          <div class="section-arrow">▲</div>
        </div>

        <div class="thank-you-list">
          <!-- <div class="thank-you-item">👤
            <div class="frame1">
              <div class="avatar"><img src="/Images/7ED.ico" alt="7ED.ico"></div>
              <div class="thank-you-info">
                <div class="name">7ED - GitMirror</div>
                <div class="description">提供 GitHub 的中国内地 文件镜像源 详见-></div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://www.7ed.net/gitmirror/hub.html')">查看镜像源（的使用方式）</div>
            </div>
          </div> -->

          <div class="thank-you-item">
            <div class="frame1">
              <div class="avatar"><img src="/Images/IPwho.is.svg" alt="IPwho.is.svg"></div>
              <div class="thank-you-info">
                <div class="name">IPwho.is</div>
                <div class="description">提供了<br>查询IP地址 以确定是否需要使用镜像网站。 详见-></div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://ipwhois.io/documentation')">查看文档</div>
            </div>
          </div>

          <div class="thank-you-item">
            <div class="frame1">
              <div class="avatar"><img src="/Images/KKGithub.jpg" alt="KKGithub.jpg"></div>
              <div class="thank-you-info">
                <div class="name">KGithub</div>
                <div class="description">提供了 Github 的中国内地 镜像！ 详见-></div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://github.com/kgithub666/kgithub')">查看项目</div>
              <div class="action-button" @click="openInBrowser('https://kkgithub.com/kgithub666/kgithub')">查看项目（镜像）</div>
              <div class="action-button" @click="openInBrowser('https://help.kkgithub.com/')">查看帮助</div>
            </div>
          </div>

          <div class="thank-you-item">
            <div class="frame1">
              <div class="avatar"><img src="/Images/FexCode.jpg" alt="FexCode.jpg"></div>
              <div class="thank-you-info">
                <div class="name">FexCode</div>
                <div class="description">帮助微调 UI</div>
              </div>
            </div>
            <div class="frame2">
              <div class="action-button" @click="openInBrowser('https://space.bilibili.com/3546840490314365')">其BiliBili页面</div>
              <!-- <div class="action-button2" @click="openInBrowser('https://kkgithub.com/kgithub666/kgithub')">查看项目（镜像）</div>
              <div class="action-button" @click="openInBrowser('https://help.kkgithub.com/')">查看帮助</div> -->
            </div>
          </div>

          <!-- <div class="thank-you-item">
            <div class="avatar">👤</div>
            <div class="thank-you-info">
              <div class="name">z0z0r4</div>
              <div class="description">提供了 MCIM 社区资源镜像源和帮助库图床！</div>
            </div>
            <div class="action-button">MCIM 主页</div>
          </div> -->

          <!-- <div class="thank-you-item">
            <div class="avatar">👤</div>
            <div class="thank-you-info">
              <div class="name">001100</div>
              <div class="description">提供了 Java Launch Wrapper 和一些重要服务支持！</div>
            </div>
            <div class="action-button">赞助</div>
          </div> -->

          <!-- <div class="thank-you-item">
            <div class="avatar">👤</div>
            <div class="thank-you-info">
              <div class="name">Patrick</div>
              <div class="description">设计并制作了 PCL 图标，让我从做图标的水深火热中得到了解脱……</div>
            </div>
            <div class="action-button">赞助</div>
          </div> -->
        </div>


        <div class="section-header">
          <div class="section-title">用户协议与免责声明</div>
          <div class="section-arrow">▲</div>
        </div>

        <div class="UAAD">
          <RouterLink to="/UAAD"><div class="action-button">查看用户协议与免责声明</div></RouterLink>
        </div>

      </div>

      <!-- 百宝箱内容 -->
      <div v-else-if="menuStates.treasure" class="content-section">
        <div class="section-header">
          <div class="section-title">百宝箱</div>
          <div class="section-arrow">▲</div>
        </div>

        <div class="treasure-content">
          <div class="guide-item">
            <div class="guide-icon">⛏️</div>
            <div class="guide-title">Minecraft 新手指南</div>
            <div class="guide-desc">针对 Minecraft 新玩家的入门教程</div>
          </div>

          <div class="guide-item">
            <div class="guide-icon">🧩</div>
            <div class="guide-title">整合包制作指南</div>
            <div class="guide-desc">介绍对整合包制作可能有用的 PCL 相关功能</div>
          </div>

          <div class="guide-item">
            <div class="guide-icon">📦</div>
            <div class="guide-title">资源安装指南</div>
            <div class="guide-desc">介绍如何安装下载到的各种游戏资源，例如 Mod、存档、纹理包（材质包）、光影等</div>
          </div>
        </div>
      </div>

      <!-- 反馈内容 -->
      <div v-else-if="menuStates.feedback" class="content-section">
        <div class="section-header">
          <div class="section-title">反馈</div>
          <div class="section-arrow">▲</div>
        </div>

        <div class="feedback-content">
          <div class="feedback-form">
            <textarea placeholder="请输入您的反馈内容..." rows="6"></textarea>
            <button class="submit-button">提交反馈</button>
          </div>
        </div>
      </div>

      <!-- 新功能投票内容 -->
      <div v-else-if="menuStates.vote" class="content-section">
        <div class="section-header">
          <div class="section-title">新功能投票</div>
          <div class="section-arrow">▲</div>
        </div>

        <div class="vote-content">
          <div class="vote-item">
            <div class="vote-title">功能一：优化启动速度</div>
            <div class="vote-description">提升启动器的启动速度和响应性能</div>
            <div class="vote-actions">
              <button class="vote-button">赞成</button>
              <button class="vote-button">反对</button>
            </div>
          </div>

          <div class="vote-item">
            <div class="vote-title">功能二：增加云同步功能</div>
            <div class="vote-description">支持用户配置文件的云同步，方便多设备使用</div>
            <div class="vote-actions">
              <button class="vote-button">赞成</button>
              <button class="vote-button">反对</button>
            </div>
          </div>

          <div class="vote-item">
            <div class="vote-title">功能三：改进界面设计</div>
            <div class="vote-description">优化用户界面，提供更好的用户体验</div>
            <div class="vote-actions">
              <button class="vote-button">赞成</button>
              <button class="vote-button">反对</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>


dialog::backdrop {
  background-color: rgba(0, 0, 0, 0.5);
}

.sidebar-container {
  display: flex;
  max-height: 60vh;
  background-color: #181818; /* 深色背景 */
}

.sidebar {
  width: 200px;
  /* background-color: #2d2d2d; 深灰色侧边栏 */
  border-right: 1px solid #444; /* 深色边框 */
  box-shadow: 0 0 8px rgba(0, 0, 0, 0.3); /* 更暗的阴影 */
  border-radius: 23px;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #444; /* 深色分隔线 */
}

.logo, .logo_nl {
  width: 180px;
  height: 180px;
  font-weight: bold;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.logo {
  background-color: #002850;
}

.logo_nl {
  background-color: #1C1E25;
}

.logo img, .logo_nl img {
  width: 128px;
  height: 128px;
  object-fit: cover;
}

.sidebar-menu {
  padding: 10px 0;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid #444; /* 深色分隔线 */
}

.menu-item:hover {
  background-color: #3d3d3d; /* 悬停时更浅的灰色 */
  border-radius: 4px;
}

.menu-item:active {
  background-color: #1d1d1d;
  border-radius: 4px;
}

.menu-item.active {
  background-color: #1d1d1d;
  border-radius: 4px;
}

.menu-icon {
  margin-right: 12px;
  font-size: 1.2em;
  color: #0066cc; /* 图标保持蓝色 */
}

.menu-text {
  flex: 1;
  font-size: 0.9em;
  color: #e0e0e0; /* 浅灰色文字 */
}

.arrow {
  font-size: 0.8em;
  color: #aaa; /* 灰色箭头 */
  transition: transform 0.2s ease;
}

.main-content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  background-color: #181818; /* 主内容区深色背景 */
  /* border: #555 1px solid; */
  border-radius: 23px;
  /* height: 80vh; */
  scrollbar-width: none;
  scrollbar-color: #181818;
  -webkit-scrollbar-color: #181818;
}

.main-content::-webkit-scrollbar{
  color: #181818;
  background-color: #181818;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  border: 1px solid #444; /* 深色边框 */
  border-radius: 4px;
  background-color: #2d2d2d; /* 深色输入框背景 */
  color: #e0e0e0; /* 浅色文字 */
  font-size: 0.9em;
}

.content-section {
  margin-bottom: 20px;
  background-color: #2d2d2d; /* 深色卡片背景 */
  border-radius: 4px;
  border: 1px solid #444; /* 深色边框 */
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background-color: #181818; /* 卡片标题背景 */
  border: 1px solid #444;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.section-header:hover {
  background-color: #383838; /* 悬停时更浅的灰色 */
}

.section-title {
  font-size: 0.9em;
  color: #e0e0e0; /* 浅灰色文字 */
}

.section-arrow {
  font-size: 0.8em;
  color: #aaa; /* 灰色箭头 */
  transition: transform 0.2s ease;
}

.guide-item {
  display: flex;
  padding: 12px 16px;
  margin-bottom: 8px;
  background-color: #2d2d2d; /* 深色卡片背景 */
  border: 1px solid #444;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.guide-item:hover {
  background-color: #3d3d3d; /* 悬停时更浅的灰色 */
  border-color: #555;
}

.guide-icon {
  margin-right: 12px;
  font-size: 1.2em;
  color: #0066cc; /* 图标保持蓝色 */
}

.guide-title {
  font-size: 0.9em;
  font-weight: 500;
  color: #e0e0e0; /* 浅灰色文字 */
}

.guide-desc {
  font-size: 0.8em;
  color: #aaa; /* 更浅的灰色描述文字 */
}

.logo {
  font-size: 1.2em;
  font-weight: bold;
  color: #0066cc; /* 保持蓝色文字 */
}

.about-content {
  padding: 16px;
  background-color: #181818; /* 深黑色背景 */
  border-radius: 8px;
  border: 1px solid #444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.about-item {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: auto;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 16px;
  background-color: #181818;
  border-radius: 4px;
  border: 1px solid #444;
}

.about-item .frame1 {
  grid-column: 1 / span 2;
}

.about-item .frame2{
  grid-column: 2;
}

.thank-you-item .frame1 {
  grid-column: 1 / span 2;
}

.thank-you-item .frame2{
  grid-column: 2;
  grid-row: 12;
}

.frame1 {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: auto;
}

.frame1 .avatar {
  grid-row: 1;
  grid-column: 1;
}

.frame1 .thank-you-info {
  grid-row: 1;
  grid-column: 2;
}

.frameq:last-child {
  margin-bottom: 0;
}

.frame2 {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: auto;
}

.frame2 {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: auto;
}

.frame1 {
  display: grid;
  grid-template-columns: auto;
  grid-template-rows: auto;
}

.frame1 .avatar {
  grid-row: 1;
  grid-column: 1;
}

.frame1 .about-info {
  grid-row: 1;
  grid-column: 2;
}

.about-item1:last-child {
  margin-bottom: 0;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #444;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2em;
  color: #ccc;
  margin-right: 12px;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.about-info {
  flex: 1;
  margin-right: 16px;
}

.name {
  font-weight: 500;
  color: #fff;
  margin-bottom: 4px;
}

.role, .version {
  font-size: 1em;
  color: #aaa;
}

.action-button {
  padding: 8px 16px;
  background-color: #002850;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.action-button:hover {
  background-color: #003d7a;
}

.thank-you-list {
  padding: 16px;
  background-color: #1a1a1a;
  border-radius: 8px;
  border: 1px solid #444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.thank-you-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  margin-bottom: 8px;
  background-color: #222222;
  border-radius: 4px;
  border: 1px solid #444;
}

.thank-you-item:last-child {
  margin-bottom: 0;
}

.thank-you-info {
  flex: 1;
  margin-right: 16px;
}

.UAAD {
  padding: 16px;
  background-color: #1a1a1a;
  border-radius: 8px;
}

.description {
  font-size: 0.9em;
  color: #aaa;
}

.treasure-content {
  padding: 16px;
  background-color: #1a1a1a;
  border-radius: 8px;
  border: 1px solid #444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.feedback-content {
  padding: 16px;
  background-color: #1a1a1a;
  border-radius: 8px;
  border: 1px solid #444;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.feedback-form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #2d2d2d;
  color: #e0e0e0;
  font-size: 0.9em;
  resize: vertical;
}

.feedback-form .submit-button {
  padding: 8px 16px;
  background-color: #003b75;
  color: rgb(158, 158, 158);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 8px;
  transition: background-color 0.2s ease;
}

.feedback-form .submit-button:hover {
  background-color: #0052a3;
}

.vote-content {
  padding: 16px;
  background-color: rgb(59, 59, 59);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.vote-item {
  padding: 12px 16px;
  margin-bottom: 16px;
  background-color: #2c2c2c;
  border-radius: 4px;
  border: 1px solid #555555;
}

.vote-item:last-child {
  margin-bottom: 0;
}

.vote-title {
  font-weight: 500;
  color: #616161;
  margin-bottom: 4px;
}

.vote-description {
  font-size: 0.9em;
  color: #666;
  margin-bottom: 8px;
}

.vote-actions {
  display: flex;
  gap: 8px;
}

.vote-button {
  padding: 6px 12px;
  background-color: #003061;
  color: rgb(158, 158, 158);
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.vote-button:hover {
  background-color: #0052a3;
}
</style>
