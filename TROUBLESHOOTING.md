# 故障排查指南

## 端口占用

**症状**：启动时报 `OSError: [Errno 48] Address already in use`

```bash
# 查找占用端口的进程
lsof -i :5000

# 终止占用进程
kill -9 <PID>

# 或使用另一个端口
HOST=127.0.0.1 PORT=5001 python backend/app.py
```

---

## 数据库不存在

**症状**：`sqlite3.OperationalError: no such table`

```bash
# 初始化数据库
bash scripts/db/init_db.sh

# 如果需要恢复备份
cp database/backups/<备份文件> database/db/tax_knowledge.db
```

---

## sqlite3 缺失

**症状**：`ModuleNotFoundError: No module named 'sqlite3'`

```bash
# macOS 安装
brew install sqlite3

# 验证
sqlite3 --version
```

---

## 依赖安装失败

**症状**：`pip install -r requirements.txt` 报错

```bash
# 确保使用正确的 Python 版本
python3 --version  # 需要 3.9+

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 登录失败

**症状**：输入密码后仍然跳转到登录页

1. 确认使用的是 admin 用户名（非邮箱）
2. 确认环境变量 `ADMIN_PASSWORD` 已正确设置
3. 检查浏览器 cookie 是否被禁用
4. 如果忘记密码：在 `.env` 文件中重新设置 `ADMIN_PASSWORD`，重启服务

---

## 权限不足

**症状**：页面显示"权限不足"或操作被拒绝

- 新增/编辑内容：需要 editor 或更高角色
- 审核通过/退回：需要 reviewer 或 admin 角色
- 用户管理：需要 admin 角色
- 联系管理员分配正确角色

---

## 页面 500 错误

**诊断步骤**：

1. 查看终端日志
2. 检查 `database/db/tax_knowledge.db` 文件是否存在
3. 检查磁盘空间
4. 运行 `python scripts/ops/check_env.py` 检查配置

```bash
# 详细错误信息
FLASK_DEBUG=1 python backend/app.py
```

---

## Docker 启动失败

**症状**：`docker compose up` 报错

```bash
# 验证配置文件
docker compose config

# 查看容器日志
docker compose logs -f

# 清理重建
docker compose down -v
docker compose up -d --build
```

---

## policy_launch_gate FAIL

**症状**：政策核验报告大量阻断

这是**预期状态**，不代表系统故障。大约 287 条内容因关联政策状态为 needs_update / source_pending / manual_local_review 而被阻断。

**处理方式**：由 reviewer 或 admin 逐一登录来源网站核实，参考 REVIEWER_GUIDE.md。

---

## 数据库恢复失败

**症状**：恢复备份后数据不对

```bash
# 1. 先备份当前数据库
cp database/db/tax_knowledge.db database/db/问题备份_$(date +%Y%m%d).db

# 2. 确认备份文件完整性
sqlite3 database/backups/<备份文件> "SELECT COUNT(*) FROM question_master"

# 3. 恢复
cp database/backups/<备份文件> database/db/tax_knowledge.db

# 4. 重启服务
```

---

## 测试全部失败

**症状**：`pytest tests/ -q` 全部报错

```bash
# 确保在项目根目录
cd /path/to/knowledge-library

# 激活虚拟环境
source .venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt

# 运行测试
python3 -m pytest tests/ -q
```
