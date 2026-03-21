# Say Hi - User App (uni-app)

Cross-platform user application built with **uni-app (Vue 3 + Vite + TypeScript)**, compiling to both **WeChat Mini Program** and **H5 web app**.

## Prerequisites

- Node.js 18+
- npm or pnpm
- [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html) (for Mini Program development)

## Setup

```bash
# Install dependencies
npm install
```

## Development

### H5 (Web Browser)

```bash
npm run dev:h5
```

Opens at `http://localhost:5174` with API proxy to `http://localhost:8000`.

### WeChat Mini Program

```bash
npm run dev:mp-weixin
```

Then open **微信开发者工具**, import `dist/dev/mp-weixin/`.

## Production Build

```bash
# H5
npm run build:h5
# Output: dist/build/h5/

# WeChat Mini Program
npm run build:mp-weixin
# Output: dist/build/mp-weixin/
```

## Project Structure

```
uniapp/
├── src/
│   ├── pages/
│   │   ├── index/         # Practice library (tab)
│   │   ├── practice/      # Recording & submission
│   │   ├── result/        # Score display
│   │   ├── history/       # Evaluation history (tab)
│   │   ├── profile/       # User profile (tab)
│   │   └── login/         # H5-only email/password login
│   ├── components/
│   │   ├── score-card.vue     # Score progress bar
│   │   └── word-compare.vue   # Word-by-word comparison
│   ├── utils/
│   │   ├── request.ts    # uni.request wrapper with JWT & 401 handling
│   │   ├── upload.ts     # Cross-platform file upload (条件编译)
│   │   ├── auth.ts       # Login/logout (wx.login vs email/password)
│   │   ├── recorder.ts   # Cross-platform recorder (条件编译)
│   │   └── storage.ts    # Token & user storage
│   ├── types/
│   │   └── index.ts      # TypeScript interfaces
│   ├── static/            # Tab bar icons
│   ├── App.vue            # Global styles & lifecycle
│   ├── main.ts            # App entry point
│   ├── pages.json         # Page routes & tab bar config
│   ├── manifest.json      # Platform-specific settings
│   └── uni.scss           # Global SCSS variables
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Platform Differences

| Feature | WeChat Mini Program | H5 |
|---|---|---|
| Login | `uni.login()` → `/api/wx/login` (silent) | Email/password → `/api/auth/login` |
| Recording | `uni.getRecorderManager()` (mp3) | `MediaRecorder` API (webm) |
| File Upload | `uni.uploadFile()` | `FormData` + `fetch` |
| Storage | `uni.setStorageSync()` | `localStorage` (auto-mapped) |
| 401 Handling | Auto re-login via `uni.login()` | Redirect to login page |

Platform-specific code uses uni-app conditional compilation:
```ts
// #ifdef MP-WEIXIN
// WeChat-only code
// #endif

// #ifdef H5
// H5-only code
// #endif
```

## Configuration

- **WeChat AppID**: Set in `src/manifest.json` → `mp-weixin.appid`
- **API Proxy**: Configured in `src/manifest.json` → `h5.devServer.proxy`
- **Backend URL**: Uses `/api` prefix, proxied in dev, configure in production deployment