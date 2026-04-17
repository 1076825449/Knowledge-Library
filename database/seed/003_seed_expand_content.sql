-- =====================================================================
-- 扩充内容批次：企业全生命周期税务问题知识库
-- 覆盖：高优先级问题群（设立后首次涉税、无收入/零申报、发票、个税、社保、成本费用、变更、风险、注销）
-- =====================================================================

-- =====================================================================
-- SET-REG 系列：设立期 - 登记管理
-- =====================================================================

-- SET-REG-003: 设立后首次涉税事项
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'SET-REG-003',
    '企业刚领了营业执照，接下来税务上要办哪些事？',
    '公司刚注册完，营业执照已经拿到了，接下来还要办什么税务上的事？要不要马上去税务局？',
    'SET', 'REG', 'type_how',
    '领取执照后30日内需到税务局办理税务登记，发票申领根据业务需要申请，社保登记则通过社保平台办理。',
    '第一步：领取营业执照后30日内到主管税务机关办理税务登记，填报《税务登记表》。\n\n第二步：根据经营需要申请发票种类——如果客户需要增值税专用发票，需先完成一般纳税人登记；如果只是普通业务，可先申领增值税普通发票。\n\n第三步：到社保经办机构办理社保登记，即便暂时没有员工也需办理单位参保登记。\n\n第四步：到银行开立对公账户，并将账户信息报备给税务机关。\n\n第五步：按时进行纳税申报，即使没有收入也要进行零申报。',
    '税务登记：企业在领取营业执照后30日内向主管税务机关办理税务登记的法定程序。\n\n一般纳税人：年应税销售额超过规定标准的小规模纳税人，需办理一般纳税人登记，可抵扣进项税额。\n\n小规模纳税人：年应税销售额未超过规定标准的纳税人，征收率低（当前1%或3%），不可抵扣进项税额。',
    '适用于在市场监管部门领取营业执照后的各类企业。',
    '个体工商户和个人独资企业税务处理方式有所不同，需根据具体类型判断。\n\n从事特定行业（如危险化学品经营、食品销售）还需取得相应许可证后方可申请发票。',
    '步骤1：30日内到主管税务局办理税务登记\n步骤2：确定增值税纳税人身份（小规模或一般纳税人）\n步骤3：申请发票（普通发票/专用发票）\n步骤4：办理社保登记\n步骤5：开立对公账户并报备\n步骤6：设置账簿，进行会计核算\n步骤7：按时申报纳税',
    '未按期办理税务登记会被处以2000元以下罚款，情节严重的可处以2000元以上10000元以下罚款。\n\n取得营业执照后长期不办理税务登记，税务机关可认定为"非正常户"，影响企业信用。',
    'scope_national', NULL,
    'certain_clear', '设立 营业执照 税务登记 首次 办理流程 新公司',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- SET-REG-004: 设立后要开哪些账户
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'SET-REG-004',
    '新公司设立后，银行账户和税务账户要怎么处理？',
    '公司注册好了，是不是要去银行开户？税务这边有没有什么账户要办？',
    'SET', 'REG', 'type_how',
    '公司注册后需开立对公银行账户，并将开户信息报税务机关；税务上通过电子税务局进行申报，不需要单独开"税务账户"。',
    '一、银行账户\n新公司应当开立对公银行账户，用于：\n- 接收投资款\n- 日常经营收付款\n- 员工工资发放\n- 社保公积金扣款\n\n二、税务账户\n税务上没有独立的"账户"概念，但需要注意：\n- 银行账户信息需要在电子税务局中备案\n- 签订三方协议（企业-银行-税务局），用于电子扣税\n- 每个申报期通过电子税务局完成申报和缴款\n\n三、社会保险\n- 到社保经办机构办理单位参保登记\n- 在社保系统绑定银行托收账户',
    '三方协议：企业、商业银行、税务机关三方签订的扣款协议，用于实现电子缴税。\n\n对公银行账户：以企业名义在银行开立的账户，与个人账户严格区分。',
    '适用于所有新设立的企业。',
    '特殊行业（如外资企业、金融机构）可能有额外的账户管理要求。',
    '步骤1：选择商业银行开立对公账户\n步骤2：获取开户许可证或基本存款账户信息\n步骤3：登录电子税务局进行银行账户备案\n步骤4：签订银税三方协议\n步骤5：办理社保参保登记',
    '未备案银行账户或备案信息变更未及时更新，可能影响申报和缴款。\n\n对公账户与个人账户混用可能导致公司财产与个人财产混同，带来法律责任风险。',
    'scope_national', NULL,
    'certain_clear', '银行账户 对公账户 三方协议 税务备案 社保登记 新公司',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- SET-DEC 系列：设立期 - 申报纳税
-- =====================================================================

