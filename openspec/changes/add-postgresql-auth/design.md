## Context

在已有的 Say Hi 英语发音评分系统上，接入 PostgreSQL 数据库、用户认证系统和评估历史记录。当前系统使用内存字典存储 practices 数据，评估结果不持久化。本次改动将系统从「单次体验工具」升级为「可追踪的学习平台」。

技术栈：Vue.js 3 + FastAPI + SQLAlchemy 2.0 (async) + PostgreSQL + JWT

## Goals / Non-Goals

**Goals:**
- 接入 PostgreSQL，所有业务数据持久化
- 完整的邮箱+密码注册登录系统，JWT 认证
- 评估结果存入数据库，支持历史查看
- 种子数据脚本化初始化
- Alembic 管理数据库迁移
- 前端登录/注册页面、路由守卫、历史页面

**Non-Goals:**
- 不做 OAuth / 社交登录
- 不做邮箱验证
- 不做密码重置功能
- 不做 refresh token（只用 access token，过期重新登录）
- 不做权限/角色系统（所有登录用户权限相同）

## Decisions

### 1. ORM：SQLAlchemy 2.0 async + asyncpg

**选择**: SQLAlchemy 2.0 新式 API，配合 asyncpg 驱动实现全异步数据库操作。

**理由**: 最成熟稳定的 Python ORM，async 支持完善，社区和文档丰富。Pydantic schema 和 SQLAlchemy model 分开定义，职责清晰。

### 2. 数据库连接管理

**选择**: 使用 `create_async_engine` + `async_sessionmaker`，通过 FastAPI 依赖注入 `get_db` 提供 session。

```
engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
```

### 3. 密码存储：bcrypt via passlib

**选择**: 使用 `passlib[bcrypt]` 对密码进行哈希。

**理由**: bcrypt 是密码哈希的行业标准，passlib 提供简洁 API。

### 4. JWT 实现：python-jose

**选择**: 使用 `python-jose[cryptography]` 签发和验证 JWT。Token 有效期 24 小时。JWT_SECRET 通过环境变量配置。

**Payload 结构**:
```json
{
  "sub": "<user_uuid>",
  "exp": <timestamp>
}
```

### 5. 认证依赖注入

**选择**: 创建 `get_current_user` 依赖，从 Authorization header 提取 JWT、解析 user_id、查询数据库获取用户。

```
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
```

### 6. 文件结构变更

```
backend/
├── app/
│   ├── database.py              ← 新增: engine, session, get_db
│   ├── models/
│   │   ├── db_models.py         ← 新增: SQLAlchemy User, Practice, EvaluationHistory
│   │   └── schemas.py           ← 重命名自 evaluation.py: Pydantic schemas
│   ├── routers/
│   │   ├── auth.py              ← 新增: register, login, me
│   │   ├── evaluate.py          ← 修改: 存入 DB, 需认证
│   │   ├── practices.py         ← 修改: DB 查询
│   │   └── history.py           ← 新增: 历史记录 CRUD
│   ├── services/
│   │   ├── auth_service.py      ← 新增: JWT + 密码哈希
│   │   ├── deps.py              ← 新增: get_db, get_current_user
│   │   ├── practice_service.py  ← 重写: DB 查询
│   │   └── ...                  (whisper, scoring, audio 不变)
│   └── main.py                  ← 修改: DB 初始化
├── alembic/                     ← 新增: 迁移目录
│   ├── alembic.ini
│   └── versions/
│       └── 001_initial.py
├── scripts/
│   ├── __init__.py
│   └── seed_db.py               ← 新增: 种子数据脚本
└── requirements.txt             ← 更新: 新增依赖
```

### 7. API 端点设计

| 端点 | 方法 | 认证 | 说明 |
|------|------|------|------|
| `/api/auth/register` | POST | 无 | 注册，返回 user + token |
| `/api/auth/login` | POST | 无 | 登录，返回 token |
| `/api/auth/me` | GET | ✅ | 获取当前用户信息 |
| `/api/evaluate` | POST | ✅ | 评估发音（改为需要认证，结果存 DB） |
| `/api/practices` | GET | 无 | 练习列表（改为 DB 查询） |
| `/api/practices/{id}` | GET | 无 | 练习详情（改为 DB 查询） |
| `/api/history` | GET | ✅ | 当前用户评估历史（分页） |
| `/api/history/{id}` | GET | ✅ | 单条评估详情 |
| `/api/health` | GET | 无 | 不变 |

### 8. 前端路由与守卫

```
/login          → LoginView     (公开)
/register       → RegisterView  (公开)
/               → PracticeList  (需登录)
/practice/:id   → PracticeDetail(需登录)
/history        → HistoryList   (需登录)
```

前端使用 axios 拦截器自动附加 `Authorization: Bearer <token>`，401 响应自动跳转登录页。使用 composable `useAuth` 管理认证状态（token 存 localStorage）。

## Risks / Trade-offs

- **[JWT 无 refresh token]** → token 过期后需重新登录。24h 有效期在学习场景下可接受。
- **[密码明文传输]** → 开发阶段 HTTP 传输，生产需 HTTPS。
- **[评估接口改为需认证]** → 这是**行为变更**，未登录用户无法使用评估功能。前端需引导用户先登录。
- **[数据库依赖]** → 系统启动前必须有可用的 PostgreSQL 实例。README 需更新 setup 步骤。
