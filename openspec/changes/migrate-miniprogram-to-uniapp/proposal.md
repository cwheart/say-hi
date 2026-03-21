## Why

当前小程序采用微信原生开发（wxml/wxss/js），只能在微信客户端内运行，无法通过浏览器 H5 访问。用户希望在微信外（如手机浏览器、分享链接）也能使用练习功能。采用 uni-app (Vue 3 + Vite) 重构小程序端，一套代码同时编译为微信小程序和 H5，降低维护成本并扩大用户触达渠道。

## What Changes

- **BREAKING** 删除 `miniprogram/` 目录下的原生小程序代码（wxml/wxss/js 文件）
- 新建 `uniapp/` 目录，使用 uni-app (Vue 3 + Vite + TypeScript) 重新实现所有页面和组件
- 将原生 API 调用（`wx.request`、`wx.uploadFile`、`wx.getRecorderManager`、`wx.login`、`wx.setStorageSync`）替换为 uni-app 跨平台 API（`uni.request`、`uni.uploadFile`、`uni.getRecorderManager`、条件编译处理平台差异）
- H5 端实现替代方案：使用 Web `MediaRecorder` API 替代 `uni.getRecorderManager`（H5 不支持），使用 H5 登录流程（邮箱密码或 OAuth）替代 `wx.login`
- 新增 H5 条件编译适配层，处理录音、登录、文件上传等平台差异
- 更新后端 CORS 配置以支持 H5 域名访问
- 新增 H5 部署配置（nginx 或静态托管）

## Capabilities

### New Capabilities
- `uniapp-project`: uni-app 项目结构、配置、条件编译策略和构建流程
- `h5-adaptation`: H5 平台适配层，包括 Web 录音、H5 登录、文件上传等平台差异处理

### Modified Capabilities
- `miniprogram-app`: **BREAKING** 从原生小程序结构迁移为 uni-app Vue 3 SFC 页面结构，页面功能不变但实现方式完全重写
- `audio-recording`: 录音实现从纯微信原生 API 改为条件编译方案——小程序端用 `uni.getRecorderManager`，H5 端用 Web `MediaRecorder` API
- `wx-auth`: 登录认证增加 H5 端适配——小程序端保持 `wx.login` 流程，H5 端使用邮箱密码登录或浏览器内 OAuth

## Impact

- **前端代码**: 删除 `miniprogram/` 全部文件，新建 `uniapp/` 项目，所有页面用 Vue 3 SFC 重写
- **后端 API**: 无逻辑变更，但需更新 CORS `allow_origins` 以包含 H5 域名
- **依赖**: 新增 `@dcloudio/uni-app`、`vue@3`、`typescript`、`vite` 等 uni-app 工具链依赖
- **构建产物**: 从单一微信小程序产物变为两个——`dist/mp-weixin/`（小程序）和 `dist/h5/`（H5 网页）
- **部署**: 新增 H5 静态资源部署流程，小程序部署流程从直接上传源码改为上传 uni-app 编译产物
- **文档**: 更新 README 和开发指南