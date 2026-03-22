## Context

用户练习发音前需要听到标准发音作为参考。系统需要在练习题创建时自动生成 TTS 音频，并在前端提供播放功能。后端使用 FastAPI，前端是 uni-app (Vue 3)，数据库是 PostgreSQL。

## Goals / Non-Goals

**Goals:**
- 使用 Edge TTS 自动为每道练习生成英语标准发音 MP3 文件
- Practice 创建时自动触发生成，文本更新时自动重新生成
- 音频文件存储在后端本地磁盘，通过 FastAPI StaticFiles 提供访问
- 前端 practice.vue 添加小喇叭按钮，支持小程序和 H5 双平台音频播放
- Admin 可手动触发重新生成音频
- seed 脚本批量生成已有练习的音频

**Non-Goals:**
- 不支持多种语音/口音选择（后续可扩展，当前固定一种）
- 不做音频 CDN 分发（当前本地存储即可）
- 不支持用户自定义音频上传

## Decisions

### Decision 1: TTS 引擎 — Edge TTS

**选择**: 使用 `edge-tts` Python 包，选择 `en-US-AriaNeural` 女声。

**理由**: 免费、无需 API Key、音质接近商业级、支持异步调用。`edge-tts` 是轻量 Python 包，直接 `pip install edge-tts`。

**替代方案**: OpenAI TTS（收费）、pyttsx3（音质差）、Google TTS（需 API Key）。

### Decision 2: 音频存储 — 本地磁盘 + StaticFiles

**选择**: 音频文件存储到 `backend/audio/` 目录，文件名使用 `{practice_id}.mp3`。通过 FastAPI `StaticFiles` 挂载到 `/api/audio/`。

**理由**: 简单直接，无需对象存储服务。练习数量可控（几百到几千条），本地存储完全够用。文件名用 practice_id 确保唯一且可预测。

**文件路径**:
```
backend/audio/
├── hello.mp3
├── good-morning.mp3
├── how-are-you.mp3
└── ...
```

**URL 映射**: `GET /api/audio/hello.mp3` → 返回 MP3 文件

### Decision 3: 生成时机 — 创建/更新后异步生成

**选择**: 在 `practice_service.create_practice()` 和 `update_practice()` 执行完 DB 操作后，调用 TTS 服务生成音频。生成过程使用 `asyncio` 异步执行，不阻塞 API 响应。

**流程**:
```
Admin 创建 Practice
       │
       ▼
  DB insert/update
       │
       ▼
  TTS 生成 (async)
       │
       ▼
  保存 MP3 到 backend/audio/{id}.mp3
       │
       ▼
  更新 DB: audio_url = /api/audio/{id}.mp3
```

**容错**: TTS 生成失败不影响 Practice 创建，`audio_url` 保持 null。日志记录失败信息。

### Decision 4: 数据库变更 — 新增 audio_url 列

**选择**: practices 表新增 `audio_url` VARCHAR(500) nullable 列。使用 Alembic migration。

**值**: 存储相对 URL 如 `/api/audio/hello.mp3`，前端直接拼接 baseURL 使用。

### Decision 5: 前端音频播放 — 跨平台方案

**选择**: 创建 `src/utils/audio-player.ts` 工具，使用条件编译：
- **MP-WEIXIN**: `uni.createInnerAudioContext()` 播放远程 URL
- **H5**: `new Audio(url)` 播放

**交互**: practice.vue 目标文本旁显示 🔊 图标按钮，点击播放/停止。播放中图标变为动画状态。

### Decision 6: Admin 手动重新生成

**选择**: 新增 Admin API `POST /api/admin/practices/{id}/regenerate-audio`，调用 TTS 服务重新生成并覆盖原文件。

**用途**: TTS 引擎更新后想刷新音频，或某个文件损坏时手动修复。

## Risks / Trade-offs

**[Edge TTS 服务可用性]** → Edge TTS 依赖微软在线服务，网络不通时无法生成。
→ 缓解: 生成失败不阻塞业务，`audio_url` 为 null 时前端隐藏播放按钮。

**[音频文件一致性]** → Practice 文本更新后音频可能与文本不一致。
→ 缓解: `update_practice` 中检测文本变更后自动重新生成。

**[磁盘占用]** → 每个 MP3 约 10-50KB，1000 条练习约 10-50MB。
→ 缓解: 占用极小，不需要特殊处理。

**[并发生成]** → seed 脚本批量生成时可能触发速率限制。
→ 缓解: 添加适当的延时间隔（如每次生成间隔 200ms）。