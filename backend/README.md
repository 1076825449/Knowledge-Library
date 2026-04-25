# backend/ 后端目录

## 技术栈

- **Python Flask** — Web框架（需安装：`pip install Flask flask-cors`）
- **Jinja2** — 模板引擎（Flask内置）
- **SQLite** — 数据库（Python内置，无需单独安装）
- **Werkzeug** — WSGI工具（Flask内置）

## 启动方式

```bash
cd ..   # 项目根目录
pip install -r requirements.txt   # 安装 Flask + flask-cors
python backend/app.py
# 服务启动在 http://localhost:5000
```

> 密码通过环境变量 `ADMIN_PASSWORD` 设置，**生产环境必须设置强密码，不得使用默认值**。
> `SECRET_KEY` 通过环境变量 `SECRET_KEY` 修改，生产环境必须更换。

## 目录结构

```
backend/
├── app.py              # Flask 唯一入口，所有页面路由在此定义
├── config.py           # 数据库路径、密码、密钥配置
├── routes/             # API蓝图（前后端分离备用，非前端直接调用）
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
| `/question/new` | GET/POST | 新建问题（需admin认证，未认证时由 admin_required 渲染 admin_login.html） |
| `/question/<code>/edit` | GET/POST | 编辑问题（需admin认证，未认证时由 admin_required 渲染 admin_login.html） |
| `/api/questions/` | GET | 问题列表API |
| `/api/questions/<code>` | GET | 问题详情API |
| `/api/search/` | GET | 搜索API（?keyword=） |
| `/api/tags/` | GET | 标签字典API |

> **认证说明**：`admin_login.html` 不是独立路由页面，而是由 `/question/new` 和 `/question/<code>/edit` 的 `admin_required` 装饰器在检测到未认证时按需渲染的登录模板。管理员通过 POST 密码到这两个路径的任一个即可完成认证。

## 数据层

所有数据操作在 `services/question_service.py`，通过 `backend/config.py` 中的 `DB_PATH` 指向 SQLite 数据库文件。

## 注意事项

- 编辑/新建问题需要admin密码（通过环境变量 `ADMIN_PASSWORD` 设置，必须设置）
- `SECRET_KEY` 通过环境变量 `SECRET_KEY` 设置，生产环境必须设置
- 当前为原型阶段，数据库为文件数据库（`tax_knowledge.db`），无并发写入保护
