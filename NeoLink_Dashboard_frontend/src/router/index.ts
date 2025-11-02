import { createRouter, createWebHistory } from 'vue-router'
import home from '../views/Home.vue'
import index from '../views/index.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/Home',
      name: 'home',
      component: home,
    },
    {
      path: '/',
      name: 'index',
      component: index,
    },
    {
      path: '/Setting',
      name: 'Setting',
      component: () => import('../views/Setting.vue')
    },
    {
      path: '/Setting_NeoLink',
      name: 'Setting_NeoLink',
      component: () => import('../views/Setting_NeoLink.vue')
    },
    {
      path: '/More',
      name: 'More',
      component: () => import('../views/More.vue')
    },
    {
      path: '/Download',
      name: 'Download',
      component: () => import('../views/Download.vue')
    },
    {
      path: '/UAAD',
      name: 'UAAD',
      component: () => import('../views/UserAgreementAndDisclaimer.vue')
    },
    // {
    //   path: '/Check',
    //   name: 'Check',
    //   component: () => import('../views/Check.vue')
    // },
  ],
})

export default router
