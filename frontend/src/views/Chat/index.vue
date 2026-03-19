<!-- AI 对话页面 - 流式输出、会话存储、记忆 -->
<!-- @author fortune -->
<!-- @date 2026-03-18 -->

<template>
  <div class="chat-page flex h-full">
    <!-- 左侧会话列表 -->
    <aside
      class="w-56 flex-shrink-0 flex flex-col border-r transition-colors"
      :class="theme === 'dark' ? 'border-[#1a1a3e]' : 'border-[#e2e8f0]'"
    >
      <div class="p-3 border-b" :class="theme === 'dark' ? 'border-[#1a1a3e]' : 'border-[#e2e8f0]'">
        <button
          type="button"
          class="btn-electric w-full py-2 text-sm"
          @click="handleNewChat"
        >
          + 新对话
        </button>
      </div>
      <div class="flex-1 overflow-y-auto py-2">
        <button
          v-for="s in sessions"
          :key="s.id"
          type="button"
          class="w-full px-3 py-2.5 text-left text-sm truncate transition-colors"
          :class="
            currentSessionId === s.id
              ? 'bg-[#0080ff15] text-[#0080ff]'
              : 'text-[var(--dp-text-muted)] hover:bg-[#0080ff08] hover:text-[var(--dp-text-primary)]'
          "
          @click="selectSession(s.id)"
        >
          {{ s.title || '新对话' }}
        </button>
        <p v-if="sessions.length === 0" class="px-3 py-4 text-xs text-[var(--dp-text-muted)]">
          暂无历史记录
        </p>
      </div>
    </aside>
    <!-- 右侧对话区 -->
    <div class="flex-1 flex flex-col min-w-0">
      <div
        ref="messageListRef"
        class="chat-messages flex-1 min-h-0 overflow-y-auto p-6 space-y-4"
      >
        <div
          v-for="(msg, index) in messages"
          :key="index"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[80%] rounded-xl px-4 py-3"
            :class="
              msg.role === 'user'
                ? 'bg-[#0080ff] text-white'
                : 'glass-card text-[var(--dp-text-primary)]'
            "
          >
            <div class="text-xs font-medium mb-1.5 opacity-80">
              {{ msg.role === 'user' ? '我' : 'AI' }}
            </div>
            <div class="whitespace-pre-wrap break-words text-sm">
              {{ loading && index === messages.length - 1 ? streamingContent : msg.content }}
              <span
                v-if="loading && index === messages.length - 1"
                class="inline-block w-2 h-4 ml-0.5 bg-[#0080ff] animate-pulse"
              />
            </div>
          </div>
        </div>
      </div>
      <div
        class="chat-input flex-shrink-0 p-4 border-t transition-colors"
        :class="theme === 'dark' ? 'border-[#1a1a3e]' : 'border-[#e2e8f0]'"
      >
        <div class="flex gap-3">
          <textarea
            v-model="inputText"
            class="flex-1 rounded-xl px-4 py-3 text-sm resize-none border transition-colors min-h-[80px] focus:outline-none focus:ring-2 focus:ring-[#0080ff]/50"
            :class="
              theme === 'dark'
                ? 'bg-[#0a0a18] border-[#1a1a3e] text-white placeholder-[#556080]'
                : 'bg-white border-[#e2e8f0] text-[#1e293b] placeholder-[#94a3b8]'
            "
            placeholder="输入消息，按 Enter 发送（Shift+Enter 换行）"
            :disabled="loading"
            @keydown.enter.exact.prevent="handleSend"
          />
          <button
            type="button"
            class="btn-electric px-6 py-3 self-end disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!inputText.trim() || loading"
            @click="handleSend"
          >
            {{ loading ? '发送中...' : '发送' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, watch, onMounted } from 'vue'
import {
  chatCompletionStream,
  listChatSessions,
  getChatSession,
  createChatSession,
  type ChatMessage,
} from '@/lib/api'
import { useTheme } from '@/composables/useTheme'

const { theme } = useTheme()
const messages = ref<ChatMessage[]>([])
const sessions = ref<{ id: string; title: string; created_at: string; updated_at: string }[]>([])
const currentSessionId = ref<string | null>(null)
const inputText = ref('')
const loading = ref(false)
const streamingContent = ref('')
const messageListRef = ref<HTMLElement>()

const scrollToBottom = () => {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

watch(() => messages.value.length, scrollToBottom)
watch(
  () => messages.value.map((m) => m.content).join('') + streamingContent.value,
  scrollToBottom
)

async function loadSessions() {
  try {
    sessions.value = await listChatSessions()
  } catch {
    sessions.value = []
  }
}

async function selectSession(sessionId: string) {
  currentSessionId.value = sessionId
  try {
    const { messages: msgs } = await getChatSession(sessionId)
    messages.value = msgs
  } catch {
    messages.value = []
  }
  scrollToBottom()
}

function handleNewChat() {
  currentSessionId.value = null
  messages.value = []
}

async function handleSend() {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  const userMsg: ChatMessage = { role: 'user', content: text }
  messages.value.push(userMsg)
  inputText.value = ''
  scrollToBottom()

  loading.value = true
  streamingContent.value = ''
  const assistantMsg: ChatMessage = { role: 'assistant', content: '' }
  messages.value.push(assistantMsg)
  scrollToBottom()

  try {
    const history: ChatMessage[] = [
      {
        role: 'system',
        content:
          '你是通义千问，一个有帮助的 AI 助手。请用简洁、友好的方式回答用户问题。结合当前对话历史（记忆）理解用户意图。',
      },
      ...messages.value.slice(0, -1),
    ]
    const newSessionId = await chatCompletionStream(
      {
        messages: history,
        model: 'qwen3.5-plus',
        session_id: currentSessionId.value ?? undefined,
      },
      (chunk) => {
        streamingContent.value += chunk
      }
    )
    if (newSessionId) {
      currentSessionId.value = newSessionId
      await loadSessions()
    }
    assistantMsg.content = streamingContent.value || '抱歉，未能获取回复。'
    messages.value[messages.value.length - 1] = { ...assistantMsg }
  } catch (e) {
    assistantMsg.content = `请求失败：${e instanceof Error ? e.message : '未知错误'}`
    messages.value[messages.value.length - 1] = { ...assistantMsg }
  } finally {
    loading.value = false
    scrollToBottom()
  }
}

onMounted(() => {
  loadSessions()
})
</script>

<style scoped>
.chat-page {
  height: calc(100vh - 140px);
  min-height: 400px;
}
.chat-messages {
  min-height: 0;
}
</style>
