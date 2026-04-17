# TASKS.md

## 1. 文件目的

本文件用于将"企业全生命周期税务问题知识库网站"项目拆解为可执行、可跟踪、可逐步验收的任务清单。

本任务清单遵循以下原则：

- 先搭底座，再做展示
- 先做结构，再做规模
- 先做最小可用闭环，再做高级能力
- 先保证可维护，再追求复杂功能
- 先把问题卡片、政策依据、标签、搜索这条主线打通

本文件适用于：
- agent 执行开发任务
- 人工检查当前进度
- 后续逐阶段验收项目完成情况

---

## 2. 阶段总览

| Phase | 名称 | 状态 |
|-------|------|------|
| Phase 0 | 项目基础文件与规范 | ✅ 已完成 |
| Phase 1 | 数据库与数据底座 | ✅ 已完成 |
| Phase 2 | 示例数据与内容模型验证 | ✅ 已完成 |
| Phase 3 | 后端读取能力 / 数据访问层 | ✅ 已完成 |
| Phase 4 | 网站最小可用前端 | ✅ 已完成 |
| Phase 5 | 检索、筛选与关联问题增强 | ✅ 已完成 |
| Phase 6 | 内容录入与维护便利化 | ✅ 已完成 |
| Phase 7 | 地方口径、更新机制与专业增强 | ✅ 已完成 |
| Phase 8 | AI 检索与高级能力预留 | 🔲 待完成（导出就绪，数据就绪） |

---

## 3. Phase 0：项目基础文件与规范

### 目标
建立项目的统一目标、结构、执行规则和内容标准。

### 任务
- [x] 建立 `README.md`
- [x] 建立 `AGENTS.md`
- [x] 建立 `TASKS.md`
- [x] 建立 `CONTENT_SPEC.md`
- [x] 明确项目目录结构
- [x] 明确数据库选型（默认 SQLite）
- [x] 明确问题编号规则
- [x] 明确生命周期阶段字典
- [x] 明确主题模块字典
- [x] 明确状态、稳定度、更新类型等字典

### 验收标准
- 项目说明文件齐全
- agent 可仅凭文档理解项目目标
- 后续建表和内容录入有统一标准

---

## 4. Phase 1：数据库与数据底座 ✅

### 目标
完成底层数据结构，确保知识库可以被结构化存储、查询和扩展。

### 必做任务

#### 4.1 核心表设计
- [x] 创建 `question_master`
- [x] 创建 `policy_basis`
- [x] 创建 `question_policy_link`
- [x] 创建 `tag_dict`
- [x] 创建 `question_tag_link`
- [x] 创建 `question_update_log`

#### 4.2 推荐扩展表
- [x] 创建 `question_relation`
- [x] 创建 `local_rule_note`

#### 4.3 字典表或约束
- [x] 实现生命周期阶段字典
- [x] 实现主题模块字典
- [x] 实现问题类型字典
- [x] 实现结论稳定度字典
- [x] 实现条目状态字典
- [x] 实现政策层级字典
- [x] 实现依据支撑类型字典
- [x] 实现更新类型字典

#### 4.4 约束与索引
- [x] 为 `question_code` 建唯一约束
- [x] 为问题表关键检索字段建索引
- [x] 为关联表外键建索引
- [x] 为更新时间字段建索引
- [x] 为高频标记、新手标记建必要索引
- [x] 为标签关联关系建复合索引
- [x] 为地区字段建必要索引

#### 4.5 初始化脚本
- [x] 输出完整建表 SQL
- [x] 输出初始化字典 SQL
- [x] 输出示例数据 SQL
- [x] 输出常用查询 SQL 示例

### 验收标准
- [x] 所有核心表可正常创建
- [x] 外键关系合理
- [x] 索引基本齐全
- [x] 示例数据可成功插入
- [x] 常用查询可运行

---

## 5. Phase 2：示例数据与内容模型验证

### 目标
用真实风格的税务问题验证数据结构和内容模板是否可用。

### 任务

#### 5.1 首批示例问题
至少录入以下方向的问题：
- [x] 企业刚设立，还没经营，要不要申报？(SET-REG-001)
- [x] 企业没有收入，是否必须申报？（同 SET-REG-001，覆盖"无收入/未经营"场景）
- [x] 零申报和未申报有什么区别？(OPR-DEC-001)
- [x] 企业变更地址后税务上还要做什么？(OPR-CHG-001)
- [ ] 退款后是否就不用开发票？

#### 5.2 示例政策依据
- [x] 为每个问题挂接至少 1～3 条政策依据
- [x] 填写政策名称、文号、条款位置、政策层级、状态
- [x] 写明每条依据支撑的是哪个结论

