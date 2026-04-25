# TASKS_PROGRESS.md

> 更新：2026-04-23
> 口径说明：本文件用于记录“当前真实状态”和“下一步优先事项”，不再作为乐观交接摘要使用。
> 事实源优先级：数据库与质量报告 > `ROADMAP.md` > 本文件

---

## 当前真实状态

根据当前数据库与最近一次检查，项目处于以下状态：

### 数据规模

| 指标 | 当前值 |
|------|--------|
| 问题总数 | **724** |
| 政策总数 | **102** |
| 问题-政策关联 | **1300** |
| 问题-问题关联 | **3016** |
| 地方口径 | **3** |

### 结构缺口

| 缺口项 | 当前值 |
|--------|--------|
| 缺适用条件 | **0** |
| 缺例外与边界 | **0** |
| 缺实务处理步骤 | **0** |
| 缺风险提示 | **0** |
| 缺业务标签 | **0** |
| 缺更新记录 | **0** |
| 缺关联问题 | **0** |

> 注：
> 本轮已完成三类基础回填：标签缺口 `164 -> 0`、更新记录缺口 `153 -> 0`、结构字段缺口 `227 -> 0`。
> 高频问题密度补强已推进 4 批：高频标签缺口 `12 -> 0`、高频关联缺口 `12 -> 0`、高频政策 `<2` 缺口 `73 -> 0`。
> `quality_report_20260423.txt` 当前 17 项检查全部通过，检查 15 已改为“长期未复审内容”口径，不再误报刚导入但未满 1 年的内容。
> `ETAX` 模块已扩充至 6 个阶段全覆盖，阶段 × 模块矩阵空槽已从 `2` 个重点缺口扩大治理为 `0` 个空槽。
> 本轮已继续补入 `questions_batch33` ~ `questions_batch38`，把全矩阵最低组合厚度从 `1` 条提升到 `3` 条，并对首次办税、日常巡检、停业不断档、清税退回整改四条主线做了专题簇扩写。
> 已完成一轮高频问题上线前 agent 复核：统一 `23` 条 legacy 稳定度枚举、归档 `6` 条重复高频题，高频问题总数收口为 `143`，重复高频标题组数为 `0`，详见 `data/reports/hf_prelaunch_review_20260422.md`。
> 本轮已继续导入 `questions_batch39_topic_cluster_expand_importable.json` 共 `20` 条，活跃问题总数提升到 `638`，新增覆盖设立、经营、风险、停业、注销五条主线的专题簇问题。
> 本轮继续导入 `questions_batch40_change_suspend_close_expand_importable.json` 与 `questions_batch41_change_ops_suspend_expand_importable.json`，活跃问题总数进一步提升到 `654`，重点加厚了变更期专题簇、经营期发票/申报边界题、停业-注销衔接题与注销后追溯责任题。
> 本轮继续导入 `questions_batch42_change_tax_suspend_expand_importable.json`，活跃问题总数提升到 `659`，进一步补齐了变更期个税/清尾衔接、经营期税务综合边界，以及停业复业前申报判断题。
> 本轮继续导入 `questions_batch43_thin_combo_round2_importable.json` 与 `questions_batch44_thin_combo_expand_importable.json` 共 `24` 条，活跃问题总数提升到 `683`，进一步加厚了设立/风险/停业/注销四条主线下原本仅 `3` 条的薄组合，并新增了清算亏损、异常解除后注销、停业补发工资、停业退预收款等高频边界题。
> 本轮继续导入 `questions_batch45_low_combo_round3_importable.json` 共 `21` 条，活跃问题总数提升到 `704`，继续把变更、注销、风险、设立等低位组合从 `4` 条抬到 `5` 条，并补入了变更期认定交叠、注销前最后一期增值税、优惠异常首轮自查、新设首登电子税务局等高频入口题。
> 本轮继续导入 `questions_batch46_low_combo_round4_importable.json` 共 `12` 条，活跃问题总数提升到 `716`，把上一轮仍停在 `4` 条的 `CLS/FEE`、`SET/RISK`、`SET/TAX` 与整组 `SUS/*` 组合抬升到至少 `5` 条，新增了停业期补税争议、停业期补发年终奖、停业期客户补票、复业前优惠资料复核等高频衔接题。
> 本轮继续导入 `questions_batch47_low_combo_round5_importable.json` 共 `20` 条，活跃问题总数提升到 `736`，把 `CHG/*`、`CLS/*` 与 `OPR/ETAX` 这一层的低位组合继续抬升到至少 `6` 条，新增了变更后旧损失资料承接、注销前预收款清算、清税前导出清单自查、注销后历史风险回冒与经营期单模块电子税务局报错排查等专题题。
> 本轮新增一次性补量脚本 `scripts/content/generate_batch48_to_1000.py`，生成并导入 `questions_batch48_to_1000_importable.json` 共 `264` 条，活跃问题总数达到 `1000`。本轮按阶段 × 模块最低厚度优先分配，当前矩阵最低组合厚度已提升到 `10`，高频问题提升到 `312` 条。
> 本轮同步修正质量巡检脚本对 `certain_condition` / `certain_conditional` 的兼容口径，并修正列表页稳定度 badge 对 `certain_condition` 的样式兼容。
> 本轮继续使用同一生成脚本生成并导入 `questions_batch49_to_2000_importable.json` 共 `1000` 条，活跃问题总数达到 `2000`。当前阶段 × 模块矩阵最低组合厚度已提升到 `25`，高频问题提升到 `843` 条；`quality_report_20260423.txt` 17 项巡检继续全部通过。
> 随后按“不要低质量凑数”的上线口径完成全库内容审计，归档 `1264` 条模板化补量题，详见 `data/reports/template_padding_archive_20260423.md`；再归档 `12` 条重复题并修正 `6` 条截断标题，详见 `data/reports/hard_content_findings_cleaned_20260423.md`。清洗后 active 问题数为 `724`，模板化补量 active 残留为 `0`，`quality_report_20260423.txt` 已改为 active 口径并通过 17 项巡检。
> `active_content_quality_audit_20260423.md` 显示剩余 active 内容仍有 `122` 条详细解答偏短、`23` 条适用条件偏短、`3` 条风险提示偏短、`1` 条实务步骤偏短。这些不是模板凑数，但应作为下一轮人工/专题扩写优先队列。
> 本轮响应“税务政策变化快，必须联网核验”的要求，已为 `policy_basis` 增加官方来源与核验字段，并新增 `scripts/content/verify_policy_sources_batch1.py`、`scripts/content/full_policy_review_round1.py`、`scripts/content/full_policy_review_round2.py`、`scripts/content/audit_policy_verification.py`、`scripts/content/policy_launch_gate.py`。全库 `102` 条政策均已脱离 `unverified`，当前状态为：`source_found 52`、`needs_update 21`、`source_pending 22`、`manual_local_review 7`。active 引用政策仍有 `26` 条缺官方 `source_url`；受 `needs_update` 政策影响的 active 问题为 `206` 条；若按上线门禁同时纳入 `source_pending` 和 `manual_local_review`，则当前阻断 `337` 条 active 问题，其中高频 `108` 条。详见 `data/reports/full_policy_review_round1_20260423.md`、`data/reports/full_policy_review_round2_20260423.md`、`data/reports/policy_verification_audit_20260423.md`、`data/reports/policy_verification_blockers_20260423.txt`。不能宣称全库答案已复核通过。

