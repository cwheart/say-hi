## Why

当前系统只有一个 Vue.js 前端，同时承载用户练习和管理功能。需要将前端拆分为两个独立项目：一个 Admin 管理后台（Web）用于管理员管理用户和题目，一个微信小程序用于最终用户通过微信授权后浏览题目、录音和查看评分。微信小程序作为主要用户入口，能大幅降低使用门槛，用户无需安装 App 即可使用。

## What Changes

- **新增 Admin 管理后台**（Vue.js Web 项目）：管理员登录、用户管理（查看/禁用）、题目 CRUD、评估历史查看
- **新增微信小程序**（原生开发）：微信登录（wx.login 获取 openid）、浏览练习题库、录音并上传到后端 Whisper 识别、展示评分结果、查看历史记录
- **后端 API 扩展**：新增 `/api/admin/` 路由组（用户管理、题目 CRUD）、新增 `/api/wx/` 路由组（微信登录、小程序专用接口）、Admin 角色鉴权中间件
- **用户模型扩展**：User 表新增 `role` 字段（admin/user）、新增 `openid` 字段用于微信登录关联
- **移除现有 Vue 前端**中的用户侧功能（登录/注册/练习/历史），保留并改造为 Admin 后台
- **录音方案**：小程序使用 `wx.getRecorderManager()` 录音，上传音频到后端，复用现有 Whisper 识别 + 评分引擎

## Capabilities

### New Capabilities
- `admin-dashboard`: Admin 管理后台前端，包含用户管理、题目 CRUD、数据概览
- `admin-api`: 后端管理员 API 路由，用户列表/禁用、题目增删改查、角色鉴权
- `miniprogram-app`: 微信小程序前端，微信登录、题库浏览、录音、评分展示、历史记录
- `wx-auth`: 微信小程序登录流程，wx.login → 后端换取 openid → JWT token

### Modified Capabilities
- `user-auth`: 新增 role 字段（admin/user），新增 openid 字段，新增微信登录认证方式
- `database`: User 表新增 role、openid 列，新增 Alembic 迁移
- `audio-recording`: 小程序端录音方案（wx.getRecorderManager），音频格式适配（mp3/silk → wav）
- `practice-management`: 新增管理员 CRUD 操作（创建/编辑/删除题目）

## Impact

- **项目结构**：新增 `admin/`（Vue.js Admin 后台）和 `miniprogram/`（微信小程序）目录，现有 `frontend/` 改造为 Admin 后台或移除
- **后端路由**：新增 `/api/admin/*` 和 `/api/wx/*` 路由组，现有 `/api/auth/*` 保留给 Admin 端
- **数据库**：需要新的 Alembic 迁移（users 表加 role + openid 列）
- **依赖**：后端新增 `httpx`（调用微信 API）；小程序无额外依赖（原生开发）
- **部署**：Admin 后台为静态文件部署，小程序需提交微信审核上线
- **音频处理**：小程序录音格式可能为 mp3/aac，后端 ffmpeg 已支持转换
