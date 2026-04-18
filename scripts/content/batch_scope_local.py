#!/usr/bin/env python3
"""
批量导入 scope_local（地方口径）问题 - 8条
聚焦广西/柳州市柳江区特殊规定
"""
import json, sqlite3, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"

batch_local = {
    "questions": [
        {
            "question_title": "广西新办企业想申请成为一般纳税人，在当地有什么特殊流程或要求？",
            "question_plain": "公司在广西南宁刚设立，想直接申请一般纳税人，广西的税务机关在审批流程上有什么特殊要求吗？",
            "stage_code": "SET",
            "module_code": "REG",
            "question_type": "type_procedure",
            "one_line_answer": "广西一般纳税人申请流程与全国一致，在广西电子税务局线上申请，线下提交《增值税一般纳税人资格登记表》，无特殊审批门槛。",
            "detailed_answer": "广西的一般纳税人资格申请适用全国统一规定，企业在办理税务登记后，可向主管税务机关提交《增值税一般纳税人资格登记表》申请认定。在广西电子税务局上线后，企业可通过线上渠道提交申请，税务机关在电子受理后进行实地核查（主要核查会计核算是否健全，是否有固定的生产经营场所），核查通过后认定为一般纳税人。值得注意的是，南宁市、柳州市等广西重点城市的税务机关对会计核算健全性的核查相对更严格，要求企业提供账簿、凭证、会计报表等资料备查。",
            "core_definition": "一般纳税人资格认定：企业向主管税务机关申请，经税务机关审核认定其会计核算健全后，赋予其一般纳税人资格并按一般计税方法计算缴纳增值税的法定程序。",
            "applicable_conditions": "在广西壮族自治区行政区域内办理了税务登记的企业；会计核算健全（有专业会计人员、建立账簿、凭证完整）；有固定的生产经营场所。",
            "exceptions_boundary": "部分地市（如南宁、柳州）对于个体工商户转企业纳税人的认定，要求更严格的会计资料审核；新办企业如果上一年度销售额已超过小规模纳税人标准（500万元），税务机关可主动认定其为一般纳税人。",
            "practical_steps": "广西一般纳税人认定流程：（1）向主管税务机关办税服务厅提交《增值税一般纳税人资格登记表》（一式两份）；（2）准备会计资料：最近一期的会计报表、账簿、凭证；（3）税务机关进行实地核查，核实生产经营场所和会计核算情况；（4）核查通过后，税务机关在系统中维护纳税人身份，发放一般纳税人认定文书；（5）安装增值税发票管理系统（百旺或航天信息税控盘）；（6）认定完成后次月生效。",
            "risk_warning": "认定通过前提前按一般纳税人开具发票：属于违规开具，税务机关可按发票管理规定处理。认定为一般纳税人后会计核算造假：税务机关可取消认定资格，补缴税款并处罚款。",
            "scope_level": "scope_local",
            "local_region": "广西壮族自治区",
            "answer_certainty": "certain_clear",
            "keywords": "广西,一般纳税人认定,会计核算健全,电子税务局,增值税",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-002", "support_type": "support_direct", "support_note": "一般纳税人资格认定全国统一标准"},
                {"policy_code": "GOV-Tax-002", "support_type": "support_procedure", "support_note": "税务登记管理办法中的纳税人身份认定程序"}
            ],
            "tags": ["广西", "一般纳税人", "税务登记"],
            "relations": [{"question_code": "SET-REG-012", "relation_type": "related"}]
        },
        {
            "question_title": "柳州市柳江区企业申报增值税，在申报期限上有无特殊规定？",
            "question_plain": "公司在柳州市柳江区，小规模纳税人按季度申报增值税，申报截止日期是否和全国一致，还是有当地特殊规定？",
            "stage_code": "OPR",
            "module_code": "DEC",
            "question_type": "type_time",
            "one_line_answer": "柳州市柳江区小规模纳税人增值税申报截止日期与全国一致，季度终了后15日内申报（即每年4/7/10/1月的15日前），无柳江区地方特殊规定。",
            "detailed_answer": "根据国家税务总局的规定，增值税小规模纳税人的申报期限为季度终了后15日内，申报期最后一日为法定休假日的，以休假日期满的次日为期限届满日。柳州市柳江区作为广西壮族自治区柳州市下辖区，执行广西壮族自治区税务局统一的申报期限规定，与全国保持一致，不存在单独的地方申报截止日特殊规定。但需注意：如遇重大自然灾害或突发事件，税务总局或广西区税务局可能会临时调整申报期限，企业应及时关注国家税务总局广西区税务局官方网站或柳州市柳江区税务局公告。",
            "core_definition": "增值税申报期限：纳税人向税务机关申报并缴纳应纳税款的法定时间限制，小规模纳税人按季度申报，截止日期为季度终了后第15日。",
            "applicable_conditions": "柳州市柳江区行政区域内登记注册的增值税小规模纳税人。",
            "exceptions_boundary": "如季度末最后一日为法定休假日（如春节、国庆假期），申报截止日按国家规定顺延；柳江区税务局在征期最后一天可能会临时开放绿色通道，企业可关注通知。",
            "practical_steps": "柳江区小规模纳税人增值税季报流程：（1）季度末在开票系统中完成抄报税；（2）登录广西电子税务局或到柳江区税务局办税服务厅进行增值税及附加税申报；（3）确认申报数据与开票系统一致；（4）如需缴税，在申报期内完成缴款；（5）申报完成后留意是否需要关联企业所得税等关联申报。",
            "risk_warning": "逾期申报：每日万分之五滞纳金，情节严重可处2000元至10000元以下罚款。连续3个月未申报：柳江区税务局可将其转入非正常户管理，影响发票领用和相关涉税事项办理。",
            "scope_level": "scope_local",
            "local_region": "柳州市柳江区",
            "answer_certainty": "certain_clear",
            "keywords": "柳江区,增值税申报期限,小规模纳税人,季报,申报截止日",
            "high_frequency_flag": False,
            "newbie_flag": True,
            "policy_links": [
                {"policy_code": "GOV-VAT-001", "support_type": "support_direct", "support_note": "增值税纳税期限的全国统一规定"},
                {"policy_code": "GOV-Tax-001", "support_type": "support_procedure", "support_note": "税收征收管理法中关于纳税申报期限的规定"}
            ],
            "tags": ["柳江区", "增值税申报", "小规模纳税人", "申报期限"],
            "relations": [{"question_code": "SET-DEC-007", "relation_type": "related"}]
        },
        {
            "question_title": "广西北部湾经济区企业在税务上有什么特殊优惠政策？如何申请？",
            "question_plain": "公司在广西钦州，属于北部湾经济区，想了解有没有针对这个区域的特殊税务优惠政策可以申请？",
            "stage_code": "INV",
            "module_code": "PREF",
            "question_type": "type_what",
            "one_line_answer": "广西北部湾经济区享有西部大开发税收优惠（企业所得税15%）、北部湾专项财政贴息，以及地方分享部分的企业所得税优惠，具体需对照项目是否符合目录要求。",
            "detailed_answer": "广西北部湾经济区（包括南宁、北海、钦州、防城港、玉林、崇左等城市）是我国西部重要的沿海开放区域，在税务上享有以下主要优惠政策：一是西部大开发税收优惠，设在西部地区鼓励类产业企业减按15%征收企业所得税，北部湾经济区在《西部地区鼓励类产业目录》范围内；二是北部湾经济区专项政策，广西区税务局对符合条件的企业给予企业所得税地方分享部分不同程度的减免；三是部分地方税种（房产税、城镇土地使用税等）可按程序申请困难性减免。申请方式：企业对照《西部地区鼓励类产业目录》判断是否属于鼓励类产业，如属于则向主管税务机关提交相关备案材料，申请享受15%优惠税率。",
            "core_definition": "广西北部湾经济区税收优惠：国家为支持广西北部湾经济区开放开发，对在该区域内注册的符合条件的企业，给予企业所得税税率优惠和地方税种减免的系列政策。",
            "applicable_conditions": "在广西北部湾经济区范围内注册的企业；主营业务属于《西部地区鼓励类产业目录》中规定的产业；主营业务收入占企业收入总额70%以上。",
            "exceptions_boundary": "房地产企业（除保障性住房外）、高尔夫球场的建设运营、境外投资者从境内取得的股息红利等不属于鼓励类产业目录范围，不得享受西部大开发税收优惠。位于钦州保税港区的企业另有更大力度的税收优惠，可叠加适用。",
            "practical_steps": "申请西部大开发税收优惠流程：（1）确认企业主营业务属于《西部地区鼓励类产业目录》；（2）准备备案材料：营业执照、公司章程、财务报表、主营业务说明等；（3）向主管税务机关提交《企业所得税优惠备案表》；（4）税务机关审核后出具备案文书；（5）年度申报时在企业所得税年度汇算清缴表中填报优惠信息。",
            "risk_warning": "主营业务不符合目录要求但享受了优惠：税务机关查实后将追缴税款，并按日加收万分之五滞纳金，同时处0.5至5倍罚款。主营业务收入占比不达标（低于70%）：当年不得享受优惠，需在汇算清缴时补税。",
            "scope_level": "scope_local",
            "local_region": "广西壮族自治区",
            "answer_certainty": "certain_conditional",
            "keywords": "广西北部湾,西部大开发,企业所得税优惠,15%税率,鼓励类产业目录",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-001", "support_type": "support_direct", "support_note": "企业所得税法中关于小型微利企业优惠税率和西部大开发优惠税率的规定"},
                {"policy_code": "GOV-CIT-003", "support_type": "support_definition", "support_note": "具体西部大开发税收优惠政策内容"}
            ],
            "tags": ["广西", "北部湾经济区", "企业所得税优惠", "西部大开发", "税收优惠"],
            "relations": []
        },
        {
            "question_title": "柳州市柳江区企业出现税务异常，如何申请移出异常户名单？",
            "question_plain": "公司在柳州市柳江区，因为忘记申报被列入了税务异常户，现在要去税局申请移出异常，需要准备什么材料？",
            "stage_code": "RISK",
            "module_code": "RISK",
            "question_type": "type_procedure",
            "one_line_answer": "柳江区税务异常户移出流程：先补齐所有逾期未申报的税种，然后到柳江区税务局办税服务厅提交解除异常户申请，税务机关核查后解除异常状态。",
            "detailed_answer": "企业被认定为税务异常户（非正常户）后，将在发票领用、税务登记变更、贷款融资等方面受到限制。柳州市柳江区税务局办理异常户解除的程序如下：第一步，企业先在电子税务局或办税服务厅补报所有逾期未申报的税种，包括增值税及附加、企业所得税、个人所得税等，补缴所有应纳税款、滞纳金和罚款（如有）；第二步，准备解除异常户申请材料，包括：营业执照复印件、法定代表人身份证复印件、补申报的完税凭证、情况说明（说明产生异常的原因及整改措施）、税务机关要求的其他材料；第三步，到柳江区税务局办税服务厅提交材料，税务机关对材料的完整性和真实性进行审核，审核通过后，税务机关在系统中解除异常户标识，解除后企业恢复正常税务状态。",
            "core_definition": "税务异常户解除（非正常户认定撤销）：纳税人被认定为非正常户后，向税务机关申请恢复正常税务管理状态的行为，需先消除非正常认定的原因（补申报、缴清税款等）。",
            "applicable_conditions": "已被柳州市柳江区税务局认定为非正常户的企业。",
            "exceptions_boundary": "如有欠税未清缴，必须先清缴全部欠税及滞纳金后方可申请解除；如企业已走逃失联，税务机关将终止对其认定，无法申请解除，只能由登记机关依程序处理。",
            "practical_steps": "柳江区异常户解除流程：（1）补报逾期申报：登录广西电子税务局或到办税服务厅，补充申报所有未按期申报的税种；（2）缴纳欠税和滞纳金：使用银联卡或对公账户转账缴纳；（3）开具情况说明：打印AB文书（财务会计报表及说明），并由法定代表人签署情况说明；（4）提交解除申请：携带全部材料到柳江区税务局办税服务厅综合业务窗口提交；（5）等待核查：税务机关在20个工作日内完成核查；（6）解除认定：核查通过后，税务机关在系统内解除异常状态，企业恢复正常。",
            "risk_warning": "异常状态未解除期间：企业不得领购发票、不得开具发票、税务登记变更受限、无法参与政府采购和招投标。解除后再次被认定异常户：将从重处理，且可能影响企业纳税信用等级。",
            "scope_level": "scope_local",
            "local_region": "柳州市柳江区",
            "answer_certainty": "certain_clear",
            "keywords": "柳江区,非正常户,异常户解除,补申报,纳税信用",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "TAX-POL-005", "support_type": "support_direct", "support_note": "非正常户认定标准和解除条件"},
                {"policy_code": "GOV-Tax-001", "support_type": "support_procedure", "support_note": "税收征收管理法中关于纳税人信用管理的规定"}
            ],
            "tags": ["柳江区", "非正常户", "纳税信用", "税务异常", "补申报"],
            "relations": []
        },
        {
            "question_title": "广西小规模纳税人季度销售额未超过30万元，免征增值税的优惠如何适用？",
            "question_plain": "公司在广西桂林，是小规模纳税人，季度销售额大概在25万元左右，听说不超过30万元不用缴增值税，是这样吗？具体怎么操作？",
            "stage_code": "OPR",
            "module_code": "PREF",
            "question_type": "type_clarify",
            "one_line_answer": "自2023年起，小规模纳税人季度销售额未超过30万元（月销售额未超过10万元）的，免征增值税，但需正常申报，申报时将销售额填入小微企业免税销售额栏次。",
            "detailed_answer": "根据国家税务总局的规定，自2023年1月1日起，小规模纳税人发生增值税应税销售行为，合计月销售额未超过10万元（季度销售额未超过30万元）的，免征增值税。该政策的适用要点如下：第一，免税的是增值税本身，城市维护建设税、教育费附加和地方教育费附加随增值税减免而减免（即所谓的'三税联动'减免）；第二，免税不等于不申报，小规模纳税人仍须按期进行增值税申报，只是在申报表中将免税销售额填入'小微企业免税销售额'栏次；第三，如小规模纳税人开具的是增值税普通发票（免税或不免税），则该部分销售额可享受免税；如开具的是增值税专用发票，则该部分销售额不能享受免税（专用发票不免税）。广西壮族自治区的小规模纳税人统一适用该政策，无地方特殊规定。",
            "core_definition": "小规模纳税人免征增值税优惠：月销售额（或季度销售额）未超过规定标准的增值税小规模纳税人，免予征收增值税的税收优惠政策。",
            "applicable_conditions": "增值税小规模纳税人；一个季度内累计开票销售额（不含税）未超过30万元；所有销售额均为增值税应税销售额。",
            "exceptions_boundary": "个体工商户小规模纳税人季度销售额不超过30万元适用同样政策；开具了增值税专用发票的部分不享受免税（即使季度总额在30万元以下，专用发票部分仍须按征收率计算纳税）；差额征税的小规模纳税人，以差额后的销售额确定是否享受优惠。",
            "practical_steps": "申报流程：（1）季度结束后，在开票系统中进行抄报税；（2）登录广西电子税务局，进入【我要办税】-【税费申报及缴纳】-【增值税及附加税费申报】；（3）将销售额填入【第10栏：小微企业免税销售额】（个体工商户填入第11栏）；（4）系统自动带出免税金额，无需缴纳增值税；（5）附加税费（城市维护建设税等）如符合小微企业条件也同步免征。",
            "risk_warning": "季度销售额超过30万元后，全部销售额（含免税部分的普通发票）须按征收率计算缴纳增值税，不能只对超过部分补税。错误填报申报表导致未缴或少缴税：构成偷税，税务机关可追缴并处罚款。",
            "scope_level": "scope_local",
            "local_region": "广西壮族自治区",
            "answer_certainty": "certain_clear",
            "keywords": "广西,小规模纳税人,免税销售额,季度30万元,增值税优惠",
            "high_frequency_flag": True,
            "newbie_flag": True,
            "policy_links": [
                {"policy_code": "GOV-VAT-001", "support_type": "support_direct", "support_note": "小规模纳税人增值税免税标准和申报规定"},
                {"policy_code": "GOV-VAT-003", "support_type": "support_procedure", "support_note": "小规模纳税人增值税申报表填表说明"}
            ],
            "tags": ["广西", "小规模纳税人", "免税销售额", "增值税优惠", "新手必看"],
            "relations": []
        },
        {
            "question_title": "柳州市柳江区跨区域经营的企业，税务登记和申报地点如何确定？",
            "question_plain": "公司注册在柳州市柳江区，但主要经营场所在南宁市，在南宁有多个项目，税务上应该在柳江区申报还是在南宁申报？",
            "stage_code": "OPR",
            "module_code": "REG",
            "question_type": "type_clarify",
            "one_line_answer": "柳江区注册的企业，税务管理关系在柳江区税务局，无论经营场所是否在南宁，增值税和企业所得税均在柳江区申报缴纳；南宁市项目如涉及项目所在地预缴，则需在项目所在地预缴部分税款。",
            "detailed_answer": "税务登记注册地与经营地不一致时的税务处理规则如下：公司的税务登记在柳州市柳江区，主管税务机关为柳江区税务局，公司的增值税、企业所得税、个人所得税等主要税种均应在柳江区税务局申报缴纳。但需注意以下特殊情况：一是建筑服务增值税：公司在南宁的建筑项目，属于跨县（区）提供建筑服务，须在南宁市项目所在地国家税务局预缴增值税（按项目实际收款或开具发票金额计算预缴），预缴后再在柳江区税务局进行纳税申报；二是企业所得税：除另有规定外，企业所得税由登记注册地税务机关统一管理，南宁项目的企业所得税应并入柳江区总机构统一申报，但如为独立核算的分公司，则须单独申报。",
            "core_definition": "税务登记地与经营地分离：企业税务登记在A地，经营场所在B地，主体税种仍在登记地申报缴纳，跨区域经营项目须在项目所在地预缴部分税种。",
            "applicable_conditions": "注册地在柳州市柳江区，经营活动在广西壮族自治区其他地市的企业。",
            "exceptions_boundary": "南宁如有独立核算的分公司，分公司须在南宁市主管税务机关单独申报企业所得税（须先向柳江区总机构所在地税务机关申请）；跨省经营（如在广东设立项目部）则须遵循跨省经营的相关规定，包括企业所得税汇总纳税或独立申报的认定。",
            "practical_steps": "柳江区企业在南宁经营的处理步骤：（1）在南宁取得项目后，向柳江区税务局报告外出经营活动情况（合同、地址、期限等）；（2）如为建筑服务项目，在南宁项目所在地税务机关进行增值税预缴（携带合同、项目登记证明等材料）；（3）在柳江区进行企业所得税年度汇算清缴，如为总分支机构模式则汇总申报；（4）在外经证到期前向柳江区税务局办理延期或注销。",
            "risk_warning": "未按规定在外地经营进行税务报验登记：项目所在地税务机关可按偷税处理，要求补缴税款并处罚款。建筑服务未在项目所在地预缴增值税：主管税务机关（柳江区）查实后将追缴，并按日加收滞纳金。",
            "scope_level": "scope_local",
            "local_region": "柳州市柳江区",
            "answer_certainty": "certain_conditional",
            "keywords": "柳江区,跨区域经营,税务登记地,建筑服务,预缴增值税,外出经营证明",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-Tax-002", "support_type": "support_direct", "support_note": "跨区域经营税务登记和申报的相关规定"},
                {"policy_code": "GOV-VAT-001", "support_type": "support_procedure", "support_note": "建筑服务跨区域经营增值税预缴规定"}
            ],
            "tags": ["柳江区", "跨区域经营", "建筑服务", "预缴增值税", "外出经营"],
            "relations": []
        },
        {
            "question_title": "广西自由贸易试验区（南宁、钦州港片区）企业，享受哪些独特的税务优惠？",
            "question_plain": "公司在广西自贸区南宁片区注册，想了解有没有针对自贸区企业的特殊税务优惠政策？",
            "stage_code": "INV",
            "module_code": "PREF",
            "question_type": "type_what",
            "one_line_answer": "广西自贸区享有企业所得税'两免三减半'、高端人才个人所得税补贴、以及国际贸易、融资租赁等方面的特殊税收优惠，需满足入驻条件和行业目录要求。",
            "detailed_answer": "中国（广西）自由贸易试验区包括南宁片区、钦州港片区和崇左片区三个区域，各片区在税务政策上既有自贸区通用政策，也有结合地方产业特色的专项政策。主要优惠政策包括：一是企业所得税优惠，对设立在自贸区内的鼓励类产业企业，在享受西部大开发15%优惠税率的基础上，还可叠加享受广西区定的'两免三减半'地方优惠（前两年免征地方分享部分，后三年减半）；二是个人所得税优惠，对在自贸区工作的高端人才和紧缺人才，其个人所得税地方分享部分由当地政府予以补贴；三是关税优惠，钦州港片区对进口设备、原材料等有特定的关税减免政策；四是跨境税收服务，自贸区企业享有更便捷的出口退税服务和跨境投资税收服务。申请方式：企业须先向自贸区管委会确认是否符合入区条件，再向主管税务机关提交相关材料申请优惠备案。",
            "core_definition": "中国（广西）自由贸易试验区税收优惠：国家为支持广西自贸区建设，在企业所得税、个人所得税、进出口关税等方面给予的系列特殊税收优惠政策。",
            "applicable_conditions": "在中国（广西）自由贸易试验区（南宁片区、钦州港片区、崇左片区）注册并实际运营的企业；主营业务属于自贸区鼓励类产业目录范围；符合高端人才或紧缺人才认定条件（个人所得税优惠适用）。",
            "exceptions_boundary": "自贸区优惠政策与西部大开发政策可以叠加，但与某些特定区域政策（如民族自治区免税政策）不能叠加享受；房地产企业不在自贸区企业所得税优惠范围内；钦州港片区的关税优惠仅适用于进口自用设备等特定物资。",
            "practical_steps": "申请广西自贸区税务优惠流程：（1）向自贸区管委会确认是否符合入区资格和主营业务范围；（2）向广西区税务局或片区所在地税务局提交《企业所得税优惠备案表》及入区证明材料；（3）准备证明材料：营业执照、公司章程、财务报表、主营业务说明、员工名册及学历证明（人才补贴用）；（4）税务机关审核后出具税收优惠备案文书；（5）年度申报时在对应申报表中填报优惠信息。",
            "risk_warning": "入区后主营业务发生变化不再属于鼓励类产业：优惠资格将被取消，税务机关有权追缴已减免的税款。高端人才个税补贴未如实申报：企业及个人可能被要求退还补贴，并承担相应法律责任。",
            "scope_level": "scope_local",
            "local_region": "广西壮族自治区",
            "answer_certainty": "certain_conditional",
            "keywords": "广西自贸区,企业所得税优惠,个人所得税补贴,钦州港,南宁片区,西部大开发",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-003", "support_type": "support_direct", "support_note": "企业所得税优惠税率和民族自治区减免政策的适用规则"},
                {"policy_code": "GOV-CIT-001", "support_type": "support_definition", "support_note": "西部大开发企业所得税15%优惠税率的规定"}
            ],
            "tags": ["广西", "自贸区", "企业所得税优惠", "个人所得税补贴", "钦州港", "税收优惠"],
            "relations": []
        },
        {
            "question_title": "柳州市柳江区企业想申请农产品收购发票，应当如何办理？",
            "question_plain": "公司在柳江区有农业合作社，想给自己开具农产品收购发票收购农户的农产品，这个发票要怎么办理？",
            "stage_code": "OPR",
            "module_code": "INV",
            "question_type": "type_procedure",
            "one_line_answer": "柳江区企业需先向柳江区税务局申请农产品收购发票的领用资格，审核通过后才能领购农产品收购发票，并按规定开具和申报抵扣进项税。",
            "detailed_answer": "农产品收购发票是增值税一般纳税人向农户收购自产农产品时自行开具的发票，可以按规定计算抵扣进项税额（按收购发票上注明的农产品买价和9%或10%的扣除率计算抵扣进项税）。柳州市柳江区企业申请农产品收购发票的程序如下：首先，申请企业须为增值税一般纳税人（不具有一般纳税人资格的小规模纳税人不得自行开具收购发票，须到税务机关代开）；其次，企业须向柳江区税务局提交书面申请，说明收购农产品的业务背景、收购对象（农户范围）、收购业务流程、核算方式等信息；税务机关审核企业的会计核算情况（是否单独设置'农产品收购'科目、是否建立农户信息档案等）；审核通过后，税务机关在增值税发票管理系统中维护企业的农产品收购发票开票资格；企业领购发票后，须按要求填写'购买方为农户'的信息，通过系统开具收购发票。",
            "core_definition": "农产品收购发票：一般纳税人向农业生产者个人（非企业、非个体工商户）收购其自产农产品时，自行开具的可抵扣进项税的增值税发票，票面金额按买价和扣除率计算进项税。",
            "applicable_conditions": "具有增值税一般纳税人资格的企业；存在向农业生产者个人收购自产农产品业务；会计核算健全，能够准确归集农产品收购成本和进项税额。",
            "exceptions_boundary": "向合作社、农业企业（非个人）收购农产品不得开具收购发票，须取得销售方开具的增值税发票；小规模纳税人不得自行开具农产品收购发票，须到税务机关申请代开；粮食、棉花等特定农产品适用不同的扣除率。",
            "practical_steps": "柳江区农产品收购发票申请步骤：（1）确认企业为增值税一般纳税人；（2）到柳江区税务局办税服务厅提交书面申请（说明业务背景、农户范围、收购规模）；（3）准备材料：营业执照、一般纳税人认定文书、收购业务流程说明、会计核算方式说明；（4）税务机关审核会计核算情况，核实是否建立农户信息档案和'农产品收购'专用账簿；（5）审核通过后在税控系统中增加农产品收购发票票种；（6）领购发票后，按系统要求填写农户身份信息和收购价格，开具收购发票。",
            "risk_warning": "虚构收购业务开具收购发票：构成虚开增值税发票罪，最高可判无期徒刑。扩大收购范围（向非农业生产者开具收购发票）：进项税额须转出，并补缴增值税和企业所得税，情节严重构成虚开。",
            "scope_level": "scope_local",
            "local_region": "柳州市柳江区",
            "answer_certainty": "certain_clear",
            "keywords": "柳江区,农产品收购发票,进项税抵扣,农业生产者,一般纳税人",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-002", "support_type": "support_direct", "support_note": "农产品收购发票的开具范围和进项税额抵扣规定"},
                {"policy_code": "GOV-VAT-001", "support_type": "support_definition", "support_note": "增值税条例中关于农产品扣除率的规定"}
            ],
            "tags": ["柳江区", "农产品收购发票", "进项税抵扣", "增值税发票", "农业"],
            "relations": []
        }
    ]
}

