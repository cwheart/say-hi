## 1. 后端依赖与基础设施

- [x] 1.1 在 `backend/requirements.txt` 中添加 `edge-tts` 依赖
- [x] 1.2 创建 `backend/audio/` 目录并在 `.gitignore` 中添加 `backend/audio/*.mp3`
- [x] 1.3 在 `backend/app/main.py` 中挂载 FastAPI StaticFiles，将 `/api/audio` 映射到 `backend/audio/` 目录

## 2. 数据库变更

- [x] 2.1 在 `backend/app/models/db_models.py` 的 `Practice` 模型中添加 `audio_url = Column(String(500), nullable=True)` 字段
- [x] 2.2 在 `backend/app/models/schemas.py` 的 `Practice` Pydantic 模型中添加 `audio_url: Optional[str] = None` 字段
- [ ] 2.3 创建 Alembic migration：`alembic revision --autogenerate -m "add_audio_url_to_practices"`
- [ ] 2.4 执行迁移：`alembic upgrade head`

## 3. TTS 服务

- [x] 3.1 创建 `backend/app/services/tts_service.py` — `generate_audio(text: str, practice_id: str) -> Optional[str]` 函数
- [x] 3.2 实现 Edge TTS 调用：使用 `edge_tts.Communicate(text, voice="en-US-AriaNeural")`，保存到 `backend/audio/{practice_id}.mp3`
- [x] 3.3 实现目录自动创建（`os.makedirs` if not exists）
- [x] 3.4 实现错误处理：TTS 失败时记录日志并返回 None，不抛异常
- [x] 3.5 实现 `delete_audio(practice_id: str)` — 删除音频文件（如存在）

## 4. Practice Service 集成

- [x] 4.1 修改 `practice_service.create_practice()` — 创建后调用 `tts_service.generate_audio()`，成功后更新 `practice.audio_url`
- [x] 4.2 修改 `practice_service.update_practice()` — 检测 `text` 字段变更后调用 TTS 重新生成
- [x] 4.3 修改 `practice_service.delete_practice()` — 删除前调用 `tts_service.delete_audio()` 清理音频文件

## 5. Admin API 端点

- [x] 5.1 在 `backend/app/routers/admin_practices.py`（或对应的 admin router）中添加 `POST /api/admin/practices/{id}/regenerate-audio` 端点
- [x] 5.2 实现端点逻辑：查找 practice → 调用 TTS 生成 → 更新 audio_url → 返回结果

## 6. Seed 脚本更新

- [x] 6.1 修改 `scripts/seed_db.py` — seed 完成后批量为所有无 audio_url 的练习生成音频
- [x] 6.2 添加生成间隔延时（asyncio.sleep(0.2)）避免速率限制

## 7. 前端音频播放工具

- [x] 7.1 创建 `uniapp/src/utils/audio-player.ts` — 封装跨平台音频播放（MP-WEIXIN: `uni.createInnerAudioContext()`，H5: `new Audio()`）
- [x] 7.2 导出 `playAudio(url)` / `stopAudio()` / `isPlaying()` 接口
- [x] 7.3 实现播放状态回调（onPlay, onStop, onError）

## 8. 前端 practice.vue 改造

- [x] 8.1 在 Practice 类型定义 `uniapp/src/types/index.ts` 中添加 `audio_url?: string` 字段
- [x] 8.2 在 practice.vue 目标文本旁添加 🔊 小喇叭按钮（仅当 `audio_url` 存在时显示）
- [x] 8.3 实现点击播放/停止逻辑，集成 `audio-player.ts`
- [x] 8.4 添加播放中动画状态样式（图标闪烁或波纹动画）
- [x] 8.5 实现播放错误时 toast 提示 "播放失败"
