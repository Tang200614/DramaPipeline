<!-- 主布局 - 参考 zeroclaw Layout，支持主题切换 -->
<!-- 左侧固定导航 + 右侧主内容区 -->
<!-- @author fortune -->
<!-- @date 2026-03-18 -->

<template>
  <div
    class="min-h-screen transition-colors duration-300"
    :class="theme === 'dark' ? 'text-white' : 'text-[#1e293b]'"
    :style="{ background: 'var(--dp-bg-main)' }"
  >
    <Sidebar />
    <div class="ml-60 flex flex-col min-h-screen">
      <Header />
      <main class="flex-1 overflow-y-auto">
        <router-view v-slot="{ Component }">
          <transition
            name="page-fade"
            mode="out-in"
          >
            <component
              v-if="Component"
              :is="Component"
              :key="$route.path"
            />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import Sidebar from '@/components/layout/Sidebar.vue'
import Header from '@/components/layout/Header.vue'
import { useTheme } from '@/composables/useTheme'

const { theme } = useTheme()
</script>
