# 影视流水线 - 会话沉淀 (agent.md)

> 主文档存放于 `project/` 文件夹
> 与 FortuneClaw/docs/agent.md 同步维护
> @author 举顾（technology@yiju.net）
> @date 2026-03-18

---

## 项目文档索引

| 文档 | 路径 |
| ---- | ---- |
| 项目设计 | `project/PROJECT_DESIGN.md` |
| 实施计划 | `project/IMPLEMENTATION_PLAN.md` |
| 会话沉淀 | `project/agent.md`（本文件） |

---

## 近期会话摘要

### 2026-03-18 17:xx（北京时间）- 会话 041

- **用户核心诉求**：影视 AI 工具岗位追问（流式性能、SSE vs WebSocket、Vue3 vs React、工作流编辑器）。
- **本次修改落地**：`doc/面试回答汇总文档.md` 追加第七十二～七十四节；`doc/面试知识点分类汇总.md` 补充流式优化、SSE/WS、Vue/React 差异、工作流数据结构。

---

### 2026-03-18 17:xx（北京时间）- 会话 040

- **用户核心诉求**：影视 AI 工具岗位面试模拟，补充第七十一节（自我介绍 / 技术栈 / 复杂交互 三题合一）。
- **本次修改落地**：
  - `doc/面试回答汇总文档.md`：追加第七十一节，含 AI 对话/可视化工作流/知识图谱项目经历、Vue3 vs React、中大型架构、状态管理选型、AI 对话设计（消息列表/流式/长对话优化）。
  - `doc/面试知识点分类汇总.md`：追加第十三节「影视 AI 工具岗位专项」。

---

### 2026-03-18 16:30（北京时间）- 会话 039

- **用户核心诉求**：将 FortuneClaw 转型为工业级短剧生成工具，非全自动流水线（每步用户确认后手动分发），目标用户为专业级/企业用户，Web 平台采用控制台风格，参考 zeroclaw 代码迁移。
- **本次修改落地**：
  - 新增 `project/PROJECT_DESIGN.md`：项目定位、10 个流水线角色、核心流程、控制台 UI 风格、技术架构、项目重命名建议。
  - 新增 `project/IMPLEMENTATION_PLAN.md`：7 阶段实施计划、zeroclaw 可复用清单、风险与依赖。
  - 新增 `project/agent.md`：会话沉淀主文档。
- **新发现与规则沉淀**：
  - 项目重命名需用户确认后再执行。
  - zeroclaw 使用 React + Tailwind，可复制 web 作为控制台基底。
  - 流水线需支持「暂停等待确认」节点，非自动流转。

---

### 2026-03-18 14:45（北京时间）- 会话 037

- **用户核心诉求**：任务拆解交由模型完成。
- **本次修改落地**：`apps/orchestrator-python/main.py` 接入 ChatTongyi 分析目标并分类任务类型；`build_plan` 接入模型生成执行计划。

---

### 2026-03-18 13:15（北京时间）- 会话 036

- **用户核心诉求**：将 FortuneClaw 后端从 MongoDB 迁移为 SQLite。
- **本次修改落地**：重写 db.go、mapper 层；tasks、dispatch_records、registry、worktrees 表；modernc.org/sqlite。

---

## 历史会话（简要）

- **会话 001-006**：Git 初始化、Vue+Go 技术栈、V0.1 任务链路、LangGraph 编排、中文规范。
- **会话 007-016**：imai-work 前端替换、侧边栏菜单、通义对话、Cursor/Trae/Antigravity 发送。
- **会话 017-032**：IDE 智能分配、分配记录、open-project、zeroclaw 集成、MongoDB 持久化。
- **会话 033-038**：面试回答汇总、Go/Python/Node 基础知识、模型拆解、SQLite 迁移。

---

## 完整历史

完整会话历史请查看：`FortuneClaw/docs/agent.md`
