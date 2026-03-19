<!-- 流水线页面 - 三块式布局：剧本选择 + 角色流转 + 角色会话 -->
<!-- 参考设计稿：顶部 ACTIVE PROJECT、左侧 Pipeline Roles、右侧主内容区 -->
<!-- @author fortune -->
<!-- @date 2026-03-19 -->

<template>
  <div class="pipelines-page flex flex-col h-full min-h-0">
    <ScriptSelector
      v-model:script-id="currentScriptId"
      v-model:episode-id="currentEpisodeId"
      :scripts="mockScripts"
      :episodes="filteredEpisodes"
    />

    <div class="flex flex-1 min-h-0 overflow-hidden">
      <RoleSidebar
        :roles="roles"
        @select="selectRole"
      />

      <main class="pipeline-main flex-1 min-w-0 overflow-y-auto p-6">
        <div
          v-if="selectedRole"
          class="pipeline-content-wrapper"
          :class="{ 'has-preview': showPreview }"
        >
          <!-- 左侧分析助手：始终存在，预览时缩小 -->
          <div class="preview-left-panel">
            <div class="task-header">
              <div class="task-title-row">
                <span class="task-icon">💬</span>
                <div>
                  <h2 class="task-title">{{ selectedRole.name }}</h2>
                  <p class="task-subtitle">
                    {{ selectedRole.status === 'active' ? '正在处理...' : selectedRole.status === 'done' ? '已完成' : '等待处理' }}
                  </p>
                </div>
              </div>
              <div class="task-actions">
                <button type="button" class="btn-outline">🕐 历史</button>
                <button
                  type="button"
                  class="btn-outline"
                  @click="showPreview = true"
                >
                  👁 预览
                </button>
                <button
                  v-if="showPreview"
                  type="button"
                  class="btn-outline btn-sm"
                  @click="showPreview = false"
                >
                  关闭预览
                </button>
              </div>
            </div>
            <div class="agent-message">
              <span class="agent-avatar">🤖</span>
              <div class="agent-bubble">
                <p class="agent-text">{{ mockAgentMessage }}</p>
                <span class="agent-time">{{ selectedRole.name }} · 2 分钟前</span>
              </div>
            </div>
            <div class="snippet-card">
              <div class="snippet-header">
                <span class="snippet-title">第 12 场片段</span>
                <button type="button" class="snippet-menu">⋮</button>
              </div>
              <pre class="snippet-body">{{ mockSnippet }}</pre>
              <div class="snippet-badge">
                <span class="badge-i">i</span>
                语气匹配：94% 一致性达成
              </div>
            </div>
            <div class="footer-actions">
              <div class="footer-left">
                <button type="button" class="btn-outline btn-rollback">↺ 回退</button>
                <button type="button" class="btn-outline btn-redo">↻ 重做</button>
              </div>
              <button
                type="button"
                class="btn-confirm"
                @click="showPreview = false"
              >
                ✓ 确认并分发
              </button>
            </div>
          </div>

          <!-- 右侧产物：仅预览时从右滑入 -->
          <Transition name="preview-drawer">
            <div
              v-if="showPreview"
              class="preview-right-panel"
            >
              <OutputPreview
                :output-type="outputType"
                :text="mockAgentMessage"
                :storyboards="mockStoryboards"
                :images="mockImages"
                :is-video-gen-role="isVideoGenRole"
                v-model:selected-storyboard="videoSelectedStoryboard"
                v-model:prompt-text="videoPromptText"
                :generated-video-url="generatedVideoUrl"
                @generate-video="generateVideo"
              />
            </div>
          </Transition>
        </div>
        <div
          v-else
          class="pipeline-content-card flex items-center justify-center text-[var(--dp-text-muted)]"
        >
          请从左侧选择角色
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import ScriptSelector from './components/ScriptSelector.vue'
import RoleSidebar from './components/RoleSidebar.vue'
import OutputPreview from './components/OutputPreview.vue'

