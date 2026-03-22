## 1. uni-app 项目初始化

- [x] 1.1 使用 `npx degit dcloudio/uni-preset-vue#vite-ts uniapp` 初始化项目骨架
- [x] 1.2 安装依赖并验证 `npm run dev:h5` 和 `npm run dev:mp-weixin` 可正常启动
- [x] 1.3 配置 `src/pages.json` — 页面路由（index/practice/result/history/profile）、tabBar（练习/历史/我的）、globalStyle（导航栏样式）
- [x] 1.4 配置 `src/manifest.json` — appid（mp-weixin）、H5 router mode(history)、devServer proxy、title
- [x] 1.5 将 tabBar 图标资源从 `miniprogram/images/` 复制到 `uniapp/src/static/`
- [x] 1.6 创建 `src/App.vue` 全局入口和 `src/main.ts`

## 2. 工具层 — API 请求封装

- [x] 2.1 创建 `src/utils/request.ts` — 封装 `uni.request`，自动注入 JWT token，处理 401 重登/重定向
- [x] 2.2 创建 `src/utils/upload.ts` — 封装文件上传，MP-WEIXIN 使用 `uni.uploadFile`，H5 使用 `FormData` + `fetch`（条件编译）
- [x] 2.3 创建 `src/utils/storage.ts` — 封装 token 的读写删除（`uni.setStorageSync` / `uni.getStorageSync` / `uni.removeStorageSync`）

## 3. 工具层 — 认证模块

- [x] 3.1 创建 `src/utils/auth.ts` — MP-WEIXIN: `uni.login()` → `/api/wx/login` 静默登录；H5: 检查 token 存在性（条件编译）
- [x] 3.2 实现 `ensureLogin()` — MP-WEIXIN 无 token 时自动 wx 登录；H5 无 token 时跳转登录页
- [x] 3.3 实现 `logout()` — 清除 token 和用户信息，H5 重定向到登录页
- [x] 3.4 在 `request.ts` 中集成 401 处理 — MP-WEIXIN 自动重新 `uni.login` 并重试；H5 清 token 后跳转登录页

## 4. 工具层 — 录音模块

- [x] 4.1 创建 `src/utils/recorder.ts` — MP-WEIXIN 分支: `uni.getRecorderManager()` 封装（mp3, 16kHz, 单声道, 30s）
- [x] 4.2 `recorder.ts` H5 分支: `navigator.mediaDevices.getUserMedia` + `MediaRecorder`（webm/opus, 30s max）
- [x] 4.3 统一导出 `start(callbacks)` / `stop()` 接口，返回录音结果（MP-WEIXIN: tempFilePath, H5: Blob）
- [x] 4.4 实现 H5 端 MediaRecorder 不可用检测，不支持时提示用户

## 5. H5 登录页

- [x] 5.1 创建 `src/pages/login/login.vue` — 邮箱 + 密码表单，调用 `/api/auth/login`
- [x] 5.2 在 `pages.json` 中注册 login 页面（非 tabBar 页，仅 H5 条件编译生效）
- [x] 5.3 实现登录成功后存储 token 并 `uni.switchTab` 到首页
- [x] 5.4 实现登录失败错误提示（"邮箱或密码错误"）

## 6. 首页 — 题目列表 (index)

- [x] 6.1 创建 `src/pages/index/index.vue` — `<script setup lang="ts">` + Composition API
- [x] 6.2 实现分类 tab 切换（全部/word/phrase/sentence）
- [x] 6.3 实现题目列表渲染（text、difficulty badge、category 标签）
- [x] 6.4 实现点击跳转 `uni.navigateTo({ url: '/pages/practice/practice?id=xxx' })`

## 7. 练习页 — 录音与提交 (practice)

- [x] 7.1 创建 `src/pages/practice/practice.vue` — 接收 `id` 参数，加载练习详情
- [x] 7.2 显示目标文本、难度、分类、提示、历史最佳分数
- [x] 7.3 集成录音模块 — 录音按钮状态（idle → recording → recorded）、计时器、波形指示
- [x] 7.4 集成上传模块 — 提交录音到 `/api/wx/evaluate`，附带 `practice_id` 和 `target_text`
- [x] 7.5 提交成功后跳转结果页，传递评分数据

## 8. 结果页 — 评分展示 (result)

- [x] 8.1 创建 `src/pages/result/result.vue` — 接收评分数据
- [x] 8.2 实现分数展示（overall、accuracy、completeness、fluency 进度条 + 颜色编码）
- [x] 8.3 实现 word-compare 逐词对比（green=correct, red=incorrect, orange=missing, gray=extra）
- [x] 8.4 实现"再试一次"按钮 — `uni.navigateBack` 返回练习页

## 9. 历史页 (history)

- [x] 9.1 创建 `src/pages/history/history.vue` — 分页加载历史记录
- [x] 9.2 实现列表渲染（target_text、overall_score、日期）
- [x] 9.3 实现滚动触底加载更多（`onReachBottom`）
- [x] 9.4 实现空状态提示 "No practice history yet"

## 10. 个人页 (profile)

- [x] 10.1 创建 `src/pages/profile/profile.vue` — 显示用户信息和练习统计
- [x] 10.2 MP-WEIXIN 显示昵称（或 "WeChat User"），H5 显示邮箱（条件编译）
- [x] 10.3 显示练习总次数
- [x] 10.4 H5 端显示退出登录按钮，点击清除 token 跳转登录页

## 11. 公共组件

- [x] 11.1 创建 `src/components/score-card.vue` — 分数卡片（进度条 + 分值 + 颜色）
- [x] 11.2 创建 `src/components/word-compare.vue` — 逐词对比（颜色编码）

## 12. 全局样式与类型

- [x] 12.1 创建 `src/uni.scss` — 全局 SCSS 变量（主色 #3b82f6、导航栏 #1e293b、背景 #f8fafc）
- [x] 12.2 创建 `src/App.vue` 全局样式 — 基础重置和通用类
- [x] 12.3 创建 `src/types/index.ts` — Practice、EvaluationResult、User、WordComparison 类型定义

## 13. 后端 CORS 更新

- [x] 13.1 在 `backend/app/main.py` 的 `CORS_ORIGINS` 环境变量文档中注明需包含 H5 域名
- [x] 13.2 在 `.env.example` 中添加 H5 域名示例

## 14. 清理与文档

- [x] 14.1 删除 `miniprogram/` 目录
- [x] 14.2 更新根目录 `README.md` — 项目结构说明（admin / uniapp / backend）
- [x] 14.3 创建 `uniapp/README.md` — 开发指南（安装、dev:h5、dev:mp-weixin、build、目录结构说明）
- [x] 14.4 更新 `.gitignore` — 添加 `uniapp/dist/`、`uniapp/node_modules/`