-- SET-DEC-002: 设立首月申报
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'SET-DEC-002',
    '公司刚成立，第一个月就要报税吗？',
    '公司4月份注册成立的，4月份要不要报税？还是从5月份开始报？',
    'SET', 'DEC', 'type_whether',
    '公司成立后次月起需要报税。4月成立，5月报4月的税（第一个申报期）。如果当月没有税务登记，则无需申报。',
    '一、什么时候开始报税？\n企业税务登记的当月，如果发生了应税行为，需要从次月开始申报。\n\n二、设立当月是否需要申报？\n- 如果在当月税务登记并领用了发票，发生了开票收入，则需要申报\n- 如果当月没有开票，也没有其他应税行为，通常无需申报\n\n三、常见申报税种：\n- 增值税（按月或按季）\n- 企业所得税（按季预缴）\n- 个人所得税（按月代扣代缴）\n- 城建税、教育费附加等（随增值税申报）\n\n四、小规模纳税人优惠：\n当前小规模纳税人增值税有季度免税额度（季度30万元），月销售额未达起征点的可以不用申报增值税。',
    '纳税义务发生时间：企业发生应税行为应当申报纳税的时间，通常以开具发票或提供服务的时间为准。\n\n申报期：税法规定的定期申报时限，如按月申报应在每月15日前完成。',
    '适用于所有新设立企业。',
    '一般纳税人需按月申报增值税，无论是否有收入。\n\n有员工的有限公司需每月代扣代缴个人所得税，不受收入影响。',
    '步骤1：确认税务登记时间\n步骤2：确认纳税人身份（小规模/一般纳税人）\n步骤3：确认适用的申报周期（月报/季报）\n步骤4：在电子税务局查看应申报税种\n步骤5：按期完成申报（零申报也要报）',
    '逾期申报会被处以滞纳金（每日万分之五）和罚款。\n\n连续3个月零申报可能触发税务机关的预警关注。',
    'scope_national', NULL,
    'certain_clear', '新公司 首次报税 设立 当月 申报期 零申报',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-DEC 系列：经营期 - 申报纳税（零申报）
-- =====================================================================

-- OPR-DEC-002: 长期零申报风险
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-DEC-002',
    '公司长期零申报有什么风险？',
    '我们公司暂时没有业务，一直在做零申报。长期零申报会不会有什么问题？',
    'OPR', 'DEC', 'type_risk',
    '长期零申报（通常超过6个月）可能引发税务机关关注，被认定为"非正常户"，进项税额无法抵扣，严重的可处以罚款甚至立案稽查。',
    '一、什么是零申报？\n零申报是指企业当期没有发生应税收入或应税行为，在税务系统中如实填报"零"（销售额为0）。\n\n二、零申报本身是合法的\n企业确实没有收入时，零申报是正常且合法的申报方式。\n\n三、长期零申报的风险：\n1. 触发税务预警：系统会标记长期零申报企业，税务机关可能要求实地核查\n2. 认定为非正常户：连续3个月零申报可能被评为"非正常户"，影响发票申领\n3. 进项税额不予抵扣：一般纳税人长期零申报，进项税额无法抵扣，造成损失\n4. 纳入重点监控对象：长期零申报企业会被列入重点监控名单\n5. 严重情况可稽查：虚假零申报（隐瞒收入）可能被定性为偷税\n\n四、哪些情况不宜长期零申报：\n- 有实际业务发生但隐瞒收入\n- 已购进货物或服务但隐瞒进项\n- 有员工工资但未代扣个税',
    '非正常户：已办理税务登记的纳税人未按规定的期限申报纳税，税务机关责令其限期改正后逾期不改正的，经派员实地检查，发现无下落、无法强制其履行纳税义务的。\n\n偷税：纳税人伪造、变造、隐匿、擅自销毁账簿、记账凭证，或者在账簿上多列支出或者不列、少列收入，导致不缴或者少缴应纳税款的行为。',
    '适用于所有长期没有收入但仍需维护的企业。',
    '季节性经营的企业（如滑雪场、游泳池）淡季零申报是正常现象，只要业务真实即可。\n\n初创企业前期投入期暂时没有收入，短期内零申报是正常的，但不宜超过12-18个月。',
    '步骤1：如实核算当期收入和支出\n步骤2：确认是否符合零申报条件\n步骤3：如长期无收入，考虑是否需要暂停营业或注销\n步骤4：如有业务发生但隐瞒收入，应主动补报\n步骤5：定期关注企业信用评级',
    '虚假零申报一旦被查处，可能面临补缴税款、加收滞纳金（每日万分之五）、处以0.5倍至5倍罚款。\n\n被认定为偷税的，还可能追究相关人员的法律责任。',
    'scope_national', NULL,
    'certain_clear', '零申报 长期零申报 非正常户 风险 偷税 预警',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- OPR-DEC-003: 季报还是月报
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-DEC-003',
    '小规模纳税人到底按月申报还是按季申报？',
    '听说小规模纳税人可以按季度申报，但又有人说要看情况，到底怎么判断？',
    'OPR', 'DEC', 'type_whether',
    '小规模纳税人增值税原则上按季申报，但有例外：开票额超过季度30万免税额度或开具了增值税专用发票的，需要按月申报。',
    '一、基本规则：小规模纳税人增值税按季申报\n\n年销售额未超过500万元的小规模纳税人，增值税按季度申报，每年4次（1月、4月、7月、10月）。\n\n二、什么时候需要按月申报？\n1. 开票额超过季度免税额度（季度30万元）：超过部分需要按月申报并缴税\n2. 开了增值税专用发票：无论销售额多少，专用发票部分需要按月申报\n3. 主管税务机关另有规定\n\n三、所得税申报周期：\n- 企业所得税：所有企业均按季度预缴（1月、4月、7月、10月）\n- 个人所得税：所有企业按月代扣代缴\n\n四、申报周期可以申请变更吗？\n小规模纳税人可以向主管税务机关申请将申报周期从季度改为月度，但一般不建议频繁变更。',
    '小规模纳税人：年应税销售额在规定标准以下，会计核算不健全，不能按规定报送有关税务资料的增值税纳税人。\n\n增值税起征点：当前小规模纳税人享受月度10万元（季度30万元）的免税额度。',
    '适用于所有小规模纳税人企业。',
    '一般纳税人必须按月申报增值税，不能按季度申报。\n\n开具了增值税专用发票的小规模纳税人，无论金额大小，专用发票部分需要按月申报。',
    '步骤1：确认纳税人身份（小规模还是一般纳税人）\n步骤2：小规模纳税人确认申报周期（季报还是月报）\n步骤3：核对当季/当月开票金额\n步骤4：在申报期内完成各税种申报\n步骤5：如有特殊情况（超过免税额度、开了专票），及时变更为月报',
    '申报周期判断错误导致逾期申报，会产生滞纳金和罚款。\n\n超过免税额度未及时申报部分收入，可能被认定为偷税。',
    'scope_national', NULL,
    'certain_clear', '小规模纳税人 月报 季报 申报周期 增值税 免税额度',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-INV 系列：经营期 - 发票管理
