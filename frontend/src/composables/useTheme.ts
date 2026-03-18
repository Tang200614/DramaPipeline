/**
 * 主题切换 composable
 * 支持暗色/亮色切换，持久化到 localStorage
 * @author fortune
 * @date 2026-03-18
 */

import { ref, watch, onMounted } from 'vue'

const STORAGE_KEY = 'dramapipeline-theme'

export type Theme = 'dark' | 'light'

function getSystemPreference(): Theme {
  if (typeof window === 'undefined') return 'dark'
  return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark'
}

function getStoredTheme(): Theme | null {
  if (typeof window === 'undefined') return null
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'dark' || stored === 'light') return stored
  return null
}

function applyTheme(theme: Theme) {
  if (typeof document === 'undefined') return
  document.documentElement.setAttribute('data-theme', theme)
}

const theme = ref<Theme>(getStoredTheme() ?? getSystemPreference())

export function useTheme() {
  onMounted(() => {
    applyTheme(theme.value)
  })

  watch(theme, (val) => {
    applyTheme(val)
    localStorage.setItem(STORAGE_KEY, val)
  })

  function toggle() {
    theme.value = theme.value === 'dark' ? 'light' : 'dark'
  }

  function setTheme(val: Theme) {
    theme.value = val
  }

  return { theme, toggle, setTheme }
}
