# DramaPipeline 会话沉淀 (docs/agent.md)

> @author 举顾（technology@yiju.net）
> @date 2026-03-18

---

## 项目文档索引

| 文档 | 路径 |
| ---- | ---- |
| 项目设计 | `project/PROJECT_DESIGN.md` |
| 实施计划 | `project/IMPLEMENTATION_PLAN.md` |
| 设计稿 Prompt | `文档/DramaPipeline_20260318180000_设计稿Prompt.md` |
| 会话沉淀 | `docs/agent.md`（本文件） |

---

## 项目概览

- **技术栈**：前端 Vue 3 + Vite + Tailwind，后端 Flask Python
- **参考**：zeroclaw 控制台 UI 风格（深色主题、glass-card、侧边栏）
- **API Key**：根目录 `.env` 配置 `DASHSCOPE_API_KEY`、`DASHSCOPE_MODEL`
- **端口分配**：前端 5175，后端 5001（与 FortuneClaw 5174/8081 分离）

---

## 近期会话

### 2026-03-18 23:30+ - 流式结束标记

- **后端**：LangGraph 与 compatible API 两种流式路径均在结束时发送 `{"done": true, "session_id": "xxx"}` 作为结束标记
- **前端**：`api.ts` 解析到 `obj.done === true` 时立即 return，`Chat.vue` 的 `finally` 将 loading 置为 false

### 2026-03-18 23:15+ - 流式对话与前端渲染

- **流式输出修复**：qwen3.5 系列走 compatible-mode；`enable_thinking: False` 禁用思考；`reasoning_content` 时发 keepalive
- **前端逐字显示**：`streamingContent` ref 替代直接改 `assistantMsg.content`，保证 Vue 响应式更新
- **端口分离**：DramaPipeline 5175/5001，FortuneClaw 5174/8081

### 2026-03-18 22:55 - LangGraph 封装

- 依赖：langchain、langchain-community、langgraph、dashscope
- `app/prompts/`：`{{variable}}` 模板；`app/graph/`：model_adapter、chat_graph
- qwen3.5 系列自动走 compatible API（ChatTongyi URL 不支持）

### 2026-03-18 22:50 - SQLite 会话与记忆

- `app/db.py`、`app/chat_store.py`，表 chat_sessions、chat_messages
- API：GET/POST /api/chat/sessions、GET/DELETE/PATCH /api/chat/sessions/<id>
- 前端：左侧会话列表、历史消息作为上下文

### 2026-03-18 22:35 - 对话与 SSE

- `POST /api/chat/completion`、`POST /api/chat/completion/stream`（SSE）
- 前端 Chat.vue、chatCompletionStream（fetch + ReadableStream）

### 2026-03-18 22:20 - 主题切换

- `composables/useTheme.ts`，CSS 变量 `--dp-*`，暗色/亮色切换

### 2026-03-18 21:55 - 会话 045

- zeroclaw 参考改造；Flask 后端（5001）、Vue 3 前端；zeroclaw 风格；.env 配置

### 2026-03-18 18:xx - 会话 044

- 推送 GitHub；remote 切换 SSH；`git push -u origin main` 成功

### 2026-03-18 18:00 - 会话 043

- 新增 `文档/DramaPipeline_20260318180000_设计稿Prompt.md`，含通用/分页/组件 Prompt

### 2026-03-18 17:xx - 会话 04x

- 042：README、.gitignore、git init、首次提交
- 041：面试文档（流式、SSE、Vue3、工作流）
- 040：面试模拟第七十一节

### 2026-03-18 16:30 - 会话 039

- **FortuneClaw 转型**：project/PROJECT_DESIGN.md、IMPLEMENTATION_PLAN.md；10 角色流水线；控制台 UI；zeroclaw 可复用清单

### 2026-03-18 14:45 - 会话 037

- orchestrator-python 接入 ChatTongyi 分析目标、build_plan 生成执行计划

### 2026-03-18 13:15 - 会话 036

- FortuneClaw 后端 MongoDB → SQLite；db.go、mapper 重写
