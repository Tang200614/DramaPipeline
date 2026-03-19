<!-- 右侧产物展示 - 按角色类型展示文字/分镜/图片/视频 -->
<!-- @author fortune -->
<!-- @date 2026-03-19 -->

<template>
  <div class="output-preview">
    <div class="preview-panel-header">
      <span>本次产物</span>
    </div>
    <div v-if="outputType === 'text'" class="output-text">
      <p>{{ text }}</p>
    </div>
    <div v-else-if="outputType === 'storyboard'" class="output-storyboard">
      <div v-for="(sb, i) in storyboards" :key="sb.id" class="storyboard-item">
        <span class="storyboard-label">分镜{{ i + 1 }}</span>
        <p class="storyboard-desc">{{ sb.desc }}</p>
      </div>
    </div>
    <div v-else-if="outputType === 'image'" class="output-images">
      <div v-for="(img, i) in images" :key="img.id" class="image-item">
        <div class="image-placeholder">图片{{ i + 1 }}</div>
      </div>
    </div>
    <div v-else-if="outputType === 'video'" class="output-video">
      <div v-if="isVideoGenRole" class="video-gen-config">
        <div class="config-section">
          <span class="config-label">选择分镜图片（素材）</span>
          <div class="storyboard-picker">
            <label
              v-for="(sb, i) in storyboards"
              :key="sb.id"
              class="picker-item"
              :class="{ selected: selectedStoryboard === sb.id }"
            >
              <input
                :model-value="selectedStoryboard"
                type="radio"
                :value="sb.id"
                @change="$emit('update:selectedStoryboard', sb.id)"
              />
              <span>分镜{{ i + 1 }}</span>
            </label>
          </div>
        </div>
        <div class="config-section">
          <span class="config-label">分镜文本（Prompt）</span>
          <textarea
            :model-value="promptText"
            class="prompt-textarea"
            placeholder="使用选中分镜的文本作为生成视频的 prompt"
            rows="3"
            @input="$emit('update:promptText', ($event.target as HTMLTextAreaElement).value)"
          />
        </div>
        <button type="button" class="btn-outline" @click="$emit('generateVideo')">
          生成视频
        </button>
      </div>
      <div v-if="generatedVideoUrl" class="video-player">
        <div class="video-placeholder">
          <span>▶</span>
          <span>当前分镜生成的视频</span>
        </div>
      </div>
      <div v-else-if="!isVideoGenRole" class="video-player">
        <div class="video-placeholder">
          <span>▶</span>
          <span>成片预览</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  outputType: 'text' | 'storyboard' | 'image' | 'video'
  text?: string
  storyboards?: { id: string; desc: string }[]
  images?: { id: string }[]
  isVideoGenRole?: boolean
  selectedStoryboard?: string
  promptText?: string
  generatedVideoUrl?: string | null
}>()
defineEmits<{
  'update:selectedStoryboard': [id: string]
  'update:promptText': [value: string]
  generateVideo: []
}>()
</script>

<style scoped>
.output-text {
  padding: 1rem;
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--dp-text-primary);
}

.output-storyboard {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.storyboard-item {
  padding: 0.75rem 1rem;
  background: var(--dp-bg-secondary);
  border: 1px solid var(--dp-border-subtle);
  border-radius: 0.5rem;
}

.storyboard-label {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--dp-text-primary);
  display: block;
  margin-bottom: 0.25rem;
}

.storyboard-desc {
  font-size: 0.8125rem;
  color: var(--dp-text-secondary);
  margin: 0;
}

.output-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
}

.image-item {
  aspect-ratio: 16/9;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--dp-bg-secondary);
  border: 1px dashed var(--dp-border);
  border-radius: 0.5rem;
  font-size: 0.75rem;
  color: var(--dp-text-muted);
}

.output-video {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.video-gen-config {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.config-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.config-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--dp-text-muted);
}

.storyboard-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.picker-item {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.8125rem;
  border: 1px solid var(--dp-border);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.picker-item:hover,
.picker-item.selected {
  border-color: #0080ff;
  background: rgba(0, 128, 255, 0.08);
  color: #0080ff;
}

.picker-item input {
  display: none;
}

.prompt-textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.8125rem;
  font-family: inherit;
  border: 1px solid var(--dp-border);
  border-radius: 0.5rem;
  background: var(--dp-bg-secondary);
  color: var(--dp-text-primary);
  resize: vertical;
}

.video-player {
  flex: 1;
  min-height: 200px;
}

.video-placeholder {
  width: 100%;
  height: 100%;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: var(--dp-bg-secondary);
  border: 1px dashed var(--dp-border);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: var(--dp-text-muted);
}

.video-placeholder span:first-child {
  font-size: 2rem;
}

.preview-panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--dp-text-primary);
}

.btn-outline {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  border: 1px solid var(--dp-border);
  border-radius: 0.5rem;
  background: transparent;
  color: var(--dp-text-secondary);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: #0080ff;
  color: #0080ff;
}
</style>
