# 发布流程

## 开发流程

### 1. 本地开发
```bash
cd "/Volumes/外接硬盘/vibe coding/网站/知识库"
source .venv/bin/activate

# 创建功能分支
git checkout -b feat/your-feature-name

# 修改代码
# ...

# 运行测试
python3 -m pytest tests/ -q

# 启动服务验证
cd backend && python app.py
```

### 2. 质量门禁
```bash
# 运行质量报告
python scripts/content/quality_report.py

# 运行政策核验
python scripts/content/policy_launch_gate.py true
python scripts/content/audit_policy_verification.py
```

### 3. 备份当前数据库
```bash
# 发布前务必备份
python scripts/ops/backup_db.py

# 或手动备份
mkdir -p database/backups
cp database/db/tax_knowledge.db database/backups/发布前_$(date +%Y%m%d).db
```

### 4. 提交代码
```bash
git add <changed-files>
git commit -m "feat: your feature description"
git push origin feat/your-feature-name
# 创建 Pull Request → 合并到 main
```

### 5. 推送到生产
```bash
git checkout main
git pull origin main
git push origin main
```

---

## 生产部署

### 方式1：Docker Compose
```bash
# 拉取最新代码
git pull origin main

# 重建并启动
docker compose up -d --build

# 验证
curl http://127.0.0.1:5000/api/health
```

### 方式2：直接部署
```bash
# 拉取代码
git pull origin main

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移（如需要）
# bash scripts/db/init_db.sh

# 重启服务
# systemctl restart knowledge-library
# 或
pkill -f "python app.py"
cd backend && nohup python app.py &
```

---

## 回滚流程

### 代码回滚
```bash
# 回到上一个稳定 commit
git revert HEAD
git push origin main

# 或回到指定 commit
git reset --hard <commit-hash>
git push origin main --force
```

### 数据库回滚
```bash
# 1. 备份当前数据库（问题状态）
cp database/db/tax_knowledge.db database/db/回滚问题保留_$(date +%Y%m%d).db

# 2. 找到上一个稳定备份
ls -la database/backups/

# 3. 恢复
cp database/backups/<上一个稳定备份> database/db/tax_knowledge.db

# 4. 重启服务
# pkill -f "python app.py" && cd backend && python app.py &
```

---

## 发布检查清单

- [ ] `pytest tests/ -q` 全部通过
- [ ] `python scripts/ops/check_env.py` 无 ERROR
- [ ] `python scripts/ops/deploy_preflight.py true` 无 BLOCKER
- [ ] `python scripts/content/quality_report.py` 已运行
- [ ] `python scripts/ops/backup_db.py` 已备份
- [ ] `.env` 文件已配置（生产环境）
- [ ] GitHub 已推送
- [ ] Docker 容器已重建（如适用）
- [ ] 服务健康检查通过