-- =====================================================================

-- OPR-INV-002: 发票领用
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-INV-002',
    '企业首次领用发票需要准备什么？',
    '公司刚办完税务登记，想申请发票，第一次领发票要带什么材料？',
    'OPR', 'INV', 'type_how',
    '首次领用发票需携带：税务登记证件、经办人身份证明、发票专用章，以及《发票领用簿》。一般纳税人还需先完成一般纳税人登记。',
    '一、确认纳税人身份\n- 小规模纳税人：可申领增值税普通发票、增值税普通发票（卷式）等\n- 一般纳税人：可申领增值税专用发票和增值税普通发票\n\n二、首次领用发票前的准备：\n1. 办理税务登记，取得《税务登记证》\n2. 刻制发票专用章（到公安机关批准的刻章点）\n3. 如需申领专用发票，先办理一般纳税人登记\n4. 在电子税务局提交发票票种核定申请\n5. 购买税控设备（如金税盘/税盘，通用）\n\n三、发票领用需携带的材料：\n- 《发票领用簿》\n- 税务登记证件原件\n- 经办人身份证明原件\n- 发票专用章\n- 税控设备（金税盘/税盘）\n\n四、领用数量：\n初次申领通常有数量限制，后续可根据实际使用情况申请增量。',
    '发票专用章：企业在开具发票时加盖在发票上的专用印章，与财务章不同。\n\n税控设备：用于电子化管理发票开具的专用设备（如金税盘、税盘），需向技术服务单位购买或租赁。\n\n发票票种核定：税务机关根据企业经营情况核定可使用的发票种类和数量。',
    '适用于所有需要开具发票的企业。',
    '非居民企业、临时经营的纳税人发票领用规定有所不同。\n\n特定行业（银行、保险等）有特殊的发票管理要求。',
    '步骤1：刻制发票专用章\n步骤2：在电子税务局申请发票票种核定\n步骤3：购买税控设备（金税盘/税盘）\n步骤4：到主管税务机关领取《发票领用簿》\n步骤5：携带材料到税务局领用发票\n步骤6：安装税控设备，开通电子开具功能',
    '购买税控设备是合理支出，可以全额抵扣增值税，但不得以"不要发票"为由不开具发票。\n\n虚开发票（为他人开具与实际业务不符的发票）是严重的违法行为。',
    'scope_national', NULL,
    'certain_clear', '发票领用 首次领用 发票专用章 税控设备 票种核定',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- OPR-INV-003: 发票作废与红字发票
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-INV-003',
    '开错的发票是作废还是开红字发票？',
    '给客户开了一张发票，但是发现金额开错了，是直接作废还是需要开红字发票？两种方式有什么区别？',
    'OPR', 'INV', 'type_whether',
    '当月开错的发票且符合作废条件（收回原发票、购买方未认证）的可以作废；跨月或已认证的发票只能开红字发票冲销。',
    '一、发票作废的条件（同时满足）：\n1. 开具时间在当月（未跨月）\n2. 收回原发票联和抵扣联（购买方未认证抵扣）\n3. 销售方未入账\n\n二、红字发票的适用情形：\n1. 跨月了，无法作废\n2. 购买方已认证抵扣\n3. 销售方已入账\n4. 发生退货、退款、折让\n5. 发票开具错误但购买方已记账\n\n三、开票流程差异：\n作废：在税控设备中直接作废，系统自动生成作废标识，不需要去税务局申请。\n\n红字发票：需先在电子税务局提交《开具红字增值税专用发票申请单》，核准后开具。\n\n四、普票和专票的区别：\n- 增值税普通发票：作废或开具红字普票即可，手续相对简单\n- 增值税专用发票：需走申请→核准→开具流程，相对复杂',
    '作废发票：发票开具后因错误在当月进行作废处理，发票视为无效。\n\n红字发票：因退货、折让等原因需要冲销原开具发票时，开具的负数发票。\n\n认证抵扣：购买方将增值税专用发票用于抵扣进项税额的行为，需在180日内完成认证。',
    '适用于开具发票后发生错误需要处理的情形。',
    '已认证抵扣的专用发票，购买方必须申请开具红字发票，销售方不能自行作废。\n\n专用发票超过认证期限未认证抵扣，可申请开红字发票。',
    '步骤1：确认发票是否符合作废条件（当月、未认证）\n步骤2：如符合作废条件，在税控设备中作废，打印作废标识\n步骤3：如不能作废，在电子税务局提交红字发票申请\n步骤4：税务机关核准后开具红字发票\n步骤5：重新开具正确金额的蓝字发票',
    '作废发票没有收回原发票联和抵扣联的，作废无效，需开具红字发票。\n\n虚开红字发票（无真实退货或折让）属于虚开发票行为，面临严重处罚。',
    'scope_national', NULL,
    'certain_clear', '发票作废 红字发票 跨月 退货 认证抵扣 专用发票',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- OPR-INV-004: 专票与普票的选择
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-INV-004',
    '客户要开专用发票，我们是小规模纳税人，能开吗？',
    '客户说必须要增值税专用发票，但我们是小规模纳税人，能开出来吗？',
    'OPR', 'INV', 'type_whether',
    '小规模纳税人可以到税务机关申请代开增值税专用发票，但税率按征收率（1%或3%）计算，非13%/9%/6%税率。',
    '一、小规模纳税人能否开具专用发票？\n可以。有两种方式：\n\n1. 自行开具：小规模纳税人自2020年起可自行开具增值税专用发票（仅限特定行业/企业，具体以最新政策为准）\n\n2. 申请代开：到主管税务机关申请代开增值税专用发票\n\n二、代开专票的税率：\n小规模纳税人代开的专票，税率为企业的征收率（当前为1%或3%），而非一般纳税人的税率。购买方收到后可以按规定抵扣进项税额。\n\n三、开具专票对销售方的影响：\n- 小规模纳税人开具专票部分需要缴税，不享受免税\n- 免税额度仅适用于普通发票\n\n四、客户不要专票要普票可以吗？\n可以。购买方为个人或小规模纳税人的，通常开具普通发票即可。购买方为一般纳税人的，需要专用发票才能抵扣进项税。',
    '代开增值税专用发票：主管税务机关根据小规模纳税人的申请，为其代为开具的增值税专用发票。\n\n征收率：小规模纳税人和简易计税方法使用的税率，低于一般纳税人适用的税率。',
    '适用于小规模纳税人收到客户要求开具专用发票的情形。',
    '自然人（个人）不能申请代开增值税专用发票（除特定情形外）。\n\n小规模纳税人开具的增值税普通发票不能抵扣进项税额。',
    '步骤1：确认客户是否真的需要专用发票（购买方是否为一船纳税人）\n步骤2：确认本企业是否已自行开通专票开具资质\n步骤3：如有需要，到税务局申请代开\n步骤4：如实申报专票部分的增值税\n步骤5：保留相关完税凭证',
    '为不具备抵扣资格的购买方开具专用发票，购买方抵扣后被发现，销售方可能面临连带责任。\n\n小规模纳税人开具专票不享受免税政策，需如实申报缴纳。',
    'scope_national', NULL,
    'certain_conditional', '专用发票 普通发票 小规模纳税人 代开 抵扣 进项税',
    1, 0,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-CHG 系列：变更登记
