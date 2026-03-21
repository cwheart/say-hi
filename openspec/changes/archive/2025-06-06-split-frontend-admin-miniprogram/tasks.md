## 1. Database & Model Extension

- [x] 1.1 Update `backend/app/models/db_models.py` — User model add: role (VARCHAR(20), default 'user'), openid (VARCHAR(100), unique, nullable), nickname (VARCHAR(100), nullable), is_active (boolean, default true)
- [x] 1.2 Update `backend/app/models/db_models.py` — Practice model add: updated_at (timestamp)
- [x] 1.3 Create Alembic migration — auto-generate for User + Practice schema changes, set existing users role='user', is_active=true
- [x] 1.4 Update `backend/app/models/schemas.py` — add role, openid, nickname, is_active to user schemas; add PracticeCreate, PracticeUpdate schemas
- [x] 1.5 Update `backend/.env.example` — add WX_APP_ID, WX_APP_SECRET

## 2. Backend Auth Extension

- [x] 2.1 Update `backend/app/services/auth_service.py` — include role in JWT payload (create_access_token), extract role in decode
- [x] 2.2 Update `backend/app/services/deps.py` — add `require_admin` dependency that checks current_user.role == 'admin'; add is_active check in get_current_user
- [x] 2.3 Update `backend/requirements.txt` — add httpx

## 3. WeChat Login API

- [x] 3.1 Create `backend/app/services/wx_service.py` — call WeChat jscode2session API with httpx, return openid
- [x] 3.2 Create `backend/app/routers/wx.py` — POST /api/wx/login (accept code, call wx_service, find/create user by openid, return JWT)
- [x] 3.3 Add wx router to `backend/app/main.py`

## 4. Mini Program API Routes

- [x] 4.1 Create `backend/app/routers/wx_practices.py` — GET /api/wx/practices (list), GET /api/wx/practices/{id} (detail), require JWT auth
- [x] 4.2 Create `backend/app/routers/wx_evaluate.py` — POST /api/wx/evaluate (upload audio, same logic as evaluate.py, require JWT)
- [x] 4.3 Create `backend/app/routers/wx_history.py` — GET /api/wx/history (paginated, current user), GET /api/wx/history/{id}
- [x] 4.4 Register all wx_* routers in `backend/app/main.py`

## 5. Admin API Routes

- [x] 5.1 Create `backend/app/routers/admin_auth.py` — POST /api/admin/auth/login (email+password, verify role=admin, return JWT)
- [x] 5.2 Create `backend/app/routers/admin_users.py` — GET /api/admin/users (paginated), PATCH /api/admin/users/{id}/disable, PATCH /api/admin/users/{id}/enable
- [x] 5.3 Create `backend/app/routers/admin_practices.py` — POST /api/admin/practices (create), PUT /api/admin/practices/{id} (update), DELETE /api/admin/practices/{id} (delete)
- [x] 5.4 Create `backend/app/routers/admin_history.py` — GET /api/admin/history (all users, paginated, filterable by user_id)
- [x] 5.5 Register all admin_* routers in `backend/app/main.py`

## 6. Practice Service Extension

- [x] 6.1 Update `backend/app/services/practice_service.py` — add create_practice, update_practice, delete_practice async functions

## 7. Seed Admin User

- [x] 7.1 Update `backend/scripts/seed_db.py` — add option to create initial admin user (email + password from env or args)

## 8. Admin Frontend — Project Restructure

- [x] 8.1 Rename `frontend/` → `admin/` directory
- [x] 8.2 Update `admin/package.json` — change name to "say-hi-admin"
- [x] 8.3 Update `admin/vite.config.ts` — update proxy target if needed
- [x] 8.4 Remove user-side views: `LoginView.vue`, `RegisterView.vue`, `PracticeList.vue`, `PracticeDetail.vue`, `HistoryList.vue`
- [x] 8.5 Remove user-side composables: `useAudioRecorder.ts`; remove user-facing components: `AudioRecorder.vue`, `EvaluationResult.vue`, `BrowserWarning.vue`

## 9. Admin Frontend — Auth & Layout

- [x] 9.1 Update `admin/src/composables/useAuth.ts` — login calls `/api/admin/auth/login`, check role=admin on login
- [x] 9.2 Update `admin/src/composables/useApi.ts` — change base URL endpoints to `/api/admin/*`
- [x] 9.3 Create `admin/src/views/AdminLogin.vue` — admin login page with email + password
- [x] 9.4 Create `admin/src/components/AdminLayout.vue` — sidebar navigation layout (Dashboard, Users, Practices, History, Logout)
- [x] 9.5 Update `admin/src/App.vue` — use AdminLayout for authenticated routes

## 10. Admin Frontend — Pages

- [x] 10.1 Create `admin/src/views/DashboardView.vue` — overview page (user count, practice count, recent evaluations)
- [x] 10.2 Create `admin/src/views/UsersView.vue` — paginated user table with enable/disable buttons
- [x] 10.3 Create `admin/src/views/PracticesView.vue` — practice list table with create/edit/delete actions
- [x] 10.4 Create `admin/src/views/PracticeFormView.vue` — create/edit form for a practice item
- [x] 10.5 Create `admin/src/views/HistoryView.vue` — all evaluations table with user email, filterable
- [x] 10.6 Update `admin/src/router/index.ts` — replace routes with admin routes (login, dashboard, users, practices, history)
- [x] 10.7 Update `admin/src/types/index.ts` — add admin-specific types (AdminUser, PracticeForm, etc.)

## 11. Mini Program — Project Setup

- [x] 11.1 Create `miniprogram/` directory with standard structure: app.js, app.json, app.wxss, project.config.json, sitemap.json
- [x] 11.2 Configure `app.json` — pages list, tabBar (Practice, History, Profile), window style, permission (scope.record)
- [x] 11.3 Create `miniprogram/utils/api.js` — wx.request wrapper with base URL, JWT token header, 401 auto re-login
- [x] 11.4 Create `miniprogram/utils/auth.js` — wx.login flow, token storage (wx.setStorageSync), login state management
- [x] 11.5 Create `miniprogram/utils/recorder.js` — wx.getRecorderManager() wrapper with start/stop/error handling, mp3 format, 16kHz

## 12. Mini Program — Pages

- [x] 12.1 Create `miniprogram/pages/index/` — practice library page with category tabs (All, Word, Phrase, Sentence), difficulty badges, tap to navigate
- [x] 12.2 Create `miniprogram/pages/practice/` — practice detail page with target text, record button, stop button, submit button, loading state
- [x] 12.3 Create `miniprogram/pages/result/` — evaluation result page with score display (overall, accuracy, completeness, fluency), word comparison, try again button
- [x] 12.4 Create `miniprogram/pages/history/` — history list page with scroll-view, load more, empty state
- [x] 12.5 Create `miniprogram/pages/profile/` — profile page with user info, practice count

## 13. Mini Program — Components

- [x] 13.1 Create `miniprogram/components/score-card/` — reusable score display component with progress bar and color coding
- [x] 13.2 Create `miniprogram/components/word-compare/` — word-by-word comparison component with color-coded status

## 14. Documentation & Config

- [x] 14.1 Update `README.md` — document new project structure (admin + miniprogram + backend), setup instructions for each
- [x] 14.2 Update `.gitignore` — add miniprogram build artifacts, node_modules in admin/
- [x] 14.3 Create `miniprogram/README.md` — mini program setup and development guide
