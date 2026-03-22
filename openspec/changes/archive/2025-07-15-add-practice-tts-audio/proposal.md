## Why

用户在练习英语发音前，需要先听到标准发音作为参考。目前系统只展示文本，用户不知道正确发音是什么，只能凭自己理解去读，导致练习效果打折扣。为每道练习题自动生成标准发音音频，并在练习页面提供试听按钮，让用户"先听后读"，提升学习体验。

## What Changes

- 新增后端 TTS 服务，使用 Edge TTS（微软免费引擎）将练习文本合成为 MP3 音频文件
- Practice 创建（Admin CRUD 和 seed 脚本）时自动触发 TTS 生成，音频文件存储到本地 `backend/audio/` 目录
- 数据库 practices 表新增 `audio_url` 字段（nullable），记录生成的音频文件路径
- 新增后端静态文件服务 `/api/audio/{filename}` 或通过 FastAPI StaticFiles 挂载
- 新增后端 API 端点支持手动重新生成音频（Admin 可触发）
- 前端 practice.vue 页面添加小喇叭按钮，点击后通过 `uni.createInnerAudioContext()`（小程序）或 `<audio>` / `new Audio()`（H5）播放标准发音

## Capabilities

### New Capabilities
- `tts-audio-generation`: Edge TTS 音频生成服务、音频文件存储、静态文件服务、自动生成触发机制

### Modified Capabilities
- `practice-management`: Practice 创建/更新时自动触发 TTS 生成；Practice 数据模型新增 `audio_url` 字段；Admin API 支持手动重新生成音频
- `miniprogram-app`: practice.vue 页面新增小喇叭试听按钮，点击后播放标准发音音频（跨平台音频播放）
- `database`: practices 表新增 `audio_url` (varchar, nullable) 列

## Impact

- **后端依赖**: 新增 `edge-tts` Python 包
- **数据库**: 需要 Alembic 迁移添加 `audio_url` 列
- **存储**: 本地 `backend/audio/` 目录存放生成的 MP3 文件
- **API**: 新增音频静态文件服务端点；practice API 响应新增 `audio_url` 字段
- **前端**: practice.vue 页面 UI 变更（新增播放按钮）；新增跨平台音频播放工具
- **Seed 脚本**: 需要更新以在 seed 时也生成音频文件