-- =====================================================================

-- OPR-CHG-002: 变更法定代表人
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-CHG-002',
    '公司换了法定代表人，税务上需要变更吗？',
    '公司原法定代表人离职了，需要变更新法定代表人，工商已经改了，税务这边要不要处理？',
    'OPR', 'CHG', 'type_how',
    '法定代表人变更后，需在工商变更后30日内到主管税务机关办理税务登记变更，电子税务局可线上办理。',
    '一、为什么需要变更？\n税务登记的法定代表人与工商登记的应当一致。如果工商已变更但税务未变更，会影响企业正常经营。\n\n二、变更流程：\n1. 在工商部门完成法定代表人变更登记\n2. 准备材料：变更后的营业执照、新法定代表人身份证明\n3. 在电子税务局提交变更申请，或到主管税务机关柜台办理\n4. 税务系统更新法定代表人信息\n\n三、需要变更的涉税信息：\n- 税务登记上的法定代表人信息\n- 发票领用簿上的相关信息\n- 购票员信息（如需变更）\n\n四、特别注意事项：\n如果新法定代表人在其他企业有未结清的税务问题，可能需要提供说明或担保。\n\n五、实名认证：\n新法定代表人需要在电子税务局完成实名认证。',
    '税务登记变更：税务登记内容发生变化时，向税务机关办理的变更登记手续。\n\n实名认证：通过人脸识别或银行卡验证确认自然人真实身份的管理制度。',
    '适用于公司法定代表人发生变更的情形。',
    '如果变更后涉及股权结构重大变化，可能需要重新进行税务清算和一般纳税人资格认定。\n\n外资企业法定代表人变更可能涉及外汇管理部门的额外审批。',
    '步骤1：在工商部门完成法定代表人变更\n步骤2：新法定代表人完成电子税务局实名认证\n步骤3：准备变更材料（执照、身份证明等）\n步骤4：电子税务局线上提交变更或到柜台办理\n步骤5：确认银行三方协议信息是否需要更新\n步骤6：如已申领发票，确认购票员信息是否需要更新',
    '未按时办理税务登记变更，可能被处以2000元以上10000元以下罚款。\n\n如果新法定代表人与原法人有未清税务关系，可能影响发票申领。',
    'scope_national', NULL,
    'certain_clear', '法定代表人 变更 税务登记 实名认证 工商变更',
    1, 0,
    'active', 1, datetime('now'), datetime('now')
);

