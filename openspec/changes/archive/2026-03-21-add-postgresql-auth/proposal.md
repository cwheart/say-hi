## Why

当前系统数据完全存储在内存中（JSON 文件 + Python 字典），无法持久化练习记录。需要接入 PostgreSQL 数据库实现数据持久化，同时增加用户系统以支持个人练习历史追踪。

## What Changes

- 接入 PostgreSQL 数据库，使用 SQLAlchemy 2.0 (async) 作为 ORM
- 使用 Alembic 管理数据库迁移
- 新增用户注册/登录系统（邮箱+密码，JWT 认证）
- 将 practices 数据从内存字典迁移到数据库表
- 新增 evaluation_history 表，记录用户每次练习的评分结果
- 新增种子数据初始化脚本，将 practices.json 写入数据库
- 前端增加登录/注册页面、路由守卫、练习历史页面
- 修改 evaluate 接口，将评估结果存入数据库并关联用户

## Capabilities

### New Capabilities
- `user-auth`: 用户注册/登录系统，邮箱+密码认证，JWT token 签发与验证
- `database`: PostgreSQL 连接管理、SQLAlchemy 模型定义、Alembic 迁移、种子数据脚本
- `evaluation-history`: 评估历史记录的存储与查询，支持按用户查看练习记录

### Modified Capabilities
- `practice-management`: practices 数据源从内存 JSON 变更为数据库查询
- `audio-recording`: evaluate 接口需要认证，前端提交时需携带 JWT token
- `feedback-display`: 新增练习历史页面，结果页展示历史最佳分数

## Impact

- **后端新增依赖**: sqlalchemy[asyncio], asyncpg, alembic, passlib[bcrypt], python-jose[cryptography]
- **后端代码**: 新增 database.py、db_models.py、auth 路由、history 路由；重写 practice_service；修改 evaluate 路由和 main.py
- **前端代码**: 新增登录/注册页面、axios 拦截器、路由守卫、练习历史页面
- **基础设施**: 需要本地 PostgreSQL 服务运行，新增 DATABASE_URL 环境变量
- **API 变更**: 新增 /api/auth/*, /api/history/* 端点；/api/evaluate 变为需要认证