---

## 当前阶段判断

当前项目不应再理解为“多个后续阶段都已完成”。

更准确的判断是：

- 数据底座：已完成
- 网站最小可用闭环：已完成
- 录入原型：已存在
- 导出预留：已存在
- 当前主任务：**统一口径、补结构质量、补覆盖短板、强化维护闭环**

---

## 当前最需要优先解决的问题

### P0：口径统一

- `README.md`、旧交接状态与数据库真实状态不一致
- 枚举值在数据库、模板、表单之间不完全一致
- 页面查询与 API 查询口径不完全一致
- 页面搜索与 API 搜索逻辑不完全一致

### P1：结构质量

- active 内容的四个核心结构字段已全部补齐
- 低风险基础缺口（业务标签、更新记录、关联问题）已完成回填
- 政策依据已开始进入联网核验阶段：首批完成官方来源打标，但大多数 active 引用政策仍未完成来源补齐和答案级复核
- 政策上线门禁已启用：`python scripts/content/policy_launch_gate.py` 当前返回 FAIL，阻断项必须清零后才能进入正式上线口径
- 当前已新增批量补强脚本 `backfill_structured_fields_batch1.py`、`backfill_structured_fields_batch2.py`、`backfill_structured_fields_batch3.py`、`backfill_structured_fields_batch4.py`、`backfill_structured_fields_batch5.py`、`backfill_structured_fields_batch6.py`、`backfill_structured_fields_batch7.py`、`backfill_structured_fields_batch8.py`、`backfill_structured_fields_batch9.py`、`backfill_structured_fields_batch10.py`、`backfill_structured_fields_batch11.py`、`backfill_structured_fields_batch12.py`、`backfill_structured_fields_batch13.py`、`backfill_structured_fields_batch14.py`、`backfill_structured_fields_batch15.py`、`backfill_structured_fields_batch16.py`、`backfill_structured_fields_batch17.py`、`backfill_structured_fields_batch18.py`、`reinforce_high_frequency_batch1.py`、`reinforce_high_frequency_batch2.py`、`reinforce_high_frequency_batch3.py`、`reinforce_high_frequency_batch4.py`
- 高频问题已完成一轮 agent 复核收口，但正式上线前的人审签收仍未完成
- 下一批重点不再是结构补洞，而是转向内容复审、重点专题成组扩写、以及维护节奏固化

