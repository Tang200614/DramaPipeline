# 影视流水线 - 实施计划

> 基于 FortuneClaw 与 zeroclaw 的迁移与改造计划
>
> @author fortune
> @date 2026-03-18

---

## 一、总体策略

1. **先文档、后代码**：设计文档与实施计划确认后再动代码
2. **zeroclaw 复用**：复制 `references/zeroclaw/web` 作为前端控制台基础，在其上改造
3. **FortuneClaw 保留**：Go 后端、Python 编排、任务模型继续沿用，按流水线业务扩展
4. **渐进式迁移**：分阶段推进，每阶段可独立验证

---

## 二、阶段划分

### 阶段 0：准备与确认（当前）

- [x] 编写 `project/PROJECT_DESIGN.md`
- [x] 编写 `project/IMPLEMENTATION_PLAN.md`
- [x] 编写 `project/agent.md`
- [ ] 用户确认项目名称（DramaPipeline / ShortDramaStudio / ClipForge）
- [ ] 用户确认设计文档与实施计划

---

### 阶段 1：项目重命名与目录调整

**目标**：将 FortuneClaw 重命名为 DramaPipeline（或用户选定名称）

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 1.1 | 重命名根目录 | `FortuneClaw` → `DramaPipeline` |
| 1.2 | 更新 package.json / pyproject.toml 等 | name、description |
| 1.3 | 更新 README.md | 项目名、定位、启动说明 |
| 1.4 | 更新 project/agent.md、OpenAPI 等 | 引用路径 |
| 1.5 | 更新 .cursor/skills、.gitignore | 如有硬编码路径 |
| 1.6 | Git 提交 | `chore: 项目重命名为 DramaPipeline` |

**注意**：若 Git 历史需保留，可仅改内容不改目录名；若改目录名，需同步更新远程仓库路径。

---

### 阶段 2：复制 zeroclaw Web 并改造为流水线控制台

**目标**：以 zeroclaw 控制台为基底，构建流水线专用前端

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 2.1 | 复制 `references/zeroclaw/web` → `frontend-console/` | 新建控制台前端目录，与现有 `frontend/` 并存 |
| 2.2 | 依赖安装与构建验证 | `npm install && npm run build` 确保可跑 |
| 2.3 | 替换 Sidebar 导航项 | Dashboard、流水线、任务、通知、配置 |
| 2.4 | 替换 Layout / Header | 品牌名改为 DramaPipeline，移除 zeroclaw 特有逻辑 |
| 2.5 | 移除 zeroclaw 业务页面 | AgentChat、Tools、Cron、Integrations、Memory、Cost、Logs、Doctor 等 |
| 2.6 | 新增流水线相关页面 | 工作台、任务列表、任务详情（含步骤确认与分发） |
| 2.7 | 对接 FortuneClaw Go API | 替换 `@/lib/api` 的 baseURL 与接口 |
| 2.8 | 移除 zeroclaw 认证逻辑 | Pairing、Auth 等，改为对接自身登录或简化 |

**技术栈**：zeroclaw 使用 React + Vite + Tailwind，可保留；若团队偏好 Vue，可后续用 Vue 重写控制台，但先以 React 快速落地。

---

### 阶段 3：后端 API 扩展（流水线模型）

**目标**：Go 后端支持流水线任务、步骤、确认、分发

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 3.1 | 定义流水线模型 | Project、Pipeline、Step、StepOutput、UserConfirm |
| 3.2 | 数据库迁移 | 新增 project、pipeline_task、pipeline_step 等表 |
| 3.3 | 新增 API | `POST /api/projects`、`GET /api/projects`、`POST /api/pipelines`、`GET /api/pipelines/{id}` |
| 3.4 | 步骤确认 API | `POST /api/pipelines/{id}/steps/{stepId}/confirm` |
| 3.5 | 手动分发 API | `POST /api/pipelines/{id}/steps/{stepId}/dispatch` |
| 3.6 | 更新 OpenAPI | 同步 Apifox |

---

### 阶段 4：Python 编排服务适配流水线

**目标**：LangGraph 编排图按流水线角色拆解，每步可暂停等待用户确认

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 4.1 | 定义流水线状态图 | 节点对应 10 个角色，边为「用户确认后」流转 |
| 4.2 | 支持「暂停等待确认」节点 | 节点执行完后进入 WAITING_CONFIRM，不自动进入下一节点 |
| 4.3 | 分发接口 | 接收 dispatch 请求后，从 WAITING_CONFIRM 进入下一节点 |
| 4.4 | 与 Go 后端联调 | Go 调用 Python 编排，Python 回调 Go 更新步骤状态 |

---

### 阶段 5：用户确认与手动分发 UI

**目标**：前端完整支持「查看输出 → 确认 → 分发」流程

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 5.1 | 任务详情页 | 展示当前步骤、输出预览（文本/图片/视频） |
| 5.2 | 确认按钮 | 用户确认当前步骤输出 |
| 5.3 | 分发按钮 | 分发到下一阶段，触发 API |
| 5.4 | 步骤状态展示 | 待执行、执行中、待确认、完成、失败 |
| 5.5 | 回退 / 重做 | 可选：支持某一步重新生成 |

---

### 阶段 6：并发与生成完成提醒

**目标**：高并发、任务完成通知

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 6.1 | 任务队列 | 后端任务队列限流、并发控制 |
| 6.2 | 任务完成通知 | WebSocket / SSE 推送，或轮询 + 站内提醒 |
| 6.3 | 前端通知中心 | 展示「生成完成」等消息 |
| 6.4 | 可选：邮件 / 钉钉 / 企业微信 | 企业用户提醒 |

---

### 阶段 7：收尾与文档

| 步骤 | 操作 | 说明 |
| ---- | ---- | ---- |
| 7.1 | 统一启动脚本 | 前端、后端、Python 编排一键启动 |
| 7.2 | README 更新 | 新架构、新接口、新启动方式 |
| 7.3 | project/agent.md 更新 | 记录各阶段结论与规则 |

---

## 三、zeroclaw 可复用清单

| 模块 | 路径 | 复用方式 |
| ---- | ---- | -------- |
| Layout | `web/src/components/layout/Layout.tsx` | 直接复用，改品牌名 |
| Sidebar | `web/src/components/layout/Sidebar.tsx` | 改导航项 |
| Header | `web/src/components/layout/Header.tsx` | 改品牌名、移除 zeroclaw 特有 |
| 主题 / 样式 | `web/src/index.css` | 控制台深色主题、glass-card 等 |
| 路由结构 | `App.tsx` | 替换为流水线相关路由 |
| API 封装 | `web/src/lib/api.ts` | 改 baseURL、接口路径 |
| i18n | `web/src/lib/i18n.ts` | 可保留多语言框架 |

**不复用**：zeroclaw 的 Rust 后端、Pairing 认证、Telegram/WhatsApp 等集成、AgentChat/Tools/Cron 等业务页面逻辑。

---

## 四、风险与依赖

| 风险 | 缓解 |
| ---- | ---- |
| zeroclaw 与 FortuneClaw 技术栈不一致 | 前端可独立为 React 控制台，与 Vue 的 imai-work 风格并存，或后续统一 |
| 流水线角色尚未接入真实 AI 服务 | 先做 Mock，保证流程跑通，再接入真实模型 |
| 并发与通知实现复杂 | 阶段 6 可拆为多期，先做轮询 + 站内提醒 |

---

## 五、下一步行动

1. **用户确认**：项目名称、设计文档、实施计划
2. **执行阶段 1**：项目重命名
3. **执行阶段 2**：复制 zeroclaw web 并改造控制台
