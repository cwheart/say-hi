## ADDED Requirements

### Requirement: uni-app project initialization
The system SHALL use a uni-app (Vue 3 + Vite + TypeScript) project structure in the `uniapp/` directory, initialized from the official `uni-preset-vue#vite-ts` template.

#### Scenario: Project directory structure
- **WHEN** the `uniapp/` project is initialized
- **THEN** the project SHALL contain: `src/pages/`, `src/components/`, `src/utils/`, `src/static/`, `src/App.vue`, `src/main.ts`, `src/pages.json`, `src/manifest.json`, `package.json`, `tsconfig.json`, `vite.config.ts`

#### Scenario: Dependency installation
- **WHEN** `npm install` (or `pnpm install`) is run in the `uniapp/` directory
- **THEN** all required dependencies SHALL be installed including `@dcloudio/uni-app`, `@dcloudio/uni-mp-weixin`, `@dcloudio/uni-h5`, `vue@3`, and `typescript`

### Requirement: pages.json configuration
The `src/pages.json` SHALL define all page routes, tab bar, and window styles matching the original mini program's `app.json` configuration.

#### Scenario: Page routes
- **WHEN** the application loads `pages.json`
- **THEN** the following pages SHALL be registered: `pages/index/index`, `pages/practice/practice`, `pages/result/result`, `pages/history/history`, `pages/profile/profile`

#### Scenario: Tab bar configuration
- **WHEN** the application renders the tab bar
- **THEN** the tab bar SHALL display three items: "练习" (pages/index/index), "历史" (pages/history/history), "我的" (pages/profile/profile) with corresponding icons and active color `#3b82f6`

#### Scenario: Global window style
- **WHEN** any page is displayed
- **THEN** the navigation bar SHALL use background color `#1e293b`, white text, and title "Say Hi"

### Requirement: manifest.json configuration
The `src/manifest.json` SHALL configure platform-specific settings for both WeChat mini program and H5 builds.

#### Scenario: WeChat mini program settings
- **WHEN** the project is compiled for `mp-weixin`
- **THEN** the manifest SHALL include the WeChat AppID and permission declaration for `scope.record`

#### Scenario: H5 settings
- **WHEN** the project is compiled for `h5`
- **THEN** the manifest SHALL configure the router mode (history), the dev server proxy to the backend API, and the document title "Say Hi"

### Requirement: Build commands
The project SHALL provide npm scripts for development and production builds targeting both platforms.

#### Scenario: WeChat mini program dev build
- **WHEN** the developer runs `npm run dev:mp-weixin`
- **THEN** the system SHALL start a dev build outputting to `dist/dev/mp-weixin/` with file watching enabled

#### Scenario: H5 dev server
- **WHEN** the developer runs `npm run dev:h5`
- **THEN** the system SHALL start a Vite dev server serving the H5 version with API proxy to the backend

#### Scenario: Production build (mini program)
- **WHEN** the developer runs `npm run build:mp-weixin`
- **THEN** the system SHALL output an optimized mini program build to `dist/build/mp-weixin/`

#### Scenario: Production build (H5)
- **WHEN** the developer runs `npm run build:h5`
- **THEN** the system SHALL output an optimized H5 build to `dist/build/h5/`

### Requirement: Conditional compilation support
The project SHALL support uni-app conditional compilation directives to handle platform-specific code.

#### Scenario: MP-WEIXIN conditional block
- **WHEN** code is wrapped in `// #ifdef MP-WEIXIN` ... `// #endif`
- **THEN** the code SHALL be included only in the WeChat mini program build and excluded from H5

#### Scenario: H5 conditional block
- **WHEN** code is wrapped in `// #ifdef H5` ... `// #endif`
- **THEN** the code SHALL be included only in the H5 build and excluded from mini program

#### Scenario: Template conditional compilation
- **WHEN** template markup is wrapped in `<!-- #ifdef MP-WEIXIN -->` ... `<!-- #endif -->`
- **THEN** the markup SHALL be included only in the mini program build
