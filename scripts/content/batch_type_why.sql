-- 批量插入type_why问题：补8条"为什么"类问题
-- 执行: cd /Volumes/外接硬盘/vibe/coding/网站/知识库 && python3 scripts/content/batch_type_why.py

-- OPR-REG-002: 企业为什么要进行税务登记？不登记会有什么后果？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-REG-002',
    '企业为什么要进行税务登记？不登记会有什么后果？',
    '',
    'OPR',
    'REG',
    'type_why',
    '税务登记是纳税人的法定义务，未办理将被责令限期改正并处罚款，逾期可能按偷税处理，面临滞纳金和税款5倍以下罚款。',
    '税务登记是纳税人依法向税务机关申报纳税的法定义务前提。《税收征收管理法》规定企业应自领取营业执照之日起30日内办理税务登记。未办理税务登记的，税务机关有权责令限期改正，可以处2000元以下罚款；情节严重的处2000-10000元罚款；长期未登记可能被认定为偷税，按日加收万分之五滞纳金，并处不缴或少缴税款50%以上5倍以下罚款。税务登记同时也是企业开具发票、享受税收优惠、办理出口退税等一切涉税事项的前置条件。',
    '税务登记是《税收征收管理法》规定的纳税人义务，营业执照签发之日起30日内必须办理，否则面临罚款、信用降级等风险。',
    '已领取营业执照但尚未办理税务登记的企业。',
    '特殊行业（免登记的政府机关、事业单位等）不在本问题范围内；个人独资企业和合伙企业也需办理税务登记。',
    '1.凭营业执照到主管税务机关办税服务厅办理税务登记；2.采集法定代表人、财务负责人实名信息；3.提交注册资本、投资总额等财务制度信息；4.根据经营范围确认需要申报的税种；5.开通电子税务局账号和CA证书。',
    '未办理税务登记被查处后，不仅面临罚款，还可能导致已开具发票的下游企业无法税前扣除；被认定为偷税后，税款、滞纳金和罚款金额可能远超企业预期；纳税信用降级影响发票申领和融资贷款。',
    'scope_national',
    'certain_clear',
    1,
    1,
    '税务登记,未登记处罚,偷税认定,滞纳金,纳税信用,营业执照',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-VAT-002: 增值税为什么要设置不同税率？13%、9%、6%、0税率分别适用于哪些场景？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-VAT-002',
    '增值税为什么要设置不同税率？13%、9%、6%、0税率分别适用于哪些场景？',
    '',
    'OPR',
    'VAT',
    'type_why',
    '增值税多档税率体现国家产业政策和民生保障导向：13%适用于一般货物和加工修理修配；9%适用于民生基础货物和交通运输、不动产服务；6%适用于现代服务业；0税率仅适用于出口。',
    '增值税设置多档税率是基于以下政策考量：13%税率（基本税率）适用于销售或进口货物、提供加工修理修配劳务、租赁有形动产等一般性经营行为；9%税率适用于粮食等农产品、自来水、图书、报纸杂志、音像制品、电子出版物、天然气、热水、食用盐、饲料、化肥、农机、农药、农膜等民生和基础性货物，以及交通运输、邮政、基础电信、不动产租赁、不动产销售、建筑服务等；6%税率适用于现代服务业（研发/技术/信息技术/文化创意/物流辅助/鉴证咨询/广播影视/其他现代服务）、增值电信服务、金融服务、生活服务，以及销售无形资产；0税率仅适用于出口货物和服务，以及符合规定的跨境应税行为。',
    '增值税税率档次设计体现国家产业政策和民生保障导向，不同货物和服务按其性质适用不同税率。',
    '一般纳税人在开票和申报时需要准确判断适用税率。',
    '混合销售行为（同时销售货物和服务）按主业适用税率；兼营不同税率货物未分别核算的从高适用税率；出口货物享受0税率需收齐出口报关单和购进货物发票等凭证。',
    '1.对照《增值税税目税率表》确认销售货物或服务的税目；2.判断是否属于9%低税率的民生类货物或基础服务；3.判断是否属于6%税率的现代服务业范围；4.出口业务确认是否符合同税率条件；5.混合销售和兼营分别核算。',
    '税率适用错误会导致申报错误，形成偷税或欠税风险；低税率货物错误适用高税率多缴税，适用低税率则面临补税和滞纳金；兼营未分别核算的从高税率，企业可能承担不必要的税负。',
    'scope_national',
    'certain_clear',
    1,
    1,
    '增值税税率,13%税率,9%税率,6%税率,零税率,现代服务业,民生货物',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-IIT-002: 年终奖为什么要单独计税？不单独计税会多交税吗？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-IIT-002',
    '年终奖为什么要单独计税？不单独计税会多交税吗？',
    '',
    'OPR',
    'IIT',
    'type_why',
    '年终奖单独计税是税收优惠政策，通过除以12降低适用税率档次；但并非对所有人都有利，低收入者并入综合所得可能反而更节税。',
    '年终奖单独计税是一项阶段性优惠政策。将年终奖除以12得到的数额，单独按月换算后适用综合所得税率表计算应纳税额，可以降低适用税率档次，减少应纳税额。具体来说：年终奖单独计税时，应纳税额 = 年终奖金额 × 适用税率 - 速算扣除数（月度）；并入综合所得计税时，年终奖与工资薪金合并后可能推高整体适用税率档次，导致税负增加。但并非所有人并入都多交：对于低收入者（每月工资低于基本减除费用5000元），并入综合所得可能反而更划算，因为基本减除费用和专项附加扣除可以更好地抵扣。财政部公告该政策延续至2027年底。',
    '年终奖单独计税是税收优惠政策，通过降低适用税率档次实现税负减轻，但并非对所有人都有利，低收入者并入可能更节税。',
    '企业发放年终奖的个人（非居民个人）。',
    '在一个纳税年度内，对每一纳税人该计税方法只允许采用一次；员工从两处以上取得年终奖需合并计税；非居民个人年终奖计税另有规定。',
    '1.企业财务计算年终奖金额；2.分别测算单独计税和并入综合所得两种方式的应纳税额；3.告知员工测算结果，由员工选择计税方式（企业代扣代缴）；4.单独计税的年终奖在次年3-6月综合所得年度汇算时无需再并入。',
    '选择错误的计税方式可能导致员工多缴税（企业未充分告知风险则存在劳动纠纷隐患）；单独计税方式在2027年底前有效，政策到期后需关注财政部公告；企业财务需保留员工选择计税方式的书面记录。',
    'scope_national',
    'certain_conditional',
    1,
    0,
    '年终奖单独计税,综合所得,并入计税,年终奖优惠政策,税率档次,年终奖税率',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-PREF-002: 企业享受税收优惠为什么需要备查？备查和备案有什么区别？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-PREF-002',
    '企业享受税收优惠为什么需要备查？备查和备案有什么区别？',
    '',
    'OPR',
    'PREF',
    'type_why',
    '备案制下税务机关事前审核，留存备查制下企业自行判断合规并承担事后责任；国家持续简化优惠办理流程，扩大备查范围以降低纳税人办税成本。',
    '税收优惠的备案和备查是两种不同的管理方式：备案制（已改为留存备查）是指纳税人享受优惠政策前，需到税务机关提交相关证明材料，经税务机关登记受理；留存备查制是指纳税人自行判断是否符合优惠条件，符合条件的只需将相关证明材料留存备查，无需到税务机关办理，税务机关后续进行抽查核查。2018年以来国家大幅简化优惠办理流程，扩大留存备查范围，如小型微利企业所得税优惠、研发费用加计扣除等均改为留存备查。备查制下企业需承担更大的合规责任：若经税务机关核查发现不符合优惠条件，将追缴税款并加收滞纳金，情节严重的还可能面临罚款。',
    '备案制下税务机关事前审核，留存备查制下企业事后合规责任更重；国家持续扩大备查范围旨在降低纳税人办税成本。',
    '正在享受或拟享受各项税收优惠政策的企业。',
    '部分优惠仍保留核准制（如集成电路企业税收优惠、动漫企业优惠等），需经国家部委核准后才能享受；跨境服务贸易等特殊优惠需经商务部等部门认定。',
    '1.对照最新税收优惠政策，判断是否符合条件；2.属于留存备查的优惠，准备相关证明材料并存档备查；3.属于备案类的优惠，在享受前到税务机关提交备案申请；4.年度汇算清缴时按要求填报优惠金额等信息；5.妥善保管备查资料（建议保存至少10年）。',
    '留存备查材料不齐全或不符合条件但已享受优惠，面临补税、滞纳金和罚款风险；将不符合条件的支出计入优惠归集范围（如将非研发人员人工费计入研发费用加计扣除）属于偷税行为；政策到期后未及时关注新政策可能导致延续优惠失效。',
    'scope_national',
    'certain_clear',
    1,
    1,
    '税收优惠备查,留存备查,备案制,研发费用加计扣除,小型微利企业,合规责任',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-SSF-002: 企业必须为所有员工缴纳社保吗？试用期员工和兼职人员也要缴吗？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-SSF-002',
    '企业必须为所有员工缴纳社保吗？试用期员工和兼职人员也要缴吗？',
    '',
    'OPR',
    'SSF',
    'type_why',
    '试用期员工必须缴纳社保；非全日制用工只需缴工伤险；其他情形均需依法缴纳五险，不缴违法。',
    '社会保险法规定中华人民共和国境内的用人单位和个人应依法缴纳社会保险。试用期员工与正式员工享有同等社保权利，用人单位不得以试用期为由拒绝缴纳社保；应在用工之日起30日内为员工办理社保登记并申报缴费。兼职人员（存在劳动关系的兼职）需要缴纳社保；非全日制用工（每日工作不超过4小时）用人单位只需为其缴纳工伤保险，无需缴纳其他四险。学生兼职（未毕业实习生）与用人单位若建立劳动关系，应缴纳社保；若仅为实习关系，部分地区允许按特殊规定处理。用人单位不缴社保面临行政处罚（责令补缴并处0.5-3倍罚款）、员工投诉、劳动仲裁，以及无法享受工伤保险待遇的法律后果。',
    '试用期员工必须缴纳社保；非全日制用工只需缴工伤险；其他情形均需依法缴纳五险，不缴违法。',
    '各类企业、个体工商户等用人单位。',
    '退休返聘人员（已享受养老保险待遇）不需要再缴社保；境外员工（含港澳台）社保缴纳另有专门规定；建筑工程等按项目参保的情形适用特殊规定。',
    '1.员工入职30日内到社保经办机构办理社保登记；2.试用期包含在社保缴纳期限内，不得以试用期为由中断；3.非全日制用工单独签订劳动合同并申报工伤保险；4.实习生确认劳动关系后（以实际用工为准）及时参保；5.员工离职当月仍需缴纳社保。',
    '试用期不缴社保，员工以此为由主张被迫解除劳动合同并要求经济补偿，法院一般支持；员工发生工伤但单位未缴社保，所有工伤待遇由用人单位自行承担；被员工举报或劳动监察发现，企业除补缴外还面临行政处罚和补缴期间的利息。',
    'scope_national',
    'certain_conditional',
    1,
    1,
    '试用期社保,非全日制用工,工伤保险,兼职人员社保,实习生社保,五险一金,社保登记',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-DEC-002: 企业明明没有税款要交，为什么还要按期申报？不申报有什么后果？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-DEC-002',
    '企业明明没有税款要交，为什么还要按期申报？不申报有什么后果？',
    '',
    'OPR',
    'DEC',
    'type_why',
    '无税款也要申报（零申报），申报是纳税人的程序性义务，违反将产生滞纳金、信用降级等严重后果。',
    '纳税申报是纳税人的法定义务，无论当期有无应纳税款，纳税人都必须按期申报。申报的意义在于：税务机关通过纳税申报掌握纳税人经营情况，即使无税款也应零申报；若不申报，税务机关无法了解企业真实经营状态，可能将其列入重点监控对象。具体后果：逾期申报将被加收滞纳金（按日加收万分之五）；连续3个月未申报的企业可能被认定为非正常户；长期不申报可能导致税务稽查和罚款；零申报超过一定期限（通常为6个月）可能引起税务机关警觉，要求提供账簿资料进行纳税评估；企业纳税信用评级也会因逾期申报被扣分，影响发票申领、融资贷款等。',
    '无税款也要申报（零申报），申报是纳税人的程序性义务，违反将产生滞纳金、信用降级等严重后果。',
    '所有已办理税务登记的纳税人。',
    '享受定期定额征收的个体工商户（定额户）按定额申报，不适用本问题；企业进入注销程序后按注销流程处理，不适用正常申报规则。',
    '1.每月/每季登录电子税务局进行纳税申报；2.当期无税款也要进行零申报（各税种均需操作）；3.确认申报状态为已申报且已入库（有税款的情况下）；4.保存好申报记录和完税凭证；5.设置申报日历提醒，避免遗漏。',
    '逾期申报按日加收万分之五滞纳金，累计金额可能远超预期；连续3个月零申报可能被系统标记为异常；长期不申报导致纳税信用等级降级（D级），影响发票申领和日常经营；被列入非正常户后解除成本远高于正常申报维护成本。',
    'scope_national',
    'certain_clear',
    1,
    1,
    '零申报,按期申报,逾期申报,非正常户,纳税信用,滞纳金,电子税务局',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-CLEAR-002: 企业注销时为什么要先清税？清税证明是什么？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-CLEAR-002',
    '企业注销时为什么要先清税？清税证明是什么？',
    '',
    'OPR',
    'CLEAR',
    'type_why',
    '清税是工商注销的前置条件，确保国家税款不因企业注销而流失；清税证明是税务机关出具的税务事项结清文书。',
    '清税是指企业在申请注销工商登记前，需先在税务机关完成所有税种的申报结清，包括：缴纳所有欠缴税款、滞纳金和罚款；完成当年度企业所得税汇算清缴；缴销未使用发票和税控设备；处理出口退税业务结清等。清税证明是税务机关出具的，证明纳税人所有税务事项已结清的文书，是工商部门办理注销营业执照的前置条件。2022年起实行一网通办，税务清税信息和工商注销登记通过数据共享互通，但实践中仍建议先完成清税再申请工商注销。清税过程中若发现企业有欠税、偷税等情形，税务机关可依法阻止其注销登记。',
    '清税是工商注销的前置条件，确保国家税款不因企业注销而流失；企业需先结清所有税务事项才能合法注销。',
    '申请注销登记的企业（含公司、合伙企业、个人独资企业等）。',
    '破产企业持人民法院终结破产程序裁定书可直接到税务机关办理注销，无需清税；分支机构注销时须先完成分支机构清税，总机构同步更新汇总纳税信息。',
    '1.到主管税务机关申请清税（如已三证合一可电子税务局申请）；2.提交当期各税种申报表，结清所有应纳税款；3.缴纳欠缴税款、滞纳金和罚款（如有）；4.缴销所有未使用发票和税控设备；5.取得清税证明（电子税务局可查询电子版）；6.凭清税证明到市场监管部门申请注销登记。',
    '未清税即申请工商注销，工商部门将驳回申请，且可能影响企业及其法定代表人的信用记录；清税过程中发现的税收违法行为（如欠税、偷税）将被追缴并处罚；印花税等小税种漏申报同样会导致无法取得清税证明。',
    'scope_national',
    'certain_clear',
    1,
    1,
    '清税证明,注销清税,税务注销,一网通办,欠税注销,发票缴销,汇算清缴',
    'active',
    1,
    datetime('now'),
    datetime('now')
);

