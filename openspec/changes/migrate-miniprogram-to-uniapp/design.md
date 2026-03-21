## Context

当前 `miniprogram/` 使用微信原生开发（wxml/wxss/js），只能运行在微信客户端中。项目需要同时支持微信小程序和 H5 浏览器访问。现有小程序包含 5 个页面（index、practice、result、history、profile）、2 个组件（score-card、word-compare）和 3 个工具模块（api、auth、recorder）。

后端 FastAPI 已提供完整的 `/api/wx/*` 路由和 `/api/auth/*` 路由，分别支持小程序和 Web 端认证。CORS 通过环境变量 `CORS_ORIGINS` 配置。

## Goals / Non-Goals

**Goals:**
- 使用 uni-app (Vue 3 + Vite + TypeScript) 重写小程序端，一套代码编译为微信小程序和 H5
- 保持所有现有功能不变：题目浏览、分类筛选、录音练习、评分展示、历史记录、个人中心
- H5 端可通过浏览器直接访问，支持移动端和桌面端
- H5 端使用 Web MediaRecorder API 进行录音，小程序端保持使用 `uni.getRecorderManager`
- H5 端使用邮箱密码登录（复用 `/api/auth/login`），小程序端保持微信静默登录
- 通过 uni-app 条件编译 `#ifdef` / `#ifndef` 处理平台差异

**Non-Goals:**
- 不涉及 Admin 管理后台的任何改动
- 不修改后端 API 逻辑（仅更新 CORS 配置）
- 不支持 App（iOS/Android）端编译
- 不实现 PWA 离线模式
- 不做 UI 重新设计，保持与原生小程序一致的视觉风格

## Decisions

### Decision 1: 项目结构 — 独立 `uniapp/` 目录

**选择**: 新建 `uniapp/` 目录替代 `miniprogram/`，使用 `npx degit dcloudio/uni-preset-vue#vite-ts` 初始化。

**理由**: uni-app CLI 项目有自己的构建体系和目录规范（`src/pages/`、`src/components/`、`src/static/`），与原生小程序目录结构完全不同。独立目录避免混淆。

**替代方案**: 在原 `miniprogram/` 目录内初始化 — 目录语义不匹配，放弃。

### Decision 2: 条件编译策略 — 适配层 + 条件编译指令

**选择**: 创建 `src/utils/platform.ts` 统一适配层，在调用处使用 `// #ifdef MP-WEIXIN` / `// #ifdef H5` 条件编译指令处理分支逻辑。

**理由**: uni-app 内置条件编译是官方推荐方案，编译时消除无关代码。适配层封装平台差异，页面组件层保持统一。

**关键分支点**:
| 功能 | 小程序 (MP-WEIXIN) | H5 |
|---|---|---|
| 登录 | `uni.login()` → `/api/wx/login` | 邮箱密码表单 → `/api/auth/login` |
| 录音 | `uni.getRecorderManager()` | Web `MediaRecorder` API |
| 文件上传 | `uni.uploadFile()` | `FormData` + `fetch`/`XMLHttpRequest` |
| 存储 | `uni.setStorageSync()` | `localStorage`（uni-app 已自动映射） |

### Decision 3: H5 录音方案 — Web MediaRecorder API

**选择**: H5 端使用 `navigator.mediaDevices.getUserMedia()` + `MediaRecorder` 录制 webm/opus 音频。

**理由**: MediaRecorder 是浏览器标准 API，主流移动/桌面浏览器均支持。后端已有 ffmpeg 转换链路可处理 webm 格式。

**约束**: H5 录音产物格式为 webm（浏览器不支持直接录 mp3），上传到 `/api/wx/evaluate` 时后端统一用 ffmpeg 转换后送 Whisper。

### Decision 4: H5 登录流程 — 复用现有 `/api/auth/login`

**选择**: H5 端展示邮箱/密码登录表单，调用已有的 `/api/auth/login` 端点获取 JWT。

**理由**: 后端已有完整的邮箱密码认证流程和 JWT 签发机制，无需新增后端代码。小程序端继续使用 `uni.login()` + `/api/wx/login`。

**替代方案**: 微信公众号网页授权 OAuth — 需要额外申请公众号权限，且限制在微信内置浏览器中，放弃。

### Decision 5: 页面路由与 TabBar

**选择**: 在 `pages.json` 中配置页面路由和 tabBar，与原生 `app.json` 保持相同的页面结构。

**路由映射**:
```
pages/index/index     → src/pages/index/index.vue
pages/practice/practice → src/pages/practice/practice.vue
pages/result/result   → src/pages/result/result.vue
pages/history/history → src/pages/history/history.vue
pages/profile/profile → src/pages/profile/profile.vue
```

H5 端 tabBar 由 uni-app 自动渲染为底部导航组件。

### Decision 6: TypeScript + Composition API

**选择**: 所有页面和工具使用 TypeScript + Vue 3 `<script setup lang="ts">` 编写。

**理由**: 与 Admin 管理后台技术栈一致（都是 Vue 3 + TS），降低维护者认知负担。uni-app Vue 3 版本完整支持 Composition API。

## Risks / Trade-offs

**[H5 录音兼容性]** → 部分旧版浏览器不支持 MediaRecorder API。  
→ 缓解: 在录音前检测 `navigator.mediaDevices` 是否存在，不支持时显示提示"请使用现代浏览器或微信小程序"。

**[uni-app 编译差异]** → uni-app 条件编译可能在某些边缘场景产生平台差异。  
→ 缓解: 关键功能（录音、登录、上传）通过独立适配层隔离，页面层不直接调用平台 API。

**[H5 音频格式]** → H5 端录制 webm，与小程序端 mp3 不同，增加后端处理复杂度。  
→ 缓解: 后端 ffmpeg 转换已支持多格式输入，无需改动。

**[原生小程序代码丢弃]** → 删除 `miniprogram/` 是不可逆操作。  
→ 缓解: 代码在 git 历史中保留；归档变更前已记录完整目录结构。

**[H5 部署]** → H5 产物需要独立的静态资源托管和域名配置。  
→ 缓解: 提供 nginx 配置示例和环境变量说明。