#### 5.3 标签与关联
- [x] 为示例问题打标签
- [x] 建立至少一组关联问题
- [x] 建立至少一条更新记录

#### 5.4 内容字段验证
检查是否所有字段都能承载以下内容：
- [x] 一句话结论
- [x] 详细解答
- [x] 核心定义
- [x] 适用条件
- [x] 例外与边界
- [x] 实务处理步骤
- [x] 风险提示
- [x] 适用地区
- [x] 结论稳定度

### 验收标准
- [x] 至少有一批完整、像样的示例问题
- [x] 示例数据不是占位符式伪内容
- [x] 数据结构能覆盖实际问题写作需要
- [x] 不需要大改表结构即可继续扩容

---

## 6. Phase 3：后端读取能力 / 数据访问层 ✅

### 目标
建立清晰、可维护的数据读取方式，为前端页面提供稳定数据来源。

### 任务
- [x] 明确项目使用的后端方式（Flask + question_service.py，数据访问层分离）
- [x] 实现问题列表读取
- [x] 实现问题详情读取
- [x] 实现政策依据联表读取
- [x] 实现标签读取
- [x] 实现更新记录读取
- [x] 实现关联问题读取
- [x] 实现按阶段筛选
- [x] 实现按模块筛选
- [x] 实现按标签筛选
- [x] 实现基础搜索

### 推荐接口能力
- [x] `get_questions` → `list_questions()`
- [x] `get_question_detail` → `get_question_detail()`
- [x] `get_question_policies` → 集成在 `get_question_detail()` 中
- [x] `get_questions_by_stage` → `list_questions(stage=)`
- [x] `get_questions_by_module` → `list_questions(module=)`
- [x] `get_questions_by_tag` → `list_questions(tag=)`
- [x] `search_questions` → `list_questions(keyword=)`
- [x] `get_recent_updates` → 集成在 `get_question_detail()` 中

### 验收标准
- [x] 前端无需直接写复杂 SQL
- [x] 数据访问逻辑清楚
- [x] 核心查询可复用
- [x] 返回结构适合页面展示

---

## 7. Phase 4：网站最小可用前端 ✅

### 目标
做出一个真正可浏览、可查询的知识库网站原型。

### 必做页面

#### 7.1 首页
- [x] 搜索框
- [x] 生命周期阶段入口
- [x] 主题模块入口
- [x] 高频问题入口
- [x] 新手必看入口
- [x] 最近更新入口

#### 7.2 问题列表页
- [x] 显示问题标题
- [x] 显示一句话结论摘要
- [x] 显示标签
- [x] 显示更新时间
- [x] 显示高频 / 新手标记
- [x] 支持分页或分段加载

#### 7.3 问题详情页
- [x] 显示问题标题
- [x] 显示一句话结论
- [x] 显示详细解答
- [x] 显示核心定义
- [x] 显示适用条件
- [x] 显示例外与边界
- [x] 显示实务处理步骤
- [x] 显示风险提示
- [x] 显示政策依据
- [x] 显示标签
- [x] 显示适用地区
- [x] 显示关联问题
- [x] 显示更新记录

### 页面体验要求
- [x] 信息层次清晰
- [x] 默认先突出问题和结论
- [x] 政策依据可折叠或分区显示
- [x] 页面结构稳定，不做过度装饰

### 验收标准
- [x] 网站能真正浏览和查问题
- [x] 核心页面完整可用
- [x] 问题卡片展示逻辑成立
- [x] 用户可以从列表进入详情，再跳转关联问题

---

## 8. Phase 5：检索、筛选与关联问题增强 ✅

### 目标
提升知识库作为"查问题工具"的效率。

### 任务

#### 8.1 搜索增强
- [x] 支持标题搜索
- [x] 支持关键词搜索
- [x] 支持模糊匹配
- [ ] 支持同义表达扩展（后续可增强）

#### 8.2 筛选增强
- [x] 按生命周期阶段筛选
- [x] 按主题模块筛选
- [x] 按标签筛选
- [x] 按是否高频筛选
- [x] 按是否新手必看筛选
- [x] 按地区筛选（使用 scope_level 字段：全国/省级/地方）
- [x] 按状态筛选（active/draft/archived，默认只看 active）

#### 8.3 关联问题增强
- [x] 在详情页展示关联问题列表
- [ ] 支持不同关联类型（当前只有 related，Phase 7 扩展）
- [x] 优化关联问题排序
- [x] 支持"下一步推荐问题"（基于同一 module + 下一 stage 的自动推荐）