-- OPR-CHG-003: 变更经营范围
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-CHG-003',
    '公司增加了新业务，税务上需要变更经营范围吗？',
    '公司原来做咨询的，现在开始卖货了，要不要去税务变更经营范围？',
    'OPR', 'CHG', 'type_whether',
    '经营范围变更后需在30日内到税务机关办理税务登记变更，新增业务涉及新税种的还需同步做税种认定调整。',
    '一、是否必须变更？\n是的。经营范围的变更是税务登记的重要内容，应当自工商变更之日起30日内向税务机关申报变更。\n\n二、变更经营范围对税务的影响：\n1. 新业务可能涉及新的税种（如新增销售业务后需缴纳增值税）\n2. 新业务可能涉及新的税率\n3. 发票种类可能需要增加（如新增销售业务需申领不同种类发票）\n4. 申报表格可能需要调整\n\n三、具体操作：\n1. 工商完成经营范围变更\n2. 到主管税务机关办理税务登记变更\n3. 根据新增业务调整税种认定（如需新增税种）\n4. 如需开具新业务的发票，申请增加发票种类和数量\n5. 更新财务核算科目，适应新业务\n\n四、注意特殊许可：\n如果新增业务需要特殊经营许可（如食品销售需食品经营许可证），在取得许可证后方可开具相关发票。',
    '税种认定：税务机关根据企业经营范围和实际经营情况，核定企业应当缴纳的税种和适用的征收方式。\n\n经营范围：企业登记注册的从事经营活动的业务范围。',
    '适用于企业在原有业务基础上新增经营项目（包括商品销售、服务提供等）的情形。',
    '新增业务属于特殊行业（危险化学品、医疗器械等）的，需先取得相应经营许可证。\n\n新增业务导致年应税销售额超过500万，需转为一般纳税人。',
    '步骤1：工商部门完成经营范围变更\n步骤2：取得新增业务所需的特殊经营许可证（如需要）\n步骤3：到主管税务机关办理税务登记变更\n步骤4：申请调整或新增税种认定\n步骤5：申请新增发票种类和用量\n步骤6：更新财务软件科目设置\n步骤7：确认新增业务的申报方式',
    '未办理税务登记变更，税务机关可处以2000元以下罚款，情节严重的处2000-10000元罚款。\n\n新增业务未申报缴税，可能被认定为偷税。',
    'scope_national', NULL,
    'certain_clear', '经营范围 变更 税务登记 税种认定 新业务 发票种类',
    1, 0,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-IIT 系列：经营期 - 个人所得税
-- =====================================================================

-- OPR-IIT-001: 个税代扣代缴义务
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-IIT-001',
    '公司给员工发工资，为什么要代扣代缴个人所得税？',
    '我是一人有限公司，自己给自己发工资，也需要申报个税吗？',
    'OPR', 'IIT', 'type_why',
    '个人所得税以所得人为纳税人，以支付所得的单位或个人为扣缴义务人。即使是只有一个股东的有限公司，股东作为员工取得工资也需要并入综合所得申报。',
    '一、什么是代扣代缴？\n个人所得税以所得人为纳税人，以支付所得的单位或个人为扣缴义务人。企业向员工支付工资时，应当从支付款项中扣下个人所得税，代为向税务机关申报缴纳。\n\n二、哪些所得需要代扣代缴？\n1. 工资、薪金所得\n2. 劳务报酬所得\n3. 稿酬所得\n4. 特许权使用费所得\n5. 利息、股息、红利所得\n6. 财产租赁所得\n7. 偶然所得\n\n三、一人有限公司的特殊情况：\n即使公司只有一个股东（自然人独资或法人独资），股东从公司取得工资，属于工资薪金所得，应当并入综合所得，按3%-45%税率缴纳个人所得税。\n\n公司不是个人所得税的纳税人，但必须履行扣缴义务。\n\n四、不申报的法律后果：\n扣缴义务人未履行扣缴义务，税务机关可以处以应扣未扣税款0.5倍以上3倍以下的罚款。',
    '代扣代缴：扣缴义务人在向纳税人支付款项时，从支付款项中扣下应纳税款，代为向税务机关申报缴纳的制度。\n\n综合所得：工资薪金、劳务报酬、稿酬、特许权使用费四项所得合并计税。',
    '适用于所有支付个人所得的企业，包括有限公司、合伙企业等。',
    '个人独资企业和合伙企业不适用代扣代缴，由业主或合伙人自行申报。\n\n外籍个人的个人所得税计算方式和免税补贴政策与中国居民个人有所不同。',
    '步骤1：到税务机关办理扣缴税款登记\n步骤2：收集员工身份信息，完成全员全额申报\n步骤3：每月计算员工工资薪金所得对应的个人所得税\n步骤4：在发放工资时扣下个人所得税\n步骤5：在次月15日前向税务机关申报并缴纳税款\n步骤6：年度终了，进行综合所得年度汇算清缴',
    '未履行代扣代缴义务，税务机关可处以应扣未扣税款0.5-3倍罚款。\n\n员工如需年度汇算清缴，单位有义务提供收入和已扣税信息。\n\n虚假申报工资、隐瞒员工收入属于偷税行为。',
    'scope_national', NULL,
    'certain_clear', '个税 代扣代缴 工资 薪金 扣缴义务人 综合所得',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-SSF 系列：经营期 - 社保费
-- =====================================================================

