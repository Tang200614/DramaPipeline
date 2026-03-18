<!-- 顶部栏 - 参考 zeroclaw Header，含主题切换 -->
<!-- @author fortune -->
<!-- @date 2026-03-18 -->

<template>
  <header
    class="flex items-center justify-between px-6 py-4 border-b transition-colors duration-300"
    :class="theme === 'dark' ? 'border-[#1a1a3e]/50' : 'border-[#e2e8f0]'"
    :style="theme === 'dark' ? { background: 'rgba(5, 5, 16, 0.6)' } : { background: 'rgba(255, 255, 255, 0.9)' }"
  >
    <h1
      class="text-sm font-semibold uppercase tracking-wider transition-colors"
      :class="theme === 'dark' ? 'text-[#556080]' : 'text-[#64748b]'"
    >
      {{ currentTitle }}
    </h1>
    <div class="flex items-center gap-4">
      <button
        type="button"
        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-all duration-300 hover:bg-[#0080ff15]"
        :class="theme === 'dark' ? 'text-[#8892a8]' : 'text-[#64748b]'"
        :title="theme === 'dark' ? '切换为亮色' : '切换为暗色'"
        @click="toggle"
      >
        <span v-if="theme === 'dark'" class="text-base">☀️</span>
        <span v-else class="text-base">🌙</span>
        <span>{{ theme === 'dark' ? '亮色' : '暗色' }}</span>
      </button>
      <span
        class="text-xs transition-colors"
        :class="theme === 'dark' ? 'text-[#334060]' : 'text-[#94a3b8]'"
      >
        DramaPipeline v0.1
      </span>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useTheme } from '@/composables/useTheme'

const route = useRoute()
const { theme, toggle } = useTheme()

const titleMap: Record<string, string> = {
  Dashboard: '工作台',
  Chat: 'AI 对话',
  Pipelines: '流水线',
  Tasks: '任务列表',
  Config: '系统设置',
}

const currentTitle = computed(() => {
  const name = route.name as string
  return titleMap[name] ?? '工作台'
})
</script>
