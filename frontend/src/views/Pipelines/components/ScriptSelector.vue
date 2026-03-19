<!-- 剧本与集数选择器 -->
<!-- @author fortune -->
<!-- @date 2026-03-19 -->

<template>
  <header class="flex-shrink-0 flex items-center justify-between px-6 py-3 border-b pipeline-header">
    <div class="flex items-center gap-4">
      <div class="selector-group">
        <span class="pipeline-label">剧本</span>
        <div class="script-selector">
          <select
            :model-value="scriptId"
            class="script-select"
            @change="onScriptChange"
          >
            <option
              v-for="s in scripts"
              :key="s.id"
              :value="s.id"
            >
              {{ s.title }}
            </option>
          </select>
          <span class="script-select-icon">⇅</span>
        </div>
      </div>
      <div class="selector-group">
        <span class="pipeline-label">集数</span>
        <div class="script-selector">
          <select
            :model-value="episodeId"
            class="script-select"
            @change="onEpisodeChange"
          >
            <option
              v-for="ep in episodes"
              :key="ep.id"
              :value="ep.id"
            >
              {{ ep.title }}
            </option>
          </select>
          <span class="script-select-icon">⇅</span>
        </div>
      </div>
    </div>
    <div class="pipeline-live-badge">
      <span class="live-dot" />
      <span>流水线运行中</span>
    </div>
  </header>
</template>

<script setup lang="ts">
const props = defineProps<{
  scriptId: string
  episodeId: string
  scripts: { id: string; title: string }[]
  episodes: { id: string; scriptId: string; title: string }[]
}>()
const emit = defineEmits<{
  'update:scriptId': [value: string]
  'update:episodeId': [value: string]
}>()

function onScriptChange(e: Event) {
  emit('update:scriptId', (e.target as HTMLSelectElement).value)
}

function onEpisodeChange(e: Event) {
  emit('update:episodeId', (e.target as HTMLSelectElement).value)
}
</script>

<style scoped>
.pipeline-header {
  border-color: var(--dp-border-subtle);
}

.pipeline-label {
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--dp-text-muted);
}

.selector-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.script-selector {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.script-select {
  appearance: none;
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid var(--dp-border);
  border-radius: 0.5rem;
  background: var(--dp-bg-card);
  color: var(--dp-text-primary);
  min-width: 180px;
}

.script-select-icon {
  position: absolute;
  right: 0.5rem;
  font-size: 0.75rem;
  color: var(--dp-text-muted);
  pointer-events: none;
}

.pipeline-live-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 9999px;
  background: rgba(0, 128, 255, 0.15);
  color: #0080ff;
}

.live-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #0080ff;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
</style>
