## Context

本项目是一个全新的英语发音识别评分系统。目前工作目录为空，需要从零搭建前后端项目。系统面向英语学习者，核心流程为：用户在浏览器端录音 → 上传到后端 → Whisper 模型转文字 → 与目标文本对比评分 → 返回结果并在前端展示。

系统采用前后端分离架构：
- **前端**: Vue.js 3 + Vite + TypeScript
- **后端**: Python FastAPI + Whisper（本地部署）
- **通信**: REST API + 文件上传（multipart/form-data）

## Goals / Non-Goals

**Goals:**
- 提供完整的浏览器端录音体验，支持录制、回放、上传
- 利用 Whisper 模型在本地进行高质量语音识别（无需外部 API 密钥）
- 实现多维度发音评分（准确度、完整度、流利度）
- 提供逐词对比视图，直观展示发音差异
- 内置基础练习题库，用户开箱即用
- 响应式设计，支持移动端使用

**Non-Goals:**
- 不实现用户注册/登录系统（MVP 阶段）
- 不实现音素级别的精确评估（Whisper 是句级/词级识别）
- 不支持实时流式语音识别（采用录完后上传方式）
- 不实现学习进度追踪和数据持久化（MVP 阶段使用内存存储）
- 不支持多语言（仅英语）

## Decisions

### 1. Whisper 模型尺寸选择：默认使用 `base` 模型

**选择**: 默认加载 Whisper `base` 模型（约 142MB），可通过环境变量配置为其他尺寸。

**备选方案**:
- `tiny` (39MB): 速度最快但准确率较低
- `small` (466MB): 准确率更高但加载慢
- `medium/large`: 准确率最佳但资源需求高

**理由**: `base` 在准确率和资源消耗之间取得较好平衡，适合开发和本地使用场景。

### 2. 音频格式：前端录制 WebM，后端转换为 WAV

**选择**: 前端使用 MediaRecorder API 录制 WebM/Opus 格式，后端使用 ffmpeg 转换为 WAV 后送入 Whisper。

**备选方案**:
- 前端直接录制 WAV: 文件体积大，上传慢
- 使用 lamejs 前端转 MP3: 增加前端复杂度

**理由**: WebM 压缩率高，上传速度快；Whisper 对 WAV 支持最好；ffmpeg 转换稳定可靠。

### 3. 发音评分算法：基于编辑距离 + 词级对齐

**选择**: 使用 Levenshtein 距离进行词级对齐，计算三个维度的分数：
- **准确度 (Accuracy)**: 正确识别的词占目标词的比例
- **完整度 (Completeness)**: 目标词中被识别到的比例
- **流利度 (Fluency)**: 基于 Whisper 返回的置信度和语速估算

**备选方案**:
- 使用 difflib: 简单但对齐效果不如 Levenshtein
- 使用音素对比 (g2p + phoneme distance): 更精确但复杂度高

**理由**: 词级 Levenshtein 对比实现简单、效果直观，适合 MVP。

### 4. 项目目录结构

```
say-hi/
├── frontend/              # Vue.js 前端
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   ├── composables/   # 组合式函数 (录音、API调用)
│   │   ├── views/         # 页面视图
│   │   ├── types/         # TypeScript 类型定义
│   │   └── assets/        # 静态资源
│   ├── package.json
│   └── vite.config.ts
├── backend/               # FastAPI 后端
│   ├── app/
│   │   ├── main.py        # FastAPI 入口
│   │   ├── routers/       # API 路由
│   │   ├── services/      # 业务逻辑 (Whisper、评分)
│   │   ├── models/        # 数据模型
│   │   └── data/          # 练习题库数据
│   ├── requirements.txt
│   └── .env.example
└── openspec/              # OpenSpec 配置
```

### 5. API 设计

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/evaluate` | POST | 上传音频 + 目标文本，返回评分结果 |
| `/api/practices` | GET | 获取练习题库列表 |
| `/api/practices/{id}` | GET | 获取单个练习详情 |
| `/api/health` | GET | 健康检查（含模型加载状态） |

### 6. 前端状态管理：使用 Composables（组合式函数）

**选择**: 不引入 Pinia/Vuex，使用 Vue 3 Composition API 的 composables 管理状态。

**理由**: 应用状态简单，composables 足以应对；减少依赖，降低学习成本。

## Risks / Trade-offs

- **[Whisper 模型加载时间]** → 首次请求可能较慢（模型加载需数秒）。**缓解**: 应用启动时预加载模型，提供 `/health` 端点反馈加载状态。

- **[ffmpeg 依赖]** → 用户必须在系统中安装 ffmpeg。**缓解**: 在 README 中明确说明，提供各平台安装指引。

- **[Whisper 识别准确度限制]** → Whisper 是通用语音识别模型，对非标准发音可能过于"宽容"或"严格"。**缓解**: 使用 `base` 或更大模型提升准确度；评分算法中增加容错机制。

- **[浏览器兼容性]** → MediaRecorder API 在部分旧浏览器不支持。**缓解**: 前端检测支持情况并给出提示。

- **[大文件上传]** → 长录音文件可能较大。**缓解**: 前端限制录音时长（最长 30 秒），后端限制上传文件大小。
