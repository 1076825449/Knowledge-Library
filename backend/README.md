# backend/ 后端目录

## 技术栈建议

当前阶段可选择：

- **Python Flask/FastAPI**（轻量）
- **Node.js Express/Koa**（如果前端用 JS）
- **直接前端直连 SQLite**（原型阶段最轻量）

后续可迁移到 Django、Spring Boot 等。

## 起步

```bash
cd backend
# Python 方案
pip install -r requirements.txt
python main.py

# Node.js 方案
npm install
node index.js
```

## 目录结构

```
backend/
├── README.md           # 本文件
├── app/                # 应用入口
├── routes/             # 路由层
├── services/          # 业务逻辑层
├── models/            # 数据访问层
├── utils/             # 工具函数
├── config/            # 配置
├── requirements.txt   # Python 依赖（如用 Python）
└── package.json       # Node.js 依赖（如用 Node.js）
```

## 推荐接口能力

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/questions` | GET | 问题列表（支持分页、筛选） |
| `/api/questions/:code` | GET | 问题详情 |
| `/api/questions/:code/policies` | GET | 问题关联的政策依据 |
| `/api/questions/:code/related` | GET | 关联问题 |
| `/api/questions/stage/:code` | GET | 按阶段查询 |
| `/api/questions/module/:code` | GET | 按模块查询 |
| `/api/questions/tag/:code` | GET | 按标签查询 |
| `/api/search` | GET | 搜索 |
| `/api/tags` | GET | 标签列表 |
| `/api/updates` | GET | 最近更新 |