### 验收标准
- [x] 用户无需精确知道标题，也能找到问题
- [x] 从一个问题能自然跳到相邻问题
- [x] 知识库开始具备路径式使用体验

---

## 9. Phase 6：内容录入与维护便利化 ✅

### 目标
降低新增问题和更新问题的维护成本。

### 任务
- [x] 设计标准化录入流程
- [x] 提供最小录入表单
- [x] 支持新建问题
- [x] 支持编辑问题（`/question/<code>/edit` 路由 + `edit_question.html` 模板）
- [x] 支持绑定政策依据（最多3条，支撑类型+说明）
- [ ] 支持新增标签（需直接操作数据库，当前可通过编辑表单已有标签）
- [x] 支持写入更新记录（新建时自动写入）
- [x] 支持修改状态（编辑表单中 status 下拉框）
- [ ] 支持维护关联问题（需手动在 question_relation 表维护）

### 验收标准
- [x] 新增一条问题不需要手改多个文件
- [x] 更新一条问题的成本可接受（编辑功能已实现）
- [x] 内容维护更接近"填表"而不是"写代码"

---

## 10. Phase 7：地方口径、更新机制与专业增强 ✅

### 目标
提升知识库的专业完整性和长期可信度。

### 任务

#### 10.1 地方口径
- [x] 建立地方口径展示区（黄色高亮卡片）
- [x] 支持问题挂接地区补充说明
- [x] 区分全国规则与地方执行差异（全国规则显示scope-note，地方单独显示）

#### 10.2 更新机制
- [x] 完善更新日志展示（带版本号v1/更新类型/更新原因/变更摘要/审核人）
- [x] 支持版本号展示（顶部badge + 底部footer）
- [x] 支持更新原因展示
- [x] 支持条目状态变化展示（状态badge：active/draft/archived）

#### 10.3 专业增强
- [x] 增加结论稳定度展示（4色标签：明确/有条件/有争议/实务做法）
- [x] 增加争议问题标识（红色dispute标签）
- [x] 优化政策依据展示逻辑（按direct/procedure/other分组，彩色左边框区分）
- [x] 优化"直接依据/辅助依据/办理依据"等类型展示（分组+support_type标签）

### 验收标准
- [x] 网站不只是"能看"，还更"可信"
- [x] 可清楚区分通用规则与地方差异
- [x] 可识别哪些问题结论稳定，哪些问题需结合条件判断

---

## 11. 枚举口径统一与数据校准 ✅

**触发原因**：Phase 3/4/6 迭代中枚举定义分散在 seed 文件、前端模板、脚本常量三处，存在拼写错误、历史遗留值和跨层不一致。

**枚举现状（2026-04-17 核查后）**：

| 枚举字段 | 标准值 | 说明 |
|---|---|---|
| `scope_level` | `scope_national` / `scope_local` / `scope_mixed` | `scope_provincial` 已清除（前端冗余选项，从未入DB） |
| `question_type` | `type_whether` / `type_how` / `type_define` / `type_risk` / `type_time` / `type_what` / `type_why` | seed/DB/前端三方对齐 |
| `answer_certainty` | `certain_clear` / `certain_conditional` / `certain_dispute` / `certain_practice` | 正确拼写：`certain_conditional`（有al），历史错误 `certain_condition` 已全量修正 |
| `status` | `status_draft` / `status_active` / `status_pending` / `status_obsolete` / `status_archived` | DB全为`status_active`（设计态），表单保留`draft`选项 |
| `support_type` | `support_direct` / `support_procedure` / `support_definition` / `support_risk` / `support_local` / `support_aux` | 中文错误值已迁入`support_note`，类型列恢复规范值 |
| `policy_level` | `level_law` / `level_admin` / `level_department` / `level_bulletin` / `level_local` | seed/DB统一使用`level_*`前缀 |
| `current_status` | `pol_effective` / `pol_partial` / `pol_expired` / `pol_replaced` / `pol_uncertain` | DB历史混用`active`/`effective`/`pol_effective`，已统一为`pol_effective` |
| `relation_type` | `related` / `next_step` / `prerequisite` / `similar` / `see_also` | ✅ 本来一致 |
| `update_type` | `update_new` / `update_revise` / `update_policy` / `update_boundary` / `update_local` / `update_status` | DB历史混用`create`/`update`/`update_new`/`update_revise`，已统一为seed标准值 |
| `tag_category` | `business` / `module` / `stage` / `policy_level` / `policy_status` / `question_type` / `scope_level` / `answer_certainty` / `support_type` / `update_type` / `status` | `business_tag`已并入`business` |

