-- ============================================================
-- 文件：004_add_policy_verification_fields.sql
-- 描述：为 policy_basis 增加官方来源与联网核验字段
-- 适用：已有数据库迁移。全新初始化库已在 001_create_core_tables.sql 中包含这些字段。
-- 注意：SQLite 不支持 ALTER TABLE ADD COLUMN IF NOT EXISTS。
--      执行前请先用 PRAGMA table_info(policy_basis) 确认字段尚不存在。
-- ============================================================

ALTER TABLE policy_basis ADD COLUMN source_url TEXT;
ALTER TABLE policy_basis ADD COLUMN source_org TEXT;
ALTER TABLE policy_basis ADD COLUMN source_type TEXT NOT NULL DEFAULT 'official';
ALTER TABLE policy_basis ADD COLUMN last_verified_at TEXT;
ALTER TABLE policy_basis ADD COLUMN verification_status TEXT NOT NULL DEFAULT 'unverified';
ALTER TABLE policy_basis ADD COLUMN verification_note TEXT;

CREATE INDEX IF NOT EXISTS idx_pb_verification_status ON policy_basis(verification_status);
CREATE INDEX IF NOT EXISTS idx_pb_last_verified_at ON policy_basis(last_verified_at);
