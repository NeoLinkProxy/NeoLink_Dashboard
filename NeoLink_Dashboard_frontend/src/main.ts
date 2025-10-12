import { createApp, onMounted } from 'vue'
import StartAni from './StartAni.vue'
import App from './App.vue'
import router from './router'

// 提前创建路由实例
const mainApp = createApp(App)
mainApp.use(router)

function initializeApp() {
  // 检查当前路由是否为首页
  const urlParams = new URLSearchParams(window.location.search)
  const redirect = urlParams.get('redirect')

  const isHomePage = window.location.pathname === '/' && redirect === null
  
  // 只在首页显示启动动画
  if (isHomePage) {
    const startAnimApp = createApp(StartAni)
    startAnimApp.mount('#StartAni')
    
    // 动画完成后移除并挂载主应用
    setTimeout(() => {
      startAnimApp.unmount() // 更安全的卸载方式
      document.getElementById('StartAni')?.remove()
      mountMainApp()
      router.push('/Home')
    }, 3000)
    
  } else {
    // 非首页直接挂载主应用
    mountMainApp()
  }
}

function mountMainApp() {
  // if (!document.getElementById('app')) {
  //   const appDiv = document.createElement('div')
  //   appDiv.id = 'app'
  //   document.body.appendChild(appDiv)
  // }
  // if (res) {
  mainApp.mount('#app')
  const app = document.getElementById('app')
  if (!app) return
    app.animate([
      { opacity: '0' },
      { opacity: '1' }
    ], {
      duration: 500,
      fill: 'forwards'
  })
  // } else {
  //   mainApp.mount('#app')
  //   const app = document.getElementById('app')
  //   if (!app) return
  //   app.animate([
  //     { opacity: '0' },
  //     { opacity: '1' }
  //   ], {
  //     duration: 500,
  //     fill: 'forwards'
  //   })
  //   // 登录页面
  //   router.push('/Login')
  // }
}

initializeApp()