-- OPR-SSF-001: 社保登记与参保
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-SSF-001',
    '新公司注册后，多久要办理社保登记？',
    '刚成立了一家公司，听说社保也要登记，有没有时间限制？',
    'OPR', 'SSF', 'type_time',
    '企业应在成立之日起30日内到社保经办机构办理社会保险登记，取得《社会保险登记证》。',
    '一、法律依据：\n《社会保险法》第五十七条规定：用人单位应当自成立之日起三十日内凭营业执照、登记证书等证件，向当地社会保险经办机构申请办理社会保险登记。\n\n二、办理流程：\n1. 到工商注册地的社保经办机构（或通过当地政府网上平台）\n2. 提交材料：营业执照、法人代表身份证、公司银行账户信息\n3. 填写《社会保险登记表》\n4. 社保经办机构核定社保费用（缴费基数、缴费比例）\n5. 取得《社会保险登记证》\n\n三、社保包含哪些：\n- 基本养老保险\n- 基本医疗保险\n- 工伤保险\n- 失业保险\n- 生育保险（已并入医疗保险）\n\n四、缴费主体：\n- 用人单位：按员工工资总额缴纳（各地比例不同）\n- 员工个人：从工资中代扣代缴（按个人缴费基数）',
    '社会保险登记：用人单位向社会保险经办机构申报办理社会保险的法定程序。\n\n社保缴费基数：用于计算社会保险费用的基数，一般为员工上年度月平均工资。',
    '适用于所有在境内注册的企业（包括公司、合伙企业、个人独资企业等）。',
    '灵活就业人员（无雇主的个人）可以通过个人窗口参加社保，无需办理单位社保登记。\n\n建筑业、制造业等农民工集中的行业有专门的社保参保规定。\n\n深圳等地已实现多证合一，工商登记后自动生成社保登记。',
    '步骤1：确认当地社保登记办理方式（柜台或网上）\n步骤2：准备营业执照、法人身份证、银行账户信息\n步骤3：到社保经办机构填写《社会保险登记表》\n步骤4：核定缴费基数和险种\n步骤5：办理社保扣款三方协议（企业-银行-社保）\n步骤6：完成员工参保登记（员工入职后30日内办理）',
    '未办理社保登记：责令改正，补办应补缴的社保费，并自欠缴之日起按日加收万分之五的滞纳金。\n\n逾期仍不缴纳的，处欠缴数额1倍以上3倍以下罚款。',
    'scope_national', NULL,
    'certain_clear', '社保登记 参保 成立 时间限制 社会保险登记证 缴费基数',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-FEE 系列：经营期 - 成本费用
-- =====================================================================

-- OPR-FEE-001: 成本费用凭证
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-FEE-001',
    '没有发票的成本费用能不能入账？',
    '公司有些支出收不到发票，比如和一些散户、小店买东西，这些费用能不能做账？能不能税前扣除？',
    'OPR', 'FEE', 'type_whether',
    '能入账，但不一定能税前扣除。没有发票的成本费用，在会计上可以入账，但在企业所得税税前扣除需要满足真实性、合法性、关联性原则，且多数情况下需要发票作为税前扣除凭证。',
    '一、会计处理：\n会计核算以真实性为原则，只要有真实的业务发生，就可以做账。没有发票不影响会计账务处理。\n\n二、税务处理（能否税前扣除）：\n（一）必须要有发票才能扣除的情形：\n- 购买商品（原材料、办公用品等）\n- 接受服务（咨询费、服务费等）\n- 支出500元以上的现金支出\n\n（二）不需要发票即可税前扣除的情形：\n- 工资薪金支出（以工资表、付款记录等）\n- 社保费、公积金（以缴费凭证）\n- 差旅费津贴（以出差报告）\n- 通讯费补贴（以相关文件）\n- 国务院税务部门规定的其他情形\n\n三、没有发票如何处理：\n1. 尽量向对方索取发票\n2. 如确实无法取得，可凭其他外部凭证（合同、付款记录、收货单据等）进行税前扣除\n3. 年度汇算清缴时进行纳税调整\n\n四、温馨提示：\n无发票支出≠不能入账，但≠能税前扣除。财务核算和税务处理是两个不同的维度。',
    '税前扣除凭证：企业用于证明支出真实发生、可以按规定在企业所得税前扣除的凭证，发票是最主要的税前扣除凭证。\n\n真实性原则：支出应当与企业取得的收入相关，且确已实际发生。\n\n关联性原则：扣除项目应与取得收入直接相关。',
    '适用于企业发生各类成本费用支出但无法取得发票的情形。',
    '购买方与销售方存在关联关系（如母子公司、内部交易）的费用，税前扣除时对发票要求更严格。\n\n自然灾害等不可抗力造成的资产损失，有专门的税前扣除规定。',
    '步骤1：确认支出是否真实发生（保留合同、付款记录等证据链）\n步骤2：尽量向销售方/服务提供方索取发票\n步骤3：如无法取得发票，做会计分录入账\n步骤4：进行企业所得税申报时，对无发票部分做纳税调增\n步骤5：保存完整的证据链（合同、收据、付款截图等）备查',
    '无发票成本费用做了税前扣除被税务机关查实，除补缴企业所得税外，还可能加收滞纳金和罚款。\n\n购买假发票或让他人为自己虚开发票，属于虚开发票行为，面临严重法律处罚。',
    'scope_national', NULL,
    'certain_clear', '发票 成本费用 税前扣除 凭证 没有发票 真实性 关联性',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- OPR-RISK 系列：经营期 - 风险应对
-- =====================================================================