**修复记录**：

DB运行数据修正（5条UPDATE，影响150+54+218条记录）：
- `question_policy_link.support_type`：55条中文值（`直接适用`/`责任认定依据`/`前置审批依据`）迁入`support_note`，类型列恢复规范值
- `question_update_log.update_type`：`create`(136)+`update`(1) → `update_new`；`update_revise`不变
- `tag_dict.tag_category`：`business_tag`(8条) → `business`
- `policy_basis.policy_level`：中文值 → `level_*`前缀（5类全覆盖，49条）
- `policy_basis.current_status`：`active`(35)+`effective`(12) → `pol_effective`

Seed文件修正（4个文件）：`certain_condition`(无al) → `certain_conditional`

前端模板修正（4个文件）：`certainty_label`宏拼写 + `type_risk`分支补全 + `scope_provincial`冗余选项删除

脚本修正（2个文件）：`quality_report.py`补`scope_mixed`+certainty拼写；`export_for_ai.py`补`scope_mixed`标签映射

**维护规范**：
- 新增枚举值时：同时更新seed文件 + 前端模板下拉选项 + `quality_report.py`的`VALID_*`集合
- 不得在DB枚举列写入中文描述性文本（应写入`support_note`等说明字段）
- 字段命名使用`snake_case`，枚举值使用`type_*`/`scope_*`/`status_*`/`level_*`前缀

**验收标准**：
- [x] DB所有枚举列无中文值
- [x] seed/DB/前端三层的枚举值完全一致
- [x] `quality_report.py`运行无P1/P2级枚举警告
- [x] 枚举拼写错误全部修正（`certain_condition` → `certain_conditional`）
- [x] `scope_provincial`从所有代码文件中清除

---

## 12. Phase 8：AI 检索与高级能力预留

### 目标
为未来 AI 检索、语义搜索、相似问题推荐打基础。

### 当前不强制实现，但应预留的内容
- [x] 问题文本结构适合切片
- [x] 字段足够结构化
- [x] 关键词维护较完整
- [x] 标签体系清晰
- [x] 关联问题逻辑清晰
- [x] 问题与依据可追溯

### 未来可做任务
- [ ] 全文检索
- [ ] 相似问题推荐
- [ ] 语义搜索
- [ ] 向量索引
- [ ] 基于底库引用式 AI 回答

### 验收标准
- 当前结构不会阻碍未来 AI 能力接入
- 不需要推翻数据库模型即可扩展

---

## 12. 内容建设任务清单（持续执行）

### 高优先级问题群
- [ ] 设立后首次涉税事项
- [ ] 无收入 / 未经营 / 零申报
- [ ] 发票领用与开具
- [ ] 普票 / 专票 / 红字发票
- [ ] 个税代扣代缴基础问题
- [ ] 社保费基础问题
- [ ] 成本费用与凭证取得
- [ ] 变更登记后税务处理
- [ ] 风险预警与异常处理
- [ ] 注销清税常见问题

### 内容质量检查项
- [ ] 标题像真实提问
- [ ] 一句话结论清楚
- [ ] 详细解答能说明逻辑
- [ ] 定义不缺失
- [ ] 适用条件明确
- [ ] 例外与边界明确
- [ ] 风险提示明确
- [ ] 依据可追溯
- [ ] 标签合理
- [ ] 更新时间完整

---

## 13. 当前推荐的最小可用里程碑

### Milestone 1：数据库完成 ✅
- [x] 建表
- [x] 建索引
- [x] 插入字典数据

### Milestone 2：示例内容完成 ✅
- [x] 至少 5 条完整问题
- [x] 至少 5 条依据
- [x] 至少 5 组标签关联

### Milestone 3：原型可浏览 ✅
- [x] 首页完成
- [x] 列表页完成
- [x] 详情页完成

### Milestone 4：可检索 ✅
- [x] 搜索可用
- [x] 标签筛选可用
- [x] 阶段/模块筛选可用

### Milestone 5：可扩展 ✅
- [x] 录入新问题成本可接受
- [x] 关联问题展示可用
- [x] 更新记录可展示

---

## 14. 最终执行提醒

### 必须始终记住
- 这是"问题卡片网站"，不是文章博客
- 这是"结构化知识工程"，不是随手答复库
- 这是"长期会增长的系统"，不是一次性交付页面
- 这是"以政策为依据的知识产品"，不是纯 AI 生成问答

### 一句话任务主线
1. [x] 先做稳数据库
2. [ ] 再做通页面
3. [ ] 再做强检索
4. [ ] 再做方便维护
5. [ ] 再做 AI 增强