def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def generate_code(conn, stage_code, module_code):
    prefix = f"{stage_code}-{module_code}-"
    cur = conn.cursor()
    cur.execute(
        "SELECT question_code FROM question_master WHERE question_code LIKE ? ORDER BY question_code DESC LIMIT 1",
        (f"{prefix}%",)
    )
    row = cur.fetchone()
    if not row:
        return f"{prefix}001"
    last = row[0]
    num = int(last.split("-")[-1])
    return f"{prefix}{num+1:03d}"

def now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def resolve_policy_id(conn, policy_code):
    cur = conn.cursor()
    cur.execute("SELECT id FROM policy_basis WHERE policy_code = ?", (policy_code,))
    r = cur.fetchone()
    return r['id'] if r else None

def main():
    data = batch_local
    conn = get_conn()
    imported = 0
    skipped = 0

    for q in data["questions"]:
        code = generate_code(conn, q["stage_code"], q["module_code"])
        now_ts = now()

        try:
            conn.execute("""INSERT INTO question_master
                (question_code, question_title, question_plain, stage_code, module_code,
                 question_type, one_line_answer, detailed_answer, core_definition,
                 applicable_conditions, exceptions_boundary, practical_steps, risk_warning,
                 scope_level, local_region, answer_certainty, keywords, high_frequency_flag, newbie_flag,
                 status, version_no, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'active','v1.0',?,?)""",
                (code, q["question_title"], q["question_plain"], q["stage_code"], q["module_code"],
                 q["question_type"], q["one_line_answer"], q["detailed_answer"], q["core_definition"],
                 q["applicable_conditions"], q["exceptions_boundary"], q["practical_steps"], q["risk_warning"],
                 q["scope_level"], q.get("local_region",""), q["answer_certainty"], q["keywords"],
                 q["high_frequency_flag"], q["newbie_flag"],
                 now_ts, now_ts))
        except Exception as e:
            print(f"  跳过(主表): {code} {q['question_title'][:20]} -> {e}")
            skipped += 1
            continue

        qid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        link_count = 0
        for pl in q.get("policy_links", []):
            pol_id = resolve_policy_id(conn, pl["policy_code"])
            if pol_id:
                conn.execute("""INSERT INTO question_policy_link
                    (question_id, policy_id, support_type, support_note, display_order)
                    VALUES (?,?,?,?,?)""",
                    (qid, pol_id, pl["support_type"], pl.get("support_note",""), link_count))
                link_count += 1

        for tag in q.get("tags", []):
            cur = conn.cursor()
            cur.execute("SELECT id FROM tag_dict WHERE tag_name = ?", (tag,))
            tr = cur.fetchone()
            if tr:
                conn.execute("INSERT OR IGNORE INTO question_tag_link (question_id, tag_id) VALUES (?,?)", (qid, tr['id']))

        for rel in q.get("relations", []):
            cur = conn.cursor()
            cur.execute("SELECT id FROM question_master WHERE question_code = ?", (rel["question_code"],))
            rr = cur.fetchone()
            if rr:
                conn.execute("""INSERT INTO question_relation
                    (question_id, related_id, relation_type, display_order)
                    VALUES (?,?,?,1)""",
                    (qid, rr['id'], rel["relation_type"]))

        conn.execute("""INSERT INTO question_update_log
            (question_id, version_no, update_date, update_type,
             update_reason, updated_by, reviewed_by, change_summary)
            VALUES (?, 1, ?, 'create', ?, 'batch_import', '', ?)""",
            (qid, now_ts, "批量导入初始数据", f"创建问题 {code}"))

        print(f"  +{code} | {q['question_title'][:35]}... | local:{q.get('local_region','')} | links:{link_count}")
        imported += 1

    conn.commit()
    conn.close()
    print(f"\n导入完成: {imported}条成功, {skipped}条跳过")

if __name__ == "__main__":
    main()