-- OPR-RISK-001: 税务异常与非正常户
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'OPR-RISK-001',
    '公司被认定为非正常户，会影响正常开发票吗？',
    '公司有一次忘记申报了，现在收到通知说变成了非正常户，这个会影响正常开票吗？怎么恢复正常？',
    'OPR', 'RISK', 'type_risk',
    '被认定为非正常户后，发票申领和开具都会受到限制，必须先到税务机关办理解除手续才能恢复正常。',
    '一、什么情况下会被认定为非正常户？\n1. 未按规定的期限申报纳税\n2. 责令限期改正后逾期仍不申报\n3. 税务机关派员实地检查无下落\n4. 无法强制履行纳税义务\n\n二、非正常户的影响：\n1. 发票申领：无法领用发票，已领用的发票可能被停供\n2. 发票开具：税控设备可能被锁死，无法开具发票\n3. 申报缴款：无法正常进行申报和缴款\n4. 信用评级：企业纳税信用等级直接降为D级\n5. 经营限制：无法参与政府采购、招标等\n\n三、如何解除非正常户：\n1. 补办所有逾期的纳税申报\n2. 缴纳欠缴的税款\n3. 缴纳因逾期申报产生的滞纳金\n4. 到主管税务机关提交解除非正常户申请\n5. 接受税务机关可能进行的实地核查\n6. 补充提供相关证明材料\n\n四、特别提示：\n即使公司已没有任何业务，也应当按期进行零申报，否则可能被认定为非正常户。',
    '非正常户：已办理税务登记的纳税人未按规定的期限申报纳税，经税务机关责令限期改正后逾期仍不改正，且经实地检查无下落，无法强制其履行纳税义务的。\n\n纳税信用等级：税务机关根据纳税人履行纳税义务情况评定的等级，由高到低分为A、B、M、C、D五级。',
    '适用于被认定为非正常户或担心被认定的企业。',
    '被认定为非正常户后连续6个月未改正，将被吊销营业执照（工商层面）。\n\n非正常户法定代表人重新创业设立新公司，可能受到经营限制。',
    '步骤1：到主管税务机关查询欠税和逾期申报情况\n步骤2：补办所有逾期的纳税申报表\n步骤3：缴纳所有欠缴税款\n步骤4：缴纳滞纳金（每日万分之五）\n步骤5：提交解除非正常户申请\n步骤6：接受实地核查（如需要）\n步骤7：税务机关解除非正常户认定后，恢复正常状态',
    '被认定非正常户期间开具的发票，税务机关有权认定为无效发票。\n\n连续6个月被认定为非正常户，工商部门可吊销营业执照。\n\n被吊销营业执照的企业，法定代表人的信用记录将受到影响。',
    'scope_national', NULL,
    'certain_clear', '非正常户 税务异常 发票锁定 解除 纳税信用 逾期申报',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- CLS-CLEAR 系列：注销期 - 清税注销
-- =====================================================================

-- CLS-CLEAR-002: 注销前清税
INSERT OR IGNORE INTO question_master (
    question_code, question_title, question_plain,
    stage_code, module_code, question_type,
    one_line_answer, detailed_answer,
    core_definition, applicable_conditions,
    exceptions_boundary, practical_steps,
    risk_warning, scope_level, local_region,
    answer_certainty, keywords,
    high_frequency_flag, newbie_flag,
    status, version_no, created_at, updated_at
) VALUES (
    'CLS-CLEAR-002',
    '公司注销前，有哪些税必须要清完？',
    '准备把公司注销了，听说注销前要先清税，到底哪些税要清？有没有时间要求？',
    'CLS', 'CLEAR', 'type_how',
    '注销前必须结清所有应纳税款，包括增值税、企业所得税、个人所得税等，并完成所有税种的当期申报，缴销剩余发票和税控设备。',
    '一、必须结清的事项：\n1. 所有税种的当期申报（完成注销前最后一个申报期）\n2. 所有欠缴的税款（增值税、企业所得税、个人所得税等）\n3. 所有滞纳金和罚款\n4. 缴销未使用的增值税发票\n5. 缴销税控设备（金税盘/税盘）\n6. 上缴空白发票\n\n二、各税种特别注意：\n- 增值税：确保已认证发票均已抵扣或转出，无留抵税额异常\n- 企业所得税：完成最后一次季度预缴和年度汇算清缴\n- 个人所得税：最后一个月的工资个税必须全员申报\n- 发票：已开和未开的发票都需要处理\n\n三、注销前的准备工作：\n1. 盘点公司所有资产（存货、固定资产等）\n2. 处理存货（销售或分配给股东），涉及增值税\n3. 处理固定资产（转让或报废），涉及增值税或企业所得税\n4. 收回所有应收账款（涉及企业所得税）\n5. 清偿所有应付账款\n6. 完成最后一次纳税申报\n\n四、特别提示：\n有欠税的企业必须先还清欠税才能注销，税务机关有权追缴欠税直至采取强制执行措施。',
    '清税证明：企业在申请注销工商登记前，由税务机关出具的说明企业已结清应纳税款、滞纳金、罚款的证明文件。\n\n留抵税额：一般纳税人尚未抵扣的进项税额，注销时不能退税，只能转给其他关联企业。',
    '适用于所有准备注销的企业，包括各类公司形式。',
    '存在以下情况的企业，注销前需要特别处理：\n- 有未抵扣完的进项税额（留抵税额）\n- 有未弥补的亏损（可转移给关联企业）\n- 有未处理的出口退税\n- 有税务稽查或评估案件未结\n\n个体工商户简易注销不需要提供清税证明（以当地规定为准）。',
    '步骤1：召开股东会，作出解散决议\n步骤2：成立清算组（有限公司）\n步骤3：到税务机关办理注销预检\n步骤4：结清所有税款，缴销发票和税控设备\n步骤5：取得清税证明\n步骤6：到工商部门办理注销登记\n步骤7：到社保、银行等其他部门办理账户注销',
    '未清税即注销，税务机关有权继续追缴原公司欠税，股东可能承担连带责任。\n\n隐瞒资产或欠税，注销后被发现的，按偷税处理，可以追究原股东和相关人员的法律责任。\n\n虚假承诺无欠税骗取简易注销，登记机关可以撤销注销登记，恢复企业主体资格。',
    'scope_national', NULL,
    'certain_clear', '注销 清税 欠税 缴销发票 税控设备 清算 简易注销',
    1, 1,
    'active', 1, datetime('now'), datetime('now')
);