const mockScripts = ref([
  { id: '1', title: '沉默的证人' },
  { id: '2', title: '都市追凶' },
  { id: '3', title: '新剧本（未命名）' },
])

const mockEpisodes = ref([
  { id: 'e1-1', scriptId: '1', title: '第 01 集' },
  { id: 'e1-2', scriptId: '1', title: '第 02 集' },
  { id: 'e1-3', scriptId: '1', title: '第 03 集' },
  { id: 'e1-4', scriptId: '1', title: '第 04 集' },
  { id: 'e2-1', scriptId: '2', title: '第 01 集' },
  { id: 'e2-2', scriptId: '2', title: '第 02 集' },
  { id: 'e3-1', scriptId: '3', title: '第 01 集' },
])

const currentScriptId = ref('1')
const currentEpisodeId = ref('e1-4')

const filteredEpisodes = computed(() =>
  mockEpisodes.value.filter((ep) => ep.scriptId === currentScriptId.value)
)

function onScriptChange() {
  const eps = filteredEpisodes.value
  if (eps.length > 0 && !eps.some((ep) => ep.id === currentEpisodeId.value)) {
    currentEpisodeId.value = eps[0].id
  }
}

const roles = ref([
  { id: '1', name: '剧本分析机器人', status: 'done' as const },
  { id: '2', name: 'AI 导演团队', status: 'done' as const },
  { id: '3', name: '素材分析助手', status: 'active' as const },
  { id: '4', name: '分镜设计助手', status: 'pending' as const },
  { id: '5', name: '首帧生成助手', status: 'pending' as const },
  { id: '6', name: '视频生成助手', status: 'pending' as const },
  { id: '7', name: '后期合成助手', status: 'pending' as const },
  { id: '8', name: '角色创建大师', status: 'pending' as const },
  { id: '9', name: '场景生成大师', status: 'pending' as const },
  { id: '10', name: '审片助手', status: 'pending' as const },
])

const selectedRole = ref<typeof roles.value[0] | null>(roles.value[2])
const showPreview = ref(false)

const ROLE_OUTPUT_TYPE: Record<string, 'text' | 'storyboard' | 'image' | 'video'> = {
  '1': 'text', '2': 'text', '3': 'image', '4': 'storyboard', '5': 'image',
  '6': 'video', '7': 'video', '8': 'image', '9': 'image', '10': 'video',
}

const outputType = computed(() =>
  selectedRole.value ? ROLE_OUTPUT_TYPE[selectedRole.value.id] ?? 'text' : 'text'
)

const isVideoGenRole = computed(() => selectedRole.value?.id === '6')

const mockStoryboards = ref([
  { id: 'sb1', desc: '室内，中景，MILLER 与 ELENA 对话' },
  { id: 'sb2', desc: '特写，ELENA 表情' },
  { id: 'sb3', desc: '全景，两人走向门口' },
])

const mockImages = ref([{ id: 'img1' }, { id: 'img2' }, { id: 'img3' }])

const videoSelectedStoryboard = ref('sb1')
const videoPromptText = ref('室内对话场景，中景切换特写，突出角色情绪')
const generatedVideoUrl = ref<string | null>(null)

function generateVideo() {
  generatedVideoUrl.value = 'mock-video-url'
}

watch(currentScriptId, onScriptChange)

watch(videoSelectedStoryboard, (id) => {
  const sb = mockStoryboards.value.find((s) => s.id === id)
  if (sb) videoPromptText.value = sb.desc
}, { immediate: true })

const mockAgentMessage =
  '已完成素材包解析，共识别 12 张参考图、3 段视频片段。已打标：室内场景、人物特写、夜景。建议后续分镜阶段使用。'
const mockSnippet = `MILLER
（压低声音）你确定要这么做？

ELENA
（坚定）没有别的选择。

MILLER
（叹气）好吧，我会配合你。`

