## Context

当前项目是一个英语发音练习和评分系统，包含 Vue.js 3 前端 + FastAPI 后端 + 本地 Whisper 语音识别。现有架构为单前端 SPA，同时服务于管理和用户练习场景。现需拆分为：
1. **Admin 管理后台**（Vue.js Web）— 管理员使用，管理用户和题目
2. **微信小程序**（原生开发）— 最终用户使用，微信授权登录后练习发音

后端保持为单一 FastAPI 服务，通过路由前缀区分不同客户端的 API。

## Goals / Non-Goals

**Goals:**
- 将现有 `frontend/` 改造为 Admin 管理后台，保留 Vue.js 技术栈
- 创建微信小程序项目，支持微信登录、浏览题库、录音上传、评分展示
- 统一后端 API，用路由前缀 `/api/admin/` 和 `/api/wx/` 区分权限域
- 复用现有 Whisper 识别和评分引擎，无需修改核心算法
- 用户模型支持 admin/user 角色和微信 openid

**Non-Goals:**
- 不做微信支付功能
- 不做小程序端的社交分享/排行榜
- 不做多语言支持（仅英语发音练习）
- 不引入新的 ORM 或后端框架
- 不做小程序端的离线功能

## Decisions

### 1. 项目结构：三项目并列

```
say-hi/
├── admin/          # Vue.js Admin 后台（从 frontend/ 改造）
├── miniprogram/    # 微信小程序（原生开发）
├── backend/        # FastAPI 后端（扩展 API）
└── openspec/
```

**选择理由**: `frontend/` 重命名为 `admin/` 并改造，微信小程序单独目录。三个项目共享一个仓库，方便联调。
**备选方案**: 多仓库 — 增加维护成本，联调不便。

### 2. Admin 后台：改造现有 frontend/

将现有 `frontend/` 重命名为 `admin/`，移除用户侧页面（Login/Register/PracticeList/PracticeDetail/HistoryList），新增：
- 管理员登录页（复用现有邮箱+密码登录）
- 用户列表页（查看用户、禁用/启用）
- 题目管理页（CRUD：列表、创建、编辑、删除）
- 评估历史总览（查看所有用户的评估记录）

**技术栈**: 继续使用 Vue.js 3 + Vite + TypeScript + Vue Router

### 3. 微信小程序：原生开发

```
miniprogram/
├── app.js / app.json / app.wxss
├── pages/
│   ├── index/          # 首页：题目分类浏览
│   ├── practice/       # 练习页：录音 + 提交
│   ├── result/         # 结果页：评分 + 单词对比
│   ├── history/        # 历史记录
│   └── profile/        # 个人中心
├── components/
│   ├── score-card/     # 评分卡片组件
│   └── word-compare/   # 单词对比组件
├── utils/
│   ├── api.js          # API 请求封装
│   ├── auth.js         # 登录 + token 管理
│   └── recorder.js     # 录音管理封装
└── project.config.json
```

**选择理由**: 原生开发性能最优，小程序功能相对简单，无需跨平台框架的额外复杂度。
**备选方案**: uni-app / Taro — 引入额外构建工具和学习成本，当前场景不需要多端发布。

### 4. 微信登录流程

```
小程序 wx.login() → code
       ↓
POST /api/wx/login { code }
       ↓
后端调用微信 API: https://api.weixin.qq.com/sns/jscode2session
       ↓
获取 openid + session_key
       ↓
查询/创建 User (openid 关联) → 签发 JWT
       ↓
返回 { token, user } → 小程序存 token 到 storage
```

- 后端需要配置 `WX_APP_ID` 和 `WX_APP_SECRET` 环境变量
- 使用 `httpx` 调用微信 API（异步 HTTP 客户端）
- JWT 结构复用现有机制，payload 中新增 `role` 字段

### 5. 录音方案

小程序端使用 `wx.getRecorderManager()` 录制音频：
- 录音格式：`mp3`（兼容性好，体积小）
- 采样率：16000 Hz（匹配 Whisper 要求）
- 声道数：1（单声道）
- 录完后通过 `wx.uploadFile()` 上传到 `/api/wx/evaluate`
- 后端 ffmpeg 已支持 mp3 → wav 转换，无需修改

### 6. 后端 API 路由设计

| 路由组 | 前缀 | 鉴权 | 用途 |
|---|---|---|---|
| 公共 | `/api/health` | 无 | 健康检查 |
| Admin 认证 | `/api/admin/auth/*` | 无/JWT | 管理员登录 |
| Admin 管理 | `/api/admin/*` | JWT + role=admin | 用户管理、题目 CRUD |
| 小程序认证 | `/api/wx/login` | 无 | 微信登录 |
| 小程序业务 | `/api/wx/*` | JWT | 题库浏览、评估、历史 |

**Admin 鉴权中间件**: 创建 `require_admin` 依赖，检查 `current_user.role == 'admin'`

### 7. 数据库迁移

User 表新增字段：
- `role`: `VARCHAR(20)`, 默认 `'user'`, 可选值 `admin`/`user`
- `openid`: `VARCHAR(100)`, nullable, unique, 用于微信登录
- `nickname`: `VARCHAR(100)`, nullable, 微信昵称

通过 Alembic 创建迁移脚本，现有用户默认 `role='user'`。

## Risks / Trade-offs

- **[微信审核风险]** → 小程序上线需通过微信审核，录音类小程序可能需要额外资质。提前准备好类目资质。
- **[录音格式兼容性]** → 不同微信版本/设备录音格式可能不一致。→ 后端 ffmpeg 统一转换，增加格式检测和错误处理。
- **[Whisper 性能]** → 大量用户并发时 Whisper 推理可能成为瓶颈。→ 当前阶段使用单实例，后续可引入任务队列（Celery）。
- **[小程序 token 过期]** → 微信 session_key 有效期不确定。→ JWT 独立过期，小程序端检测 401 自动重新 wx.login。
- **[Admin 后台安全]** → Admin API 暴露在公网。→ role 校验 + 可选 IP 白名单。

## Migration Plan

1. **Phase 1 — 后端扩展**：新增数据库迁移、Admin API、微信登录 API
2. **Phase 2 — Admin 后台改造**：重命名 frontend → admin，改造页面
3. **Phase 3 — 微信小程序开发**：创建小程序项目，实现所有页面
4. **Phase 4 — 联调测试**：前后端联调，录音流程测试
5. **Rollback**: 后端 API 新增为独立路由，不影响现有端点，可通过 Alembic downgrade 回滚数据库

## Open Questions

- 微信小程序的 AppID 和 AppSecret 是否已申请？
- Admin 后台是否需要数据统计仪表板（如每日活跃用户、评分分布）？
- 是否需要题目分类/标签管理功能？