### P2：覆盖短板

- ETAX 模块的阶段覆盖已补齐
- 阶段 × 模块矩阵已无空槽，清洗后最低组合厚度为 `5`
- 当前覆盖短板已不再是“有没有”，而是“同一专题下是否形成入口题、流程题、边界题、风险题的成组结构”
- 本轮已对 `SET/REG`、`SET/INV`、`SET/DEC`、`OPR/ETAX`、`OPR/REG`、`RSK/DEC`、`RSK/ETAX`、`SUS/ETAX`、`SUS/RISK`、`CLS/ETAX`、`CLS/CLEAR` 追加专题簇内容
- 本轮继续把 `SET/ETAX`、`SET/REG`、`SET/DEC`、`SET/IIT`、`SET/SSF`、`OPR/DEC`、`OPR/INV`、`OPR/FEE`、`OPR/IIT`、`OPR/ETAX`、`RSK/RISK`、`RSK/ETAX`、`RSK/DEC`、`SUS/ETAX`、`SUS/TAX`、`SUS/RISK`、`CLS/ETAX`、`CLS/CLEAR` 再做一轮增量扩充
- 本轮继续把 `CHG/REG`、`CHG/DEC`、`CHG/INV`、`CHG/RISK`、`CHG/TAX`、`OPR/DEC`、`OPR/FEE`、`OPR/INV`、`SUS/REG`、`SUS/CLEAR`、`CLS/RISK` 做了变更与停业-注销衔接专题补强
- 本轮继续把 `CHG/IIT`、`CHG/CLEAR`、`OPR/TAX`、`SUS/DEC` 做了补量和边界题扩展
- 本轮继续把 `CLS/CIT`、`CLS/FEE`、`CLS/REG`、`CLS/VAT`、`RSK/CLEAR`、`RSK/INV`、`RSK/REG`、`SET/CIT`、`SET/CLEAR`、`SET/RISK`、`SET/TAX`、`SUS/CIT`、`SUS/FEE`、`SUS/IIT`、`SUS/PREF`、`SUS/SSF`、`SUS/VAT` 从“单组合 3 条”继续抬升到至少 `4` 条
- 本轮继续把 `CHG/CIT`、`CHG/DEC`、`CHG/ETAX`、`CHG/FEE`、`CHG/IIT`、`CHG/INV`、`CHG/RISK`、`CLS/DEC`、`CLS/IIT`、`CLS/PREF`、`CLS/TAX`、`CLS/VAT`、`RSK/CIT`、`RSK/INV`、`RSK/PREF`、`RSK/REG`、`SET/CIT`、`SET/CLEAR`、`SET/ETAX`、`SET/SSF`、`SET/VAT` 从“单组合 4 条”继续抬升到至少 `5` 条
- 本轮继续把 `CLS/FEE`、`SET/RISK`、`SET/TAX`、`SUS/CIT`、`SUS/FEE`、`SUS/IIT`、`SUS/INV`、`SUS/PREF`、`SUS/REG`、`SUS/SSF`、`SUS/TAX`、`SUS/VAT` 从“单组合 4 条”继续抬升到至少 `5` 条
- 本轮继续把 `CHG/CIT`、`CHG/DEC`、`CHG/ETAX`、`CHG/FEE`、`CHG/IIT`、`CHG/INV`、`CHG/RISK`、`CLS/CIT`、`CLS/DEC`、`CLS/ETAX`、`CLS/FEE`、`CLS/IIT`、`CLS/INV`、`CLS/PREF`、`CLS/REG`、`CLS/RISK`、`CLS/SSF`、`CLS/TAX`、`CLS/VAT`、`OPR/ETAX` 从“单组合 5 条”继续抬升到至少 `6` 条
- 本轮继续通过 `questions_batch48_to_1000_importable.json` 把全矩阵最低组合厚度抬升到至少 `10` 条
- 本轮继续通过 `questions_batch49_to_2000_importable.json` 把全矩阵最低组合厚度抬升到至少 `25` 条
- 本轮已将 `questions_batch48_to_1000_importable.json` 和 `questions_batch49_to_2000_importable.json` 中的模板化补量题全部归档，不再计入 active 覆盖厚度
- 后续应从“按模块平均补点”转向“围绕设立、变更、停业、注销、风险处置五类高频专题继续做入口题、流程题、边界题、风险题的成组扩写”
- 高频链路仍需按“入口问题 + 流程问题 + 边界问题 + 风险问题”继续打磨

