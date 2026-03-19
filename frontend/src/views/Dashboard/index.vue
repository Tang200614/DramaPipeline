<!-- 工作台 - 参考 zeroclaw Dashboard -->
<!-- @author fortune -->
<!-- @date 2026-03-18 21:55:00 -->

<template>
  <div class="p-6 space-y-6 animate-fade-in">
    <div v-if="error" class="rounded-xl bg-[#ff446615] border border-[#ff446630] p-4 text-[#ff6680]">
      加载失败: {{ error }}
    </div>
    <div
      v-else-if="!status"
      class="flex items-center justify-center h-64"
    >
      <div
        class="h-8 w-8 border-2 border-[#0080ff30] border-t-[#0080ff] rounded-full animate-spin"
      />
    </div>
    <template v-else>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div
          v-for="card in statusCards"
          :key="card.label"
          class="glass-card p-5 animate-slide-in-up"
        >
          <div class="flex items-center gap-3 mb-3">
            <div
              class="p-2 rounded-xl"
              :style="{ background: card.bg }"
            >
              <span class="text-lg" :style="{ color: card.color }">{{ card.icon }}</span>
            </div>
            <span class="text-xs uppercase tracking-wider font-medium text-[var(--dp-text-muted)]">
              {{ card.label }}
            </span>
          </div>
          <p class="text-lg font-semibold truncate capitalize text-[var(--dp-text-primary)]">
            {{ card.value }}
          </p>
          <p class="text-sm truncate text-[var(--dp-text-muted)]">{{ card.sub }}</p>
        </div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="glass-card p-5 animate-slide-in-up">
          <h2 class="text-sm font-semibold uppercase tracking-wider mb-5 text-[var(--dp-text-primary)]">
            系统状态
          </h2>
          <div class="space-y-3">
            <div
              v-for="(comp, name) in status.health.components"
              :key="name"
              class="rounded-xl p-3 border transition-all"
              :class="theme === 'dark' ? 'border-[#1a1a3e]' : 'border-[#e2e8f0]'"
              :style="theme === 'dark' ? { background: 'rgba(10, 10, 26, 0.5)' } : { background: 'rgba(248, 250, 252, 0.8)' }"
            >
              <div class="flex items-center gap-2">
                <span
                  class="inline-block h-2 w-2 rounded-full"
                  :class="comp.status === 'ok' ? 'bg-[#00e68a]' : 'bg-[#ff4466]'"
                />
                <span class="text-sm font-medium capitalize text-[var(--dp-text-primary)]">{{ name }}</span>
              </div>
              <p class="text-xs capitalize mt-1 text-[var(--dp-text-muted)]">{{ comp.status }}</p>
            </div>
          </div>
        </div>
        <div class="glass-card p-5 animate-slide-in-up">
          <h2 class="text-sm font-semibold uppercase tracking-wider mb-5 text-[var(--dp-text-primary)]">
            欢迎使用 DramaPipeline
          </h2>
          <p class="text-sm leading-relaxed text-[var(--dp-text-muted)]">
            影视流水线控制台，支持剧本分析、分镜设计、视频生成等流水线步骤。
            每步需用户确认后手动分发到下一阶段。
          </p>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getStatus, type StatusResponse } from '@/lib/api'
import { useTheme } from '@/composables/useTheme'

const { theme } = useTheme()

const status = ref<StatusResponse | null>(null)
const error = ref<string | null>(null)

const statusCards = computed(() => {
  if (!status.value) return []
  const s = status.value
  return [
    {
      icon: '⚙',
      color: '#0080ff',
      bg: '#0080ff15',
      label: 'Provider / Model',
      value: s.provider ?? 'DramaPipeline',
      sub: s.model,
    },
    {
      icon: '🌐',
      color: '#00e68a',
      bg: '#00e68a15',
      label: 'Gateway',
      value: `:${s.gateway_port}`,
      sub: `Locale: ${s.locale}`,
    },
    {
      icon: '💾',
      color: '#a855f7',
      bg: '#a855f715',
      label: 'Memory',
      value: s.memory_backend,
      sub: `Paired: ${s.paired ? 'Yes' : 'No'}`,
    },
    {
      icon: '✓',
      color: '#ff8800',
      bg: '#ff880015',
      label: 'Status',
      value: 'Running',
      sub: 'API 正常',
    },
  ]
})

onMounted(async () => {
  try {
    status.value = await getStatus()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Unknown error'
  }
})
</script>
