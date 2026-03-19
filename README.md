# DramaPipeline

> 影视流水线 - 工业级短剧生成工具
>
> 面向专业级用户和企业用户，采用流水线式、每步人工确认的控制台风格 Web 平台。

## 项目定位

- **非全自动**：每个流水线步骤需用户确认输出内容后，再手动分发到下一阶段
- **流水线式**：角色按顺序执行，用户主动触发下一步
- **控制台风格**：Web 平台采用控制台式 UI，偏专业、高效、可观测

## 文档索引

| 文档       | 说明           |
| ---------- | -------------- |
| docs/项目设计.md | 项目设计文档   |
| docs/实施计划.md | 实施计划       |
| agent.md   | 会话沉淀与开发记忆 |

## 技术栈

- **前端**：Vue 3 + Vite + Tailwind（参考 zeroclaw 控制台风格）
- **后端**：Flask Python
- **流水线**：10 个 Agent 角色（剧本分析、AI 导演、分镜设计、视频生成等）

## 本地启动

1. **环境变量**：复制 `.env.example` 为 `.env`，配置 `DASHSCOPE_API_KEY` 等
2. **后端**：`cd backend && python3 run.py`（默认端口 5001）
3. **前端**：`cd frontend && npm run dev`（默认端口 5173）
4. 访问 http://127.0.0.1:5175（macOS 上 localhost 可能被 AirPlay 占用导致 403，请用 127.0.0.1）

## 参考项目

- `references/zeroclaw`：zeroclaw 控制台 UI 参考（已克隆）

---

@author fortune  
@date 2026-03-18