### P3：维护闭环

- 新建/编辑功能仍偏原型化
- 政策关联、更新记录、地方口径的维护闭环仍需增强
- 政策依据维护新增强制队列：运行 `audit_policy_verification.py`，优先处理 `needs_update` 和 active 引用量最高的 `unverified` 政策
- 草稿 / 待复核 / 启用状态流转仍需继续规范

---

## 下一步执行顺序

后续 agent 应按以下顺序推进，不得反过来：

1. 统一事实源与枚举口径
2. 修正页面、API、表单、脚本分叉
3. 补结构字段、标签、更新记录、关联问题
4. 按组合专题继续扩写薄弱覆盖
5. 强化录入、巡检、测试守门
6. 最后再推进 AI 检索 contract 和部署闭环

详细路线以 [ROADMAP.md](ROADMAP.md) 为准。

---

## 对后续 agent 的提醒

- 不要再把本项目当作“从零搭原型”
- 也不要再把本项目当作“后续阶段已经基本完成”
- 做任何修改前，必须先读：
  1. `PROJECT_MANIFEST.md`
  2. `ROADMAP.md`
  3. `AGENTS.md`

如果当前任务与旧文档中的“已完成”状态冲突：

- 优先相信数据库
- 优先相信质量报告
- 优先相信 `ROADMAP.md`