-- =====================================================================
-- 标签关联（question_tag_link）
-- =====================================================================

-- SET-REG-003 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'SET-REG-003' AND t.tag_code IN ('SET', 'REG', 'type_how', 'certain_clear', 'tag_registration');

-- SET-REG-004 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'SET-REG-004' AND t.tag_code IN ('SET', 'REG', 'type_how', 'certain_clear', 'tag_registration');

-- SET-DEC-002 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'SET-DEC-002' AND t.tag_code IN ('SET', 'DEC', 'type_whether', 'certain_clear', 'tag_zero_report');

-- OPR-DEC-002 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-DEC-002' AND t.tag_code IN ('OPR', 'DEC', 'type_risk', 'certain_clear', 'tag_zero_report', 'tag_risk');

-- OPR-DEC-003 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-DEC-003' AND t.tag_code IN ('OPR', 'DEC', 'type_whether', 'certain_clear', 'tag_zero_report');

-- OPR-INV-002 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-INV-002' AND t.tag_code IN ('OPR', 'INV', 'type_how', 'certain_clear', 'tag_invoice');

-- OPR-INV-003 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-INV-003' AND t.tag_code IN ('OPR', 'INV', 'type_whether', 'certain_clear', 'tag_invoice');

-- OPR-INV-004 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-INV-004' AND t.tag_code IN ('OPR', 'INV', 'type_whether', 'certain_conditional', 'tag_invoice');

-- OPR-CHG-002 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-CHG-002' AND t.tag_code IN ('OPR', 'REG', 'type_how', 'certain_clear', 'tag_change');

-- OPR-CHG-003 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-CHG-003' AND t.tag_code IN ('OPR', 'REG', 'type_whether', 'certain_clear', 'tag_change');

-- OPR-IIT-001 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-IIT-001' AND t.tag_code IN ('OPR', 'IIT', 'type_why', 'certain_clear');

-- OPR-SSF-001 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-SSF-001' AND t.tag_code IN ('OPR', 'SSF', 'type_time', 'certain_clear');

-- OPR-FEE-001 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-FEE-001' AND t.tag_code IN ('OPR', 'FEE', 'type_whether', 'certain_clear');

-- OPR-RISK-001 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'OPR-RISK-001' AND t.tag_code IN ('OPR', 'RISK', 'type_risk', 'certain_clear', 'tag_risk');

-- CLS-CLEAR-002 标签
INSERT OR IGNORE INTO question_tag_link (question_id, tag_id, display_order)
SELECT q.id, t.id, 1
FROM question_master q, tag_dict t
WHERE q.question_code = 'CLS-CLEAR-002' AND t.tag_code IN ('CLS', 'CLEAR', 'type_how', 'certain_clear');

-- =====================================================================
-- 关联问题（question_relation）
-- =====================================================================

-- SET-REG 系列关联
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-001' AND r.question_code = 'SET-REG-002';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-002' AND r.question_code = 'SET-REG-003';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-002' AND r.question_code = 'SET-DEC-002';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-003' AND r.question_code = 'OPR-DEC-001';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'SET-REG-003' AND r.question_code = 'SET-REG-004';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'SET-DEC-002' AND r.question_code = 'OPR-DEC-001';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'SET-DEC-002' AND r.question_code = 'OPR-DEC-002';

-- OPR-INV 系列关联
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-INV-001' AND r.question_code = 'OPR-INV-003';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-INV-001' AND r.question_code = 'OPR-INV-002';

-- OPR-DEC 系列关联
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-DEC-001' AND r.question_code = 'OPR-DEC-002';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-DEC-001' AND r.question_code = 'OPR-DEC-003';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-DEC-002' AND r.question_code = 'OPR-RISK-001';

-- OPR-CHG 系列关联
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-CHG-001' AND r.question_code = 'OPR-CHG-002';

INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 2
FROM question_master q, question_master r
WHERE q.question_code = 'OPR-CHG-001' AND r.question_code = 'OPR-CHG-003';

-- CLS-CLEAR 系列关联
INSERT OR IGNORE INTO question_relation (question_id, related_id, relation_type, display_order)
SELECT q.id, r.id, 'related', 1
FROM question_master q, question_master r
WHERE q.question_code = 'CLS-CLEAR-001' AND r.question_code = 'CLS-CLEAR-002';

-- SELECT 'Content expansion batch completed: 13 new questions added' AS result;
