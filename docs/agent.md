# DramaPipeline 会话沉淀 (docs/agent.md)

> @author fortune
> @date 2026-03-18

---

## 项目文档索引

| 文档 | 路径 |
| ---- | ---- |
| 项目设计 | `docs/项目设计.md` |
| 实施计划 | `docs/实施计划.md` |
| 设计稿 Prompt | `docs/设计稿Prompt.md` |
| Stitch 设计稿 Prompt | `docs/Stitch设计稿Prompt.md` |
| 前端需求与结构设计 | `docs/前端需求与结构设计.md` |
| 交互设计 | `docs/交互设计.md` |
| 会话沉淀 | `docs/agent.md`（本文件） |
| FortuneClaw 历史 | `docs/archive/FortuneClaw/` |

---

## 项目概览

- **技术栈**：前端 Vue 3 + Vite + Tailwind，后端 Flask Python
- **参考**：zeroclaw 控制台 UI 风格（深色主题、glass-card、侧边栏）
- **API Key**：根目录 `.env` 配置 `DASHSCOPE_API_KEY`、`DASHSCOPE_MODEL`
- **端口分配**：前端 5175，后端 5001（与 FortuneClaw 5174/8081 分离）

---

## 近期会话

### 2026-03-19 - 历史人物视频 Workflow（大模型可解析）

- **诉求**：让大模型理解何时调用该工作流，纯文本、换行分隔节点，不记录 md
- **产出**：`backend/app/prompts/historical_figure_video_workflow.txt`，含触发条件（一句话历史人物/主题生成视频）+ 5 节点（web_search、script_writing、storyboard_slice、text_to_image、image_to_video）

### 2026-03-19 - 文档整理与交互设计

- **文档重命名**：设计稿Prompt、Stitch设计稿Prompt、前端需求与结构设计、项目设计、实施计划，统一为语义化名称
- **FortuneClaw 归档**：`docs/archive/FortuneClaw/` 存放历史文档
- **交互设计**：新增 `docs/交互设计.md`，含导航流转、流水线/任务列表交互、状态反馈、动效规范、响应式
- **索引更新**：agent.md 文档索引指向新路径；README、项目设计、实施计划内链同步

### 2026-03-19 - 过渡动画

- **页面流转**：Layout 中 router-view 使用 Transition（page-fade），路由切换时淡入 + 轻微位移
- **预览面板**：左侧分析助手始终存在；点击「预览」时，右侧产物弹窗用 `Transition name="preview-drawer"` 从右滑入，左侧 `preview-left-panel` 通过 `has-preview` 类缩小（flex 过渡）
- **样式**：`index.css` 定义 `preview-drawer-enter/leave`；`pipeline-content-wrapper.has-preview` 控制 gap 与左侧 flex 收缩

### 2026-03-19 - 页面组件化与目录结构

- **目录结构**：各页面改为 `视图名/index.vue`（Chat、Config、Dashboard、Tasks、Pipelines）
- **Pipelines 组件化**：ScriptSelector、RoleSidebar、OutputPreview 抽至 `Pipelines/components/`
- **路由**：main.ts 指向 `views/xxx/index.vue`，删除原单文件 .vue

### 2026-03-19 - 流水线页面实现

- **Pipelines.vue**：按设计稿实现三块式布局——顶部剧本选择 + 左侧 10 角色流转 + 右侧角色会话与操作
- **Mock 数据**：3 个剧本、10 角色（前 2 已完成、第 3 进行中、其余待执行）、Agent 消息、片段卡片
- **组件**：剧本下拉、流水线运行中 badge、角色列表（状态徽章）、任务头、历史/预览、回退/重做、确认并分发
- **预览模式**：点击「预览」切换双框——左框（Agent 消息、片段、回退/重做）、右框（本次产物，按角色类型：文字/分镜1-N/图片1-N/视频）
- **视频生成**：视频生成助手时，右框展示「选择分镜图片（素材）」+「分镜文本（Prompt）」+ 生成视频按钮；选择分镜时自动填入 prompt

### 2026-03-19 - Stitch UI 设计稿 Prompt

- **产出**：`文档/DramaPipeline_Stitch_UI设计稿Prompt.md`，汇总 7 份文档的需求与设计，可直接复制到 Stitch 生成 UI 设计稿
- **内容**：需求摘要、完整 Prompt（导航、三块式流水线、状态、配色）、分页面 Prompt

### 2026-03-19 00:00+ - 前端需求分析与结构设计（按草图定稿）

- **需求**：多剧本并行、剧本/大纲输入、素材 zip/rar/图片、自定义角色、剧本切片→分镜、剧本量/拼接字数/匹配章节配置、用户剧本作为知识库
- **布局**：三块式草图在 **流水线页面** `/pipelines` 中——顶部剧本选择 + 左侧角色流转 + 右侧角色会话与处理进度
- **产出**：`文档/DramaPipeline_20260319000000_前端需求分析与结构设计.md`，含布局、样式、组件清单、实施优先级（前端先行 Mock）

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