-- OPR-TAX-005: 企业为什么会成为非正常户？被认定非正常户和正常户有什么区别？
INSERT INTO question_master (question_code, question_title, question_plain, stage_code, module_code, question_type, one_line_answer, detailed_answer, core_definition, applicable_conditions, exceptions_boundary, practical_steps, risk_warning, scope_level, answer_certainty, high_frequency_flag, newbie_flag, keywords, status, version_no, created_at, updated_at)
VALUES (
    'OPR-TAX-005',
    '企业为什么会成为非正常户？被认定非正常户和正常户有什么区别？',
    '',
    'OPR',
    'TAX',
    'type_why',
    '非正常户主要因逃避纳税义务被认定，正常经营企业应保持联系畅通、按时申报以避免触发。',
    '非正常户的认定原因主要包括：企业已实际停止经营但未办理注销登记；企业地址变更后未通知税务机关更新联系方式，导致税务机关多次实地核查均无法找到；企业未按规定进行纳税申报，经责令限期改正后仍不申报。非正常户与正常户的主要区别：发票领购——正常户可随时申领发票，非正常户被暂停发票供应；申报办理——正常户可网上申报，非正常户必须到办税服务厅现场办理；信用评价——非正常户直接导致纳税信用等级降为D级，影响融资、招标等；法律责任——非正常户期间若继续从事经营活动并开具发票，按虚开发票处理；解除难度——解除非正常户需补齐所有逾期申报和欠缴税款，成本远高于正常维护。',
    '非正常户是税收管理的惩戒性措施，主要针对逃避纳税义务的企业，正常经营企业应保持联系畅通、按时申报以避免触发。',
    '已办理税务登记的所有纳税人。',
    '企业实际控制人失联、恶意逃避纳税义务是触发非正常户的主要原因；因不可抗力（如自然灾害）导致无法正常申报的，需提供证明材料申请特殊处理。',
    '1.保持注册地址和联系方式真实有效，变更后及时在电子税务局更新；2.按时进行纳税申报（包括零申报）；3.若预计无法按期申报，提前申请延期申报；4.定期登录电子税务局确认申报状态；5.安排专人负责纳税申报工作，避免遗漏。',
    '被认定为非正常户后，法定代表人名下其他企业也可能受到关联影响；被暂停发票供应后，正常生产经营将受到严重制约；D级纳税信用等级保留两年，期间无法享受即时办结类涉税服务；非正常户持续满两年，税务登记证失效，税务机关可依法申请强制注销。',
    'scope_national',
    'certain_clear',
    1,
    1,
    '非正常户,纳税信用等级D级,解除非正常户,地址失联,逾期申报,发票暂停,失信惩戒',
    'active',
    1,
    datetime('now'),
    datetime('now')
);
