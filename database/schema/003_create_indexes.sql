-- ============================================================
-- 文件：003_create_indexes.sql
-- 描述：创建所有索引
-- 执行顺序：第3步（在表创建后执行）
-- ============================================================

-- ===== question_master 索引 =====
CREATE INDEX IF NOT EXISTS idx_qm_stage_code     ON question_master(stage_code);
CREATE INDEX IF NOT EXISTS idx_qm_module_code    ON question_master(module_code);
CREATE INDEX IF NOT EXISTS idx_qm_question_type  ON question_master(question_type);
CREATE INDEX IF NOT EXISTS idx_qm_status         ON question_master(status);
CREATE INDEX IF NOT EXISTS idx_qm_scope_level    ON question_master(scope_level);
CREATE INDEX IF NOT EXISTS idx_qm_high_freq      ON question_master(high_frequency_flag);
CREATE INDEX IF NOT EXISTS idx_qm_newbie        ON question_master(newbie_flag);
CREATE INDEX IF NOT EXISTS idx_qm_updated_at     ON question_master(updated_at);

-- ===== policy_basis 索引 =====
CREATE INDEX IF NOT EXISTS idx_pb_policy_level    ON policy_basis(policy_level);
CREATE INDEX IF NOT EXISTS idx_pb_current_status ON policy_basis(current_status);
CREATE INDEX IF NOT EXISTS idx_pb_region_scope   ON policy_basis(region_scope);
CREATE INDEX IF NOT EXISTS idx_pb_policy_code    ON policy_basis(policy_code);
CREATE INDEX IF NOT EXISTS idx_pb_verification_status ON policy_basis(verification_status);
CREATE INDEX IF NOT EXISTS idx_pb_last_verified_at    ON policy_basis(last_verified_at);

-- ===== tag_dict 索引 =====
CREATE INDEX IF NOT EXISTS idx_td_tag_category  ON tag_dict(tag_category);
CREATE INDEX IF NOT EXISTS idx_td_parent_id     ON tag_dict(parent_id);

-- ===== question_policy_link 索引 =====
CREATE UNIQUE INDEX IF NOT EXISTS idx_qpl_unique    ON question_policy_link(question_id, policy_id, support_type);
CREATE INDEX IF NOT EXISTS idx_qpl_question_id     ON question_policy_link(question_id);
CREATE INDEX IF NOT EXISTS idx_qpl_policy_id       ON question_policy_link(policy_id);

-- ===== question_tag_link 索引 =====
CREATE UNIQUE INDEX IF NOT EXISTS idx_qtl_unique  ON question_tag_link(question_id, tag_id);
CREATE INDEX IF NOT EXISTS idx_qtl_question_id   ON question_tag_link(question_id);
CREATE INDEX IF NOT EXISTS idx_qtl_tag_id        ON question_tag_link(tag_id);

-- ===== question_update_log 索引 =====
CREATE INDEX IF NOT EXISTS idx_qul_question_id  ON question_update_log(question_id);
CREATE INDEX IF NOT EXISTS idx_qul_update_date  ON question_update_log(update_date);

-- ===== question_relation 索引 =====
CREATE UNIQUE INDEX IF NOT EXISTS idx_qr_unique    ON question_relation(question_id, related_id, relation_type);
CREATE INDEX IF NOT EXISTS idx_qr_question_id     ON question_relation(question_id);
CREATE INDEX IF NOT EXISTS idx_qr_related_id       ON question_relation(related_id);

-- ===== local_rule_note 索引 =====
CREATE INDEX IF NOT EXISTS idx_lrn_question_id  ON local_rule_note(question_id);
CREATE INDEX IF NOT EXISTS idx_lrn_region_code   ON local_rule_note(region_code);
