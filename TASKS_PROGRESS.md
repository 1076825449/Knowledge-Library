# 企业税务知识库 - 交接摘要

> 更新：2026年4月17日
> 数据库：/Volumes/外接硬盘/vibe coding/网站/知识库/database/db/tax_knowledge.db

---

## 当前数据规模

| 指标 | 数值 |
|------|------|
| 问题总数 | **281条** |
| 政策总数 | **102条** |
| 问题-问题关联 | **800条** |
| 问题-政策关联 | **424条** |
| pytest | **71 passed** |

---

## 各模块详情

| 模块 | 问题 | 关系覆盖率 | 政策引用率 |
|------|------|-----------|-----------|
| REG | 43 | 100% | 100% |
| RISK | 48 | 100% | 100% |
| DEC | 34 | 100% | 100% |
| INV | 23 | 100% | 100% |
| PREF | 20 | 100% | 100% |
| CIT | 18 | 100% | 100% |
| FEE | 17 | 100% | 100% |
| IIT | 17 | 100% | 100% |
| VAT | 16 | 100% | 100% |
| SSF | 12 | 100% | 100% |
| TAX | 12 | 100% | 100% |
| CLEAR | 21 | 100% | 100% |
| **全局** | **281** | **100%** | **100%** |

---

## 本次批量操作记录（2025年 月 日）

### T3.2 RSK模块扩容
- 新增8条问题：RSK-SUS-006(滞纳金计算)、RSK-SUS-007(善意取得虚开发票维权)、RSK-IIT-002(代扣代缴处罚)、RSK-RISK-011(双随机检查)、RSK-SSF-002(社保费风险)、RSK-CIT-003(优惠不合规补缴)、RSK-TAX-004(非正常户个人责任)、RSK-RISK-012(一案双查)

### T3.3 其他模块扩容
- 新增FEE×5：OPR-FEE-007~010、CHG-FEE-001(补)、CLS-FEE-001(补)
- 新增IIT×2：RSK-IIT-005(股权激励)、OPR-IIT-012(外籍员工补贴)
- 新增SSF×2：OPR-SSF-008(跨省社保)、OPR-SSF-009(退休返聘)
- 新增TAX×4：OPR-TAX-005~008

### T4 政策补强
- 新增政策13条入库（TAX-POL-001~008、SSF-POL-001~002、IIT-POL-001~002、CLEAR-POL-001）
- 孤立政策18条关联到已有问题（18条全部完成）
- 新政策→19条无引用问题（全部完成）

---

## 字段规范提醒

### question_policy_link 表
- **字段**：id / question_id / policy_id / support_type(='citation') / support_note / display_order
- **注意**：不是 section_quote / created_at

### policy_basis 表
- **字段**：id / policy_code / policy_name / document_no / article_ref / policy_level / effective_date / **expiry_date** / current_status / policy_summary / raw_quote_short / region_scope / remarks / created_at / updated_at
- **注意**：不是 expiration_date，没有 source_url 字段

---

## 未完成/待扩展项

1. **7条未关联政策**：地方裁量基准(广东/上海各1)及通用申报公告(4条)暂时没有合适的具体问题对应，待业务场景扩展时自然覆盖
2. **T5 尚未启动**：如需继续扩容，方向包括CIT非居民细分场景、VAT申报细节深化等
3. **CI/CD**：GitHub Actions CI已配置（.github/workflows/ci.yml），每次push自动跑pytest
4. **Git提交**：本次批量操作尚未提交Git，建议在测试服务器确认无误后手动提交

---

## 快速验证命令

```bash
cd "/Volumes/外接硬盘/vibe coding/网站/知识库"
python3 -m pytest tests/ -q

# 启动Flask
cd "/Volumes/外接硬盘/vibe coding/网站/知识库" && python backend/app.py
```
