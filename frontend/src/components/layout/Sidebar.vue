<!-- 侧边栏导航 - 参考 zeroclaw Sidebar，支持主题切换 -->
<!-- @author fortune -->
<!-- @date 2026-03-18 -->

<template>
  <aside
    class="fixed top-0 left-0 h-screen w-60 flex flex-col transition-colors duration-300"
    :style="{ background: 'var(--dp-bg-sidebar)' }"
  >
    <div class="sidebar-glow-line" />
    <div
      class="flex items-center gap-3 px-4 py-4 border-b transition-colors"
      :class="theme === 'dark' ? 'border-[#1a1a3e]/50' : 'border-[#e2e8f0]'"
    >
      <div
        class="h-10 w-10 rounded-xl bg-gradient-to-br from-[#0080ff] to-[#00d4ff] flex items-center justify-center text-lg font-bold"
      >
        D
      </div>
      <span class="text-lg font-bold text-gradient-blue tracking-wide">
        DramaPipeline
      </span>
    </div>
    <nav class="flex-1 overflow-y-auto py-4 px-3 space-y-1">
      <router-link
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        custom
        v-slot="{ isActive, href, navigate }"
      >
        <a
          :href="href"
          @click="navigate"
          :class="[
            'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 group',
            isActive
              ? 'text-[var(--dp-text-primary)] shadow-[0_0_15px_rgba(0,128,255,0.2)]'
              : 'text-[var(--dp-text-muted)] hover:text-[var(--dp-text-primary)] hover:bg-[#0080ff08]',
          ]"
          :style="
            isActive
              ? {
                  background:
                    'linear-gradient(135deg, rgba(0,128,255,0.15), rgba(0,128,255,0.05))',
                }
              : {}
          "
        >
          <component
            :is="item.icon"
            :class="[
              'h-5 w-5 flex-shrink-0 transition-colors duration-300',
              isActive ? 'text-[#0080ff]' : 'group-hover:text-[#0080ff80]',
            ]"
          />
          <span>{{ item.label }}</span>
          <div
            v-if="isActive"
            class="ml-auto h-1.5 w-1.5 rounded-full bg-[#0080ff]"
            style="box-shadow: 0 0 6px currentColor"
          />
        </a>
      </router-link>
    </nav>
    <div
      class="px-5 py-4 border-t transition-colors"
      :class="theme === 'dark' ? 'border-[#1a1a3e]/50' : 'border-[#e2e8f0]'"
    >
      <p
        class="text-[10px] tracking-wider uppercase transition-colors"
        :class="theme === 'dark' ? 'text-[#334060]' : 'text-[#94a3b8]'"
      >
        影视流水线控制台
      </p>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { h } from 'vue'
import { useTheme } from '@/composables/useTheme'

const { theme } = useTheme()

// 简单图标组件（无 lucide 依赖）
const LayoutDashboard = () =>
  h('svg', {
    xmlns: 'http://www.w3.org/2000/svg',
    width: 20,
    height: 20,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': 2,
  }, [
    h('rect', { x: 3, y: 3, width: 7, height: 9 }),
    h('rect', { x: 14, y: 3, width: 7, height: 5 }),
    h('rect', { x: 14, y: 12, width: 7, height: 9 }),
    h('rect', { x: 3, y: 16, width: 7, height: 5 }),
  ])
const GitBranch = () =>
  h('svg', {
    xmlns: 'http://www.w3.org/2000/svg',
    width: 20,
    height: 20,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': 2,
  }, [
    h('line', { x1: 6, y1: 3, x2: 6, y2: 15 }),
    h('circle', { cx: 18, cy: 6, r: 3 }),
    h('circle', { cx: 6, cy: 18, r: 3 }),
    h('path', { d: 'M18 9a9 9 0 0 1-9 9' }),
  ])
const MessageSquare = () =>
  h('svg', {
    xmlns: 'http://www.w3.org/2000/svg',
    width: 20,
    height: 20,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': 2,
  }, [
    h('path', { d: 'M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z' }),
  ])
const ListTodo = () =>
  h('svg', {
    xmlns: 'http://www.w3.org/2000/svg',
    width: 20,
    height: 20,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': 2,
  }, [
    h('rect', { x: 3, y: 5, width: 6, height: 6 }),
    h('path', { d: 'm3 17 2 2 4-4' }),
    h('path', { d: 'M13 5h8' }),
    h('path', { d: 'M13 17h8' }),
  ])
const Settings = () =>
  h('svg', {
    xmlns: 'http://www.w3.org/2000/svg',
    width: 20,
    height: 20,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    'stroke-width': 2,
  }, [
    h('path', {
      d: 'M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z',
    }),
    h('circle', { cx: 12, cy: 12, r: 3 }),
  ])

const navItems = [
  { to: '/', icon: LayoutDashboard, label: '工作台' },
  { to: '/chat', icon: MessageSquare, label: 'AI 对话' },
  { to: '/pipelines', icon: GitBranch, label: '流水线' },
  { to: '/tasks', icon: ListTodo, label: '任务列表' },
  { to: '/config', icon: Settings, label: '系统设置' },
]
</script>
