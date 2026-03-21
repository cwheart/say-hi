## Why

英语学习者缺乏便捷的发音练习和反馈工具。传统方式需要真人外教逐一纠正，成本高且不可扩展。本项目利用 OpenAI Whisper 语音识别模型，在本地部署一套英语发音识别与评分系统，让用户可以随时录音、获取发音评分和改进建议。

## What Changes

- 新建完整的全栈项目，包含 Vue.js 3 前端和 Python FastAPI 后端
- 前端提供录音界面，用户可以看到目标句子/单词，录制自己的发音
- 后端集成 Whisper 模型进行语音转文字 (Speech-to-Text)
- 实现发音评分算法：将 Whisper 识别结果与目标文本进行对比，从准确度、完整度等维度评分
- 提供逐词对比和高亮反馈，标识发音正确/错误/遗漏的单词
- 内置练习题库（常用单词和句子）

## Capabilities

### New Capabilities
- `audio-recording`: 前端浏览器录音功能，采集用户语音并上传至后端
- `speech-recognition`: 后端 Whisper 模型集成，将音频文件转换为文本
- `pronunciation-scoring`: 发音评分引擎，对比识别文本与目标文本，输出多维度评分
- `practice-management`: 练习题库管理，提供单词和句子练习内容
- `feedback-display`: 前端评分结果展示，包含逐词对比、分数展示和改进建议

### Modified Capabilities

（无，这是全新项目）

## Impact

- **前端**: 新建 Vue.js 3 项目，使用 Vite 构建，依赖 Web Audio API / MediaRecorder API
- **后端**: 新建 FastAPI 项目，依赖 openai-whisper、ffmpeg、python-Levenshtein 等
- **基础设施**: 需要本地安装 ffmpeg；Whisper 模型首次运行需下载模型文件（约 1-3GB）
- **API**: 新建 REST API 端点用于音频上传、发音评估、题库查询
