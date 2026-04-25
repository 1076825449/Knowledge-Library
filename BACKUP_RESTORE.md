# 备份与恢复指南

## 快速命令

```bash
# 备份
python scripts/ops/backup_db.py

# 恢复（先停服务）
cp database/backups/<备份文件> database/db/tax_knowledge.db

# 完整备份（含上传文件）
tar czf backup_$(date +%Y%m%d).tar.gz database/db/ data/reports/ --exclude='database/backups'
```

---

## 备份策略

- 备份脚本自动保留最近 **10 个**备份文件
- 建议开启**定时任务**：每天凌晨 3 点自动备份
- 重要操作（批量导入、审核流程调整）**前**手动备份一次

```cron
# 每天凌晨 3 点备份（Linux/macOS）
0 3 * * * cd /path/to/知识库 && python scripts/ops/backup_db.py >> data/logs/backup.log 2>&1
```

---

## 备份文件位置

`database/backups/tax_knowledge_YYYYMMDD_HHMMSS.db`

---

## 恢复步骤

### 1. 停止服务

```bash
# Systemd
sudo systemctl stop tax-knowledge

# 或者直接 kill
pkill -f "python.*app.py"
pkill -f gunicorn
```

### 2. 备份当前数据库（恢复前必须）

```bash
cp database/db/tax_knowledge.db database/db/tax_knowledge_PRE_RESTORE_$(date +%Y%m%d_%H%M%S).db
```

### 3. 选择备份文件

```bash
# 列出所有备份
ls -lt database/backups/

# 查看备份内容（可选）
sqlite3 database/backups/tax_knowledge_XXXXXXXX.db "SELECT COUNT(*) as total, SUM(status='active') as active FROM question_master;"
```

### 4. 恢复

```bash
cp database/backups/tax_knowledge_YYYYMMDD_HHMMSS.db database/db/tax_knowledge.db
```

### 5. 验证

```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('database/db/tax_knowledge.db')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM question_master')
print('总问题数:', cur.fetchone()[0])
cur.execute(\"SELECT COUNT(*) FROM question_master WHERE status='active'\")
print('Active:', cur.fetchone()[0])
conn.close()
"
```

### 6. 重启服务

```bash
sudo systemctl start tax-knowledge
# 或
python backend/app.py
```

---

## 回滚流程

如果部署后出现严重问题：

```bash
# 1. 停止服务
sudo systemctl stop tax-knowledge

# 2. 找到最近一个正常工作的备份
ls -lt database/backups/ | head -5

# 3. 恢复
cp database/backups/tax_knowledge_XXXXXXXX.db database/db/tax_knowledge.db

# 4. 重启
sudo systemctl start tax-knowledge
```

---

## 定时备份设置（Systemd timer）

```bash
# /etc/systemd/system/tax-knowledge-backup.timer
[Unit]
Description=Tax Knowledge DB Backup

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
# /etc/systemd/system/tax-knowledge-backup.service
[Unit]
Description=Tax Knowledge DB Backup

[Service]
Type=oneshot
WorkingDirectory=/path/to/知识库
ExecStart=/usr/bin/python3 scripts/ops/backup_db.py
```

```bash
sudo systemctl enable tax-knowledge-backup.timer
sudo systemctl start tax-knowledge-backup.timer
```

---

## 注意事项

- **恢复前必须先停止服务**，否则 SQLite 可能损坏
- 备份文件已配置 `.gitignore`，不会推送到 GitHub
- 不要删除 `database/backups/` 目录本身
- 建议定期将 `database/backups/` 同步到另一台服务器或云存储
- 如果 `database/backups/` 目录为空，手动运行一次备份：

```bash
mkdir -p database/backups
python scripts/ops/backup_db.py
```