function selectRole(role: typeof roles.value[0]) {
  selectedRole.value = role
}
</script>

<style scoped>
.pipelines-page {
  height: calc(100vh - 140px);
  min-height: 400px;
}

.pipeline-content-card {
  background: var(--dp-bg-card);
  border: 1px solid var(--dp-border-subtle);
  border-radius: 0.75rem;
  padding: 1.5rem;
  min-height: 400px;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.task-title-row {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
}

.task-icon {
  font-size: 1.5rem;
}

.task-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--dp-text-primary);
  margin: 0 0 0.25rem 0;
}

.task-subtitle {
  font-size: 0.75rem;
  color: var(--dp-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
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
}

.btn-outline:hover {
  border-color: #0080ff;
  color: #0080ff;
}

.agent-message {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.agent-avatar {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.agent-bubble {
  flex: 1;
  padding: 1rem 1.25rem;
  background: var(--dp-bg-secondary);
  border-radius: 0.75rem;
  border: 1px solid var(--dp-border-subtle);
}

.agent-text {
  font-size: 0.875rem;
  line-height: 1.6;
  color: var(--dp-text-primary);
  margin: 0 0 0.5rem 0;
}

.agent-time {
  font-size: 0.75rem;
  color: var(--dp-text-muted);
}

.snippet-card {
  padding: 1rem 1.25rem;
  font-size: 0.75rem;
  background: var(--dp-bg-secondary);
  border: 1px solid var(--dp-border-subtle);
  border-radius: 0.5rem;
  margin-bottom: 1.5rem;
}

.snippet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.snippet-title {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--dp-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.snippet-menu {
  padding: 0.25rem;
  font-size: 1rem;
  background: none;
  border: none;
  color: var(--dp-text-muted);
  cursor: pointer;
}

.snippet-body {
  font-family: ui-monospace, monospace;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: var(--dp-text-primary);
  margin: 0 0 0.75rem 0;
  white-space: pre-wrap;
  word-break: break-word;
}

.snippet-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.6875rem;
  color: var(--dp-text-muted);
}

.badge-i {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--dp-text-muted);
  color: var(--dp-bg-primary);
  font-family: sans-serif;
  font-weight: 700;
}

.footer-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--dp-border-subtle);
}

.footer-left {
  display: flex;
  gap: 0.5rem;
}

.btn-rollback:hover {
  border-color: #f59e0b;
  color: #f59e0b;
}

.btn-redo:hover {
  border-color: #0080ff;
  color: #0080ff;
}

.btn-confirm {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1.25rem;
  font-size: 0.875rem;
  font-weight: 500;
  border: none;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #0080ff, #0066cc);
  color: white;
  cursor: pointer;
}

.btn-confirm:hover {
  background: linear-gradient(135deg, #0090ff, #0070dd);
  box-shadow: 0 0 20px rgba(0, 128, 255, 0.3);
}

.pipeline-content-wrapper {
  display: flex;
  gap: 0;
  min-height: 0;
  overflow: hidden;
  transition: gap 0.3s cubic-bezier(0.32, 0.72, 0, 1);
}

.pipeline-content-wrapper.has-preview {
  gap: 1rem;
}

.preview-left-panel {
  flex: 1 1 100%;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: var(--dp-bg-card);
  border: 1px solid var(--dp-border-subtle);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: flex 0.35s cubic-bezier(0.32, 0.72, 0, 1);
}

.pipeline-content-wrapper.has-preview .preview-left-panel {
  flex: 1 1 0;
}

.preview-right-panel {
  flex: 1 1 0;
  min-width: 280px;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--dp-border-subtle);
  border-radius: 0.75rem;
  background: var(--dp-bg-card);
  padding: 1rem;
  overflow-y: auto;
}

.btn-sm {
  padding: 0.2rem 0.5rem;
  font-size: 0.6875rem;
}
</style>
