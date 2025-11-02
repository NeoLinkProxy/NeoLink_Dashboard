import { createApp, onMounted } from 'vue'
import StartAni from './StartAni.vue'
import Check from './Check.vue'
import App from './App.vue'
import router from './router'

// 提前创建路由实例
const mainApp = createApp(App)
mainApp.use(router)

// function initializeApp() {
//   // 检查当前路由是否为首页
//   const urlParams = new URLSearchParams(window.location.search)
//   const redirect = urlParams.get('redirect')

//   const isHomePage = window.location.pathname === '/' && redirect === null
  
//   // 只在首页显示启动动画
//   if (isHomePage) {
//     const startAnimApp = createApp(StartAni)
//     startAnimApp.mount('#StartAni')
    
//     // 动画完成后移除并挂载主应用
//     setTimeout(() => {
//       startAnimApp.unmount() // 更安全的卸载方式
//       document.getElementById('StartAni')?.remove()
//       mountMainApp()
//     }, 3000)
    
//   } else {
//     // 非首页直接挂载主应用
//     mountMainApp()
//   }
// }

function mountMainApp() {
  // 检查是否需要执行检查逻辑：只有在根路径或刷新时才检查
  const isRootPath = window.location.pathname === '/';
  const shouldRunCheck = isRootPath || window.shouldRunCheckOnLoad;
  
  if (window.IsChinaUser !== undefined && !shouldRunCheck) {
    // 如果已经设置过且不是根路径或不需要检查，则直接挂载主应用
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
  } else if (shouldRunCheck) {
    // 只有在需要检查时才挂载检查页面
    const checkApp = createApp(Check, {
        onMountApp: (IsChinaUser: boolean) => {
          const check = document.getElementById('Check')
          if (check) {
            check.animate([
              { opacity: '1' },
              { opacity: '0' }
            ], {
              duration: 500,
              fill: 'forwards'
            })
            window.IsChinaUser = IsChinaUser
            window.shouldRunCheckOnLoad = false; // 重置标志
            setTimeout(() => {
              checkApp.unmount()
              check.remove()
            }, 500)
          }
          setTimeout(() => {
            mountMainApp();
          }, 500)
        }
    })
    checkApp.mount('#Check')
    const check = document.getElementById('Check')
    if (!check) return
    check.animate([
      { opacity: '0' },
      { opacity: '1' }
    ], {
      duration: 500,
      fill: 'forwards'
    })
    // 设置标志，表示已经执行过检查
    window.shouldRunCheckOnLoad = false;
  } else {
    // 其他情况直接挂载主应用
    mainApp.mount('#app')
  }
}

// 在 initializeApp 函数中设置初始标志
function initializeApp() {
  // 设置初始检查标志
  window.shouldRunCheckOnLoad = window.location.pathname === '/';
  
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
      startAnimApp.unmount()
      document.getElementById('StartAni')?.remove()
      mountMainApp()
    }, 3000)
    
  } else {
    // 非首页直接挂载主应用
    mountMainApp()
  }
}

initializeApp()