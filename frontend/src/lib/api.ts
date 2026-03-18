/**
 * API 封装 - 对接 Flask 后端
 * 开发环境用 VITE_API_BASE 直连后端，避免 localhost 被 AirPlay 拦截 403
 * @author fortune
 * @date 2026-03-18
 */

const BASE = (import.meta.env.VITE_API_BASE as string) || '/api'

export interface StatusResponse {
  provider: string
  model: string
  uptime_seconds: number
  gateway_port: number
  locale: string
  memory_backend: string
  paired: boolean
  channels: Record<string, boolean>
  health: {
    components: Record<string, { status: string; restart_count: number }>
  }
}

export async function getHealth(): Promise<{ status: string; message: string }> {
  const res = await fetch(`${BASE}/health`)
  if (!res.ok) throw new Error(`Health check failed: ${res.status}`)
  return res.json()
}

export async function getStatus(): Promise<StatusResponse> {
  const res = await fetch(`${BASE}/status`)
  if (!res.ok) throw new Error(`Status failed: ${res.status}`)
  return res.json()
}

// 对话 API
export interface ChatMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface ChatCompletionResponse {
  code: number
  msg: string
  data?: { content: string; role: string }
}

export async function chatCompletion(params: {
  messages: ChatMessage[]
  model?: string
}): Promise<ChatCompletionResponse['data']> {
  const res = await fetch(`${BASE}/chat/completion`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: params.messages,
      model: params.model,
    }),
  })
  const text = await res.text()
  if (!text) {
    throw new Error(`服务端返回空响应 (${res.status})，请确认后端已启动`)
  }
  let json: ChatCompletionResponse
  try {
    json = JSON.parse(text)
  } catch {
    throw new Error(`服务端返回非 JSON: ${text.slice(0, 100)}`)
  }
  if (json.code !== 1) {
    throw new Error(json.msg || '对话失败')
  }
  return json.data
}

/**
 * 流式对话，SSE 逐字推送
 * @param params 请求参数
 * @param onChunk 每收到一块内容时回调
 */
export async function chatCompletionStream(
  params: { messages: ChatMessage[]; model?: string; session_id?: string },
  onChunk: (content: string) => void
): Promise<string | undefined> {
  const BASE = (import.meta.env.VITE_API_BASE as string) || '/api'
  const res = await fetch(`${BASE}/chat/completion/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: params.messages,
      model: params.model,
      session_id: params.session_id,
    }),
  })
  if (!res.ok) {
    throw new Error(`请求失败: ${res.status}`)
  }
  const reader = res.body?.getReader()
  if (!reader) throw new Error('无法读取流')
  const decoder = new TextDecoder()
  let buffer = ''
  let lastSessionId: string | undefined
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        if (data.trim() === '[DONE]') return lastSessionId
        try {
          const obj = JSON.parse(data)
          // 后端结束标记，收到后立即返回，前端据此更新 loading 状态
          if (obj.done === true) {
            if (obj.session_id) lastSessionId = obj.session_id
            return lastSessionId
          }
          if (obj.content) {
            onChunk(obj.content)
          }
          if (obj.session_id) lastSessionId = obj.session_id
        } catch {
          // ignore
        }
      }
    }
  }
  return lastSessionId
}

// 会话与记忆 API
export interface ChatSession {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export async function listChatSessions(limit = 50): Promise<ChatSession[]> {
  const res = await fetch(`${BASE}/chat/sessions?limit=${limit}`)
  const json = await res.json()
  if (json.code !== 1) throw new Error(json.msg || '获取失败')
  return json.data?.sessions ?? []
}

export async function createChatSession(title = '新对话'): Promise<string> {
  const res = await fetch(`${BASE}/chat/sessions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  })
  const json = await res.json()
  if (json.code !== 1) throw new Error(json.msg || '创建失败')
  return json.data?.session_id ?? ''
}

export async function getChatSession(sessionId: string): Promise<{
  session: ChatSession
  messages: ChatMessage[]
}> {
  const res = await fetch(`${BASE}/chat/sessions/${sessionId}`)
  const json = await res.json()
  if (json.code !== 1) throw new Error(json.msg || '获取失败')
  return json.data
}

export async function deleteChatSession(sessionId: string): Promise<void> {
  const res = await fetch(`${BASE}/chat/sessions/${sessionId}`, { method: 'DELETE' })
  const json = await res.json()
  if (json.code !== 1) throw new Error(json.msg || '删除失败')
}
