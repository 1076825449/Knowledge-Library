# 管理员操作手册

## 用户管理

### 创建新用户
1. 以 admin 身份登录
2. 访问 `/admin/users`
3. 点击"新增用户"
4. 填写用户名、显示名称、角色

### 角色说明
| 角色 | 权限 |
|------|------|
| admin | 全部权限 |
| editor | 新增/编辑内容，提交审核 |
| reviewer | 审核发布内容 |
| viewer | 只读访问 |

---

## 质量看板

访问 `/admin/quality` 查看：
- active 内容总条数
- 缺失政策依据条目数
- 缺失标签条目数
- 高频问题政策依据数
- 高频问题关联问题数
- 最短解答条目（可能质量不足）

---

## 政策核验

```bash
# 运行政策核验报告
cd /path/to/knowledge-library
python scripts/content/policy_launch_gate.py true

# 查看阻断报告
cat data/reports/policy_verification_blockers_*.txt

# 查看优先强化队列
cat data/reports/priority_reinforce_*.txt
```

**关键指标**：`policy_launch_gate` 列出的条目因政策状态为 needs_update / source_pending / manual_local_review 而阻断发布。需要：
1. 登录国家税务总局官网核实最新政策
2. 更新政策信息
3. 或标记为"人工复核通过"并填写说明

---

## 数据库备份

```bash
# 自动备份（保留最近30份）
python scripts/ops/backup_db.py

# 手动备份
cp database/db/tax_knowledge.db database/backups/手动备份_$(date +%Y%m%d).db

# 恢复
cp database/backups/<备份文件> database/db/tax_knowledge.db
```

---

## 服务管理

```bash
# 启动服务（开发）
cd backend && python app.py

# 生产环境（使用 Gunicorn）
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Docker 部署
docker compose up -d --build
docker compose down
```

---

## 部署前检查

```bash
# 检查环境配置
python scripts/ops/deploy_preflight.py true

# 验证所有依赖
pip install -r requirements.txt
python3 -m pytest tests/ -q
```

---

## 迁移到生产服务器

1. 复制项目到服务器
2. 创建 `.env` 文件（参考 `.env.example`）
3. 运行 `deploy_preflight.py true`
4. 初始化数据库：`bash scripts/db/init_db.sh`
5. 配置 Nginx 反向代理到 `127.0.0.1:5000`
6. 配置 systemd 服务（参考 `deploy/systemd/`）
