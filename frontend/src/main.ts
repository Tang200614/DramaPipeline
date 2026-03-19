/**
 * DramaPipeline 前端入口
 * 初始化时应用已存储的主题
 * @author fortune
 * @date 2026-03-18
 */

import { createApp } from 'vue'

// 尽早应用主题，避免闪烁
const stored = localStorage.getItem('dramapipeline-theme')
if (stored === 'dark' || stored === 'light') {
  document.documentElement.setAttribute('data-theme', stored)
} else if (window.matchMedia('(prefers-color-scheme: light)').matches) {
  document.documentElement.setAttribute('data-theme', 'light')
}
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './index.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('./layouts/Layout.vue'),
      children: [
        { path: '', name: 'Dashboard', component: () => import('./views/Dashboard/index.vue') },
        { path: 'chat', name: 'Chat', component: () => import('./views/Chat/index.vue') },
        { path: 'pipelines', name: 'Pipelines', component: () => import('./views/Pipelines/index.vue') },
        { path: 'tasks', name: 'Tasks', component: () => import('./views/Tasks/index.vue') },
        { path: 'config', name: 'Config', component: () => import('./views/Config/index.vue') },
      ],
    },
  ],
})

createApp(App).use(router).mount('#app')
