# backend/ 后端目录

## 技术栈

- **Python Flask** — Web框架
- **Jinja2** — 模板引擎（服务端渲染）
- **SQLite** — 数据库（文件位于 `database/db/tax_knowledge.db`）
- **Werkzeug** — WSGI工具（Flask内置）

## 启动方式

```bash
cd /Volumes/外接硬盘/vibe\ coding/知识库
python backend/app.py
# 服务启动在 http://localhost:5000
```

无需安装依赖（标准库足够），无需 `.env` 文件。密码通过环境变量 `ADMIN_PASSWORD` 修改，默认密码为 `tax2026`。

## 目录结构

```
backend/
├── app.py              # Flask 唯一入口，所有路由在此定义
├── config.py           # 数据库路径、密码、密钥配置
├── requirements.txt    # （预留，当前无需安装额外依赖）
├── routes/             # API蓝图（前后端分离备用）
│   ├── questions.py    # 问题列表/详情API
│   ├── search.py       # 搜索API
│   └── tags.py         # 标签API
├── services/           # 业务逻辑层
│   └── question_service.py  # 问题CRUD、搜索、详情查询
└── README.md
```

## 路由一览

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/questions` | GET | 问题列表页（支持stage/module/tag/region/status过滤） |
| `/question/<code>` | GET | 问题详情页 |
| `/question/new` | GET/POST | 新建问题（需admin认证） |
| `/question/<code>/edit` | GET/POST | 编辑问题（需admin认证） |
| `/api/questions/` | GET | 问题列表API |
| `/api/questions/<code>` | GET | 问题详情API |
| `/api/search/` | GET | 搜索API（?keyword=） |
| `/api/tags/` | GET | 标签字典API |
| `/admin/login` | POST | 管理员登录 |

## 数据层

所有数据操作在 `services/question_service.py`，通过 `backend/config.py` 中的 `DB_PATH` 指向 SQLite 数据库文件。

## 注意事项

- 编辑/新建问题需要admin密码（默认`tax2026`）
- `SECRET_KEY` 默认硬编码，生产环境请通过环境变量覆盖
- 当前为原型阶段，数据库为文件数据库（`tax_knowledge.db`），无并发写入保护
