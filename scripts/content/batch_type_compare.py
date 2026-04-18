#!/usr/bin/env python3
"""
批量导入 type_compare（对比型）问题 - 12条新增
"""
import json, sqlite3, datetime, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"

# 12条对比型问题，涵盖多个模块
batch_compare = {
    "questions": [
        {
            "question_title": "税务登记中的设立登记与变更登记，税务处理有何本质不同？",
            "question_plain": "企业完成工商设立登记后，税务上需要做什么？和后续发生变更时的税务处理有何本质区别？",
            "stage_code": "SET",
            "module_code": "REG",
            "question_type": "type_compare",
            "one_line_answer": "设立登记是从无到有建立税务档案，变更登记是在已有档案上更新信息；设立登记触发税种认定和初始申报，变更登记仅在信息变化时申报。",
            "detailed_answer": "设立登记（税务报到）是企业首次与税务机关建立关系，需要提供营业执照、法人信息、经营地址等基础材料，税务机关据此建立纳税人档案并认定税种、核定发票种类和数量。变更登记则是企业已有税务档案的信息发生变动（如地址、法定代表人了、经营范围等），仅需向税务机关申报更新信息，不触发新的税种认定。两者的核心区别在于：设立登记是从0到1建立关系，变更登记是对现有关系的信息更新。",
            "core_definition": "设立税务登记：企业、个体工商户自领取营业执照之日起30日内，向税务机关申报办理税务登记，建立纳税人档案。变更税务登记：税务登记内容发生变化时，向税务机关申报办理税务登记变更。",
            "applicable_conditions": "设立登记：领取营业执照后30日内必须办理。变更登记：登记内容变化后30日内办理（有些变更如法人代表可先行工商变更再更新税务）。",
            "exceptions_boundary": "两证整合后（营业执照与税务登记证合一），设立登记流程简化，但法律义务不变；非独立核算的分公司也需要税务登记；境外企业在中国境内发生应税行为同样需办理税务登记。",
            "practical_steps": "设立登记步骤：（1）工商领取营业执照；（2）到主管税务机关报到；（3）提交营业执照、法人身份证、经营地址证明等材料；（4）填写《税务登记表》；（5）税务机关核发纳税人识别号（税号）；（6）认定税种和发票种类。\n变更登记步骤：（1）核实变更内容；（2）准备变更证明材料；（3）向主管税务机关申报；（4）窗口更新信息或网上自助办理。",
            "risk_warning": "设立登记逾期未办理：处2000元以下罚款，情节严重处2000～10000元罚款；可能影响发票领用和申报资格。变更登记逾期：税务机关可按规定处理；地址变更未更新可能影响发票认证和信件接收，导致税务风险。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "设立登记,变更登记,税务报到,营业执照,税种认定,纳税人识别号",
            "high_frequency_flag": True,
            "newbie_flag": True,
            "policy_links": [
                {"policy_code": "GOV-Tax-001", "support_type": "support_direct", "support_note": "第15条，企业自领取营业执照30日内申报税务登记"},
                {"policy_code": "GOV-Tax-007", "support_type": "support_procedure", "support_note": "变更登记时限要求"}
            ],
            "tags": ["税务登记", "设立登记", "变更登记", "新手必看"],
            "relations": []
        },
        {
            "question_title": "小规模纳税人与一般纳税人，在税率、申报和发票使用上有何核心差异？",
            "question_plain": "公司刚成立，该申请小规模纳税人还是一般纳税人？两者在税务处理上有什么主要区别？",
            "stage_code": "OPR",
            "module_code": "TAX",
            "question_type": "type_compare",
            "one_line_answer": "小规模纳税人适用简易计税（征收率3%或5%），按季度申报；一般纳税人适用一般计税（税率13%/9%/6%），按月度申报，可抵扣进项税额。",
            "detailed_answer": "小规模纳税人与一般纳税人的核心差异体现在三个方面：计税方式上，小规模按销售额乘以征收率简易计算，不抵扣进项税；一般纳税人按销项税额减进项税额的差额计算。申报周期上，小规模纳税人通常按季度申报（1/4/7/10月），一般纳税人按月度申报。发票使用上，小规模纳税人只能开具增值税普通发票（或通用机打发票），如需开具专用发票需到税务机关代开；一般纳税人可自行开具增值税专用发票和普通发票，且取得的增值税专用发票可抵扣进项税。",
            "core_definition": "小规模纳税人：年应税销售额500万元以下的增值税纳税人，适用简易计税方法。一般纳税人：年应税销售额超过500万元，或会计核算健全、能提供准确税务资料的企业，适用一般计税方法。",
            "applicable_conditions": "小规模纳税人：年销售额500万元以下，或新成立企业未申请认定一般纳税人。一般纳税人：年销售额超过500万元，或主动申请认定（需会计核算健全）。",
            "exceptions_boundary": "新成立企业默认小规模，但可随时申请转为一般纳税人（认定制）；住宿业、鉴证咨询业等行业小规模纳税人可自行开具专用发票（无需代开）；一般纳税人不得再转为小规模（除国家另有规定外）。",
            "practical_steps": "选择小规模路径：先完成税务登记，默认按小规模纳税人管理；如需代开专票，到主管税务机关办理。\n选择一般纳税人路径：（1）向主管税务机关提交《增值税一般纳税人资格登记表》；（2）认定后安装税控设备；（3）领购增值税专用发票；（4）按月申报增值税及附加。",
            "risk_warning": "小规模虚开专票风险：即使为他人开具与实际经营不符的专票，按虚开专票处理，可能被移交司法机关。一般纳税人取得虚专票：已抵扣的进项税额需转出，并可能被定性为偷税。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "小规模纳税人,一般纳税人,税率,申报周期,进项税额抵扣,专用发票,普通发票",
            "high_frequency_flag": True,
            "newbie_flag": True,
            "policy_links": [
                {"policy_code": "GOV-VAT-001", "support_type": "support_direct", "support_note": "小规模纳税人认定标准和征收率规定"},
                {"policy_code": "GOV-VAT-002", "support_type": "support_direct", "support_note": "一般纳税人资格认定和进项税额抵扣规则"}
            ],
            "tags": ["增值税", "小规模纳税人", "一般纳税人", "发票", "申报", "新手必看"],
            "relations": []
        },
        {
            "question_title": "增值税专用发票与普通发票，在税务处理和法律效力上有何本质区别？",
            "question_plain": "开出去的发票有专票和普票之分，两者有什么区别？收到发票的一方处理一样吗？",
            "stage_code": "OPR",
            "module_code": "INV",
            "question_type": "type_compare",
            "one_line_answer": "专用发票是增值税一般纳税人的扣税凭证，可抵扣进项税；普通发票不能抵扣进项税，只能作为成本费用凭证入账。两者都是合法凭证，但用途不同。",
            "detailed_answer": "增值税专用发票与普通发票的核心区别在于可抵扣性：专用发票的购买方（必须是一般纳税人）可凭票上注明的进项税额抵扣销项税，而普通发票无论开给谁都不能抵扣进项税。从版式看，专用发票有购买方和销售方的完整税务信息（纳税人识别号、开户行、账号、地址），普通发票信息相对简化。从开具资格看，小规模纳税人可到税务机关申请代开专用发票（征收率3%），但自己不能自行开具；一般纳税人可自行开具两种发票。从法律效力看，两者都是合法凭证，但专用发票一旦虚开，按刑法第205条追究责任，处罚更严厉。",
            "core_definition": "增值税专用发票：增值税一般纳税人销售货物、提供应税劳务或应税服务时开具的，可作为购买方抵扣进项税款的合法凭证。增值税普通发票：不能抵扣进项税，只能作为销售方依法纳税、购买方计入成本费用的凭证。",
            "applicable_conditions": "专用发票：只能开具给增值税一般纳税人（小规模如需专票须到税务机关代开）。普通发票：可开具给任意购买方，包括自然人、小规模企业。",
            "exceptions_boundary": "商业企业零售烟、酒、化妆品等消费品的，不得开具增值税专用发票（政策另有规定除外）；农产品收购发票、旅客运输发票等可计算抵扣进项税，性质类似普通发票但有抵扣效力。",
            "practical_steps": "销售方开专票：（1）确认购买方为一般纳税人；（2）在开票系统中选择专用发票填开；（3）完整填写购买方名称、纳税人识别号、开户行、账号、地址电话；（4）密码区在打印后生成。\n销售方开普票：（1）普通发票填开相对简单；（2）购买方名称和纳税人识别号为必填项（给个人或小规模可不填识别号）。",
            "risk_warning": "虚开专票风险最高：即使是善意取得虚开发票，已抵扣进项税需转出补税；恶意虚开构成犯罪，最高可判无期徒刑。普票风险相对较低，但虚开普票（金额较大或情节严重）同样可构成虚开发票罪。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "专用发票,普通发票,进项税额抵扣,虚开发票,一般纳税人,小规模纳税人",
            "high_frequency_flag": True,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-002", "support_type": "support_direct", "support_note": "专用发票作为抵扣凭证的法律规定"},
                {"policy_code": "GOV-VAT-004", "support_type": "support_procedure", "support_note": "专用发票和普通发票的开具范围和填开要求"}
            ],
            "tags": ["增值税", "专用发票", "普通发票", "进项抵扣", "虚开发票"],
            "relations": []
        },
        {
            "question_title": "查账征收与核定征收，在计税方式和适用情形上有何不同？",
            "question_plain": "企业所得税为什么有查账征收和核定征收两种方式？它们在税负上有何差异？",
            "stage_code": "OPR",
            "module_code": "DEC",
            "question_type": "type_compare",
            "one_line_answer": "查账征收按账簿记载的真实利润计算应税所得，需规范会计核算；核定征收按税务机关核定的应税所得率推算利润，适用于账簿不健全的企业。",
            "detailed_answer": "查账征收（也叫查账征收方式A）适用于账簿、凭证、财务核算健全的企业，以账面上记载的收入减去允许扣除的成本费用后的余额（利润）乘以适用税率计算应纳税额。核定征收（包括核定应税所得率和定额征收两种）适用于账簿不健全、无法准确核算收入或成本的企业，税务机关根据行业特点、经营规模等因素核定一个应税所得率，用收入总额乘以应税所得率得出应税所得，再乘以适用税率（或按定额直接核定税额）。两者的根本差异在于：查账征收基于真实账簿数据，核定征收基于税务机关的推定数据。",
            "core_definition": "查账征收：企业所得税的一种征收方式，适用于账证健全、能准确核算收入和成本费用的纳税人，以实际利润为计税依据。核定征收：企业所得税的另一种征收方式，适用于账证不全、无法准确核算的纳税人，税务机关依法核定其应税所得率或税额。",
            "applicable_conditions": "查账征收：会计核算规范，账簿、凭证齐全，能真实反映经营情况。核定征收：会计核算不健全，无法准确查账；或连续亏损且不愿主动调整；或抗拒提供账簿凭证。",
            "exceptions_boundary": "特殊行业（如定率征收的加油站）按行业特殊规定执行；采用核定征收方式的企业，当年符合条件的可申请转为查账征收；核定征收企业不得享受小型微利企业的低税率优惠（部分地区规定）。",
            "practical_steps": "查账征收下的企业税务处理：（1）规范设置账簿，确保收入、成本、费用真实完整；（2）按季度预缴企业所得税，年度汇算清缴；（3）保存完整的凭证和账簿以备检查。\n核定征收下的企业税务处理：（1）收到税务机关核定的应税所得率后按公式计算；（2）收入发生明显变化可申请调整应税所得率；（3）年度终了无需进行复杂的汇算清缴调整。",
            "risk_warning": "查账征收风险：账簿不规范、凭证缺失会导致纳税调整增多，严重时可能被认定为偷税。核定征收风险：即使实际亏损也需按核定金额纳税；转让定价调查时核定征收不能成为抗辩理由。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_conditional",
            "keywords": "查账征收,核定征收,企业所得税,应税所得率,会计核算",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-001", "support_type": "support_direct", "support_note": "企业所得税征收方式的法律依据"},
                {"policy_code": "GOV-CIT-002", "support_type": "support_procedure", "support_note": "核定征收应税所得率的核定标准"}
            ],
            "tags": ["企业所得税", "查账征收", "核定征收", "应税所得率"],
            "relations": []
        },
        {
            "question_title": "增值税月报与季报，在申报频率和现金流量上有何不同影响？",
            "question_plain": "听说小规模纳税人可以按季度申报增值税，一般纳税人要按月申报，这两种方式对企业管理有什么不同影响？",
            "stage_code": "OPR",
            "module_code": "DEC",
            "question_type": "type_compare",
            "one_line_answer": "月报（一般纳税人）申报频率高、留抵税额周期短；季报（小规模纳税人）申报压力小但单次税额可能较大，现金流管理逻辑不同。",
            "detailed_answer": "月报与季报的区别不仅是申报频率不同，更影响企业的现金流安排和税务管理节奏。一般纳税人按月申报增值税，每月需确认销项税额、可抵扣进项税额，计算应纳税额并及时缴款，进项税抵扣周期短（当月认证当月抵扣），留抵税额不会积累太久。小规模纳税人按季度申报，1/4/7/10月为申报期，单次申报金额等于三个月销售额乘以征收率之和；如季度销售额较小，可能整个季度无需缴税，但单笔税额相对集中。两种方式对企业的财务管理要求也不同：月报企业需要更精细的进项税管理，季报企业需要对季度收入做好预测和规划。",
            "core_definition": "增值税月报：一般纳税人按规定在每月终了后15日内申报缴纳增值税。增值税季报：小规模纳税人在每季度终了后15日内申报缴纳增值税（申报当期实现的增值税）。",
            "applicable_conditions": "月报：增值税一般纳税人。季报：增值税小规模纳税人（也可自愿申请一般纳税人后改为月报）。",
            "exceptions_boundary": "小规模纳税人申请自行开具专用发票后，仍按季度申报（部分行业如住宿业、鉴证咨询业小规模可申请为季报）；一般纳税人如果当月销项小于进项形成留抵税额，可不缴增值税，留抵税额继续结转下月抵扣。",
            "practical_steps": "月报管理要点：（1）每月初认证进项发票；（2）每月按时抄报税；（3）进项税归集和比对；（4）留抵税额管理。\n季报管理要点：（1）季度内做好收入台账；（2）季度末测算应纳税额；（3）季报期集中处理发票认证和归集；（4）避免季度末集中开票导致税负突增。",
            "risk_warning": "月报逾期处罚：每日万分之五滞纳金，情节严重可处2000元以下至10000元以下罚款。季报逾期：同月报处罚标准，但因周期长更容易遗忘；连续三个季度未申报可能纳入非正常户管理。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "增值税申报,月报,季报,一般纳税人,小规模纳税人,申报周期",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-001", "support_type": "support_direct", "support_note": "增值税申报期限的法律规定"},
                {"policy_code": "GOV-VAT-002", "support_type": "support_procedure", "support_note": "进项税额抵扣时限规定"}
            ],
            "tags": ["增值税", "申报期限", "月报", "季报", "一般纳税人", "小规模纳税人"],
            "relations": []
        },
        {
            "question_title": "免税收入与不征税收入，在企业所得税处理上有何本质区别？",
            "question_plain": "同样是企业收到的钱，为什么有的计入免税收入，有的不计入应税收入？两者在税务处理上有何不同？",
            "stage_code": "INV",
            "module_code": "PREF",
            "question_type": "type_compare",
            "one_line_answer": "免税收入属于应税范畴但给予减免优惠（如国债利息），不征税收入本身就不属于应税范畴（如财政拨款）；两者都不缴企业所得税，但性质和后续处理不同。",
            "detailed_answer": "免税收入与不征税收入的核心区别在于'血缘'不同：免税收入源自市场经营行为，本身属于企业所得税的应税收入，但国家给予税收优惠使其免予纳税（如国债利息收入、符合条件的居民企业之间的股息红利等）；不征税收入不是因为优惠而免税，而是其本身就不在应税收入范围之内（如财政拨款、行政事业性收费、政府性基金等）。在税务处理上，免税收入需要申报但填写在免税列，相应成本费用可以正常扣除；不征税收入的对应成本费用往往不能税前扣除（如用财政资金购建资产，相关折旧不得扣除）。此外，免税收入的政策稳定，不征税收入的认定往往依赖政府文件。",
            "core_definition": "免税收入：属于应税收入但根据税收法律法规规定免予征收企业所得税的收入。不征税收入：不属于企业所得税应税收入范围的收入，即从源头就不是'应税'的。",
            "applicable_conditions": "免税收入：国债利息收入、符合条件的居民企业之间股息红利、符合条件的非营利组织收入等。不征税收入：财政拨款（除专项用途财政资金外）、行政事业性收费、政府性基金等。",
            "exceptions_boundary": "专项用途的财政性资金（如科技部创新基金），如符合条件可作为不征税收入，其支出不得扣除；如作为免税收入则对应的成本费用可以扣除。不征税收入5年内未使用完的，应计入第6年的应税收入。",
            "practical_steps": "免税收入处理：（1）确认是否符合免税条件；（2）在年度汇算清缴时填入免税收入明细表；（3）对应的成本费用正常核算和扣除。\n不征税收入处理：（1）取得时确认是否属于不征税收入；（2）用于支出形成的资产，其折旧或费用不得税前扣除；（3）如已计入不征税收入后改变用途，应按规定补税。",
            "risk_warning": "将应税收入错误填列不征税收入：会导致成本费用不得扣除风险（双重损失）。免税收入不符合条件：税务机关有权调整，要求补税并加收滞纳金和罚款。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_conditional",
            "keywords": "免税收入,不征税收入,企业所得税,财政拨款,国债利息,股息红利",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-001", "support_type": "support_direct", "support_note": "免税收入和不征税收入的法定定义和处理规则"},
                {"policy_code": "GOV-CIT-003", "support_type": "support_definition", "support_note": "具体免税收入类型和条件"}
            ],
            "tags": ["企业所得税", "免税收入", "不征税收入", "税收优惠"],
            "relations": []
        },
        {
            "question_title": "居民企业与非居民企业，在企业所得税适用税率和征收方式上有何不同？",
            "question_plain": "同样是企业，为什么有的企业适用25%税率，有的适用10%或20%？有什么判断标准？",
            "stage_code": "FIN",
            "module_code": "CIT",
            "question_type": "type_compare",
            "one_line_answer": "居民企业就其来源于境内、境外的所得全部纳税，适用25%基本税率（或优惠税率）；非居民企业仅就来源于境内的所得纳税，适用25%税率或10%预提税率（股息红利、利息、特许权使用费）。",
            "detailed_answer": "居民企业和非居民企业的核心区别在于纳税义务的范围。居民企业（包括依法在中国境内成立的企业，以及实际管理机构在中国境内的境外注册企业）对其来源于境内和境外的全部所得缴纳企业所得税，适用25%基本税率（符合条件的小型微利企业适用20%优惠税率，高新技术企业适用15%税率）。非居民企业（在中国境内未设立机构场所，或机构场所与所得无实际联系的境外注册企业）仅就其来源于中国境内的所得纳税，适用25%税率（机构场所所得）或10%预提税率（股息红利、利息、特许权使用费，双边税收协定可降低）。此外，非居民企业在中国境内设立机构场所的，其来源于该机构场所的所得，以及发生在中国境外但与其机构场所有实际联系的所得，也需要在中国缴纳企业所得税。",
            "core_definition": "居民企业：依法在中国境内成立，或实际管理机构在中国境内的企业。非居民企业：在中国境内未设立机构场所，或取得的所得与机构场所无实际联系的企业。",
            "applicable_conditions": "居民企业：在中国境内注册成立；或在境外注册但实际管理机构在中国境内。非居民企业：在境外注册且在中国境内未设立机构场所；或虽设立机构场所但所得与其无实际联系。",
            "exceptions_boundary": "境外注册但实际管理机构在境内的居民企业认定：实际管理机构是指对企业生产经营、人员、账务、财产等实施实质性全面管理和控制的机构；单纯有董事会开会不构成实际管理机构。",
            "practical_steps": "居民企业所得税处理：（1）确认纳税主体身份；（2）境内外所得合并计算应税所得；（3）境外所得已在境外缴纳的所得税可按规定抵免（限额抵免）；（4）年度汇算清缴。\n非居民企业税务处理：（1）确认所得类型（股息/利息/特许权使用费/经营所得）；（2）源泉扣缴或自行申报；（3）如涉及协定税率，提供税收居民身份证明享受协定待遇。",
            "risk_warning": "非居民企业股息红利等消极所得：如支付方未按规定源泉扣缴，可能被处应扣未扣税款50%以上3倍以下罚款。非居民企业冒用居民企业身份：构成偷税，追缴税款、滞纳金并处罚款。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "居民企业,非居民企业,企业所得税税率,境外所得,源泉扣缴,预提所得税",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-001", "support_type": "support_direct", "support_note": "居民企业和非居民企业的纳税义务规定"},
                {"policy_code": "GOV-CIT-004", "support_type": "support_direct", "support_note": "非居民企业所得税率和源泉扣缴规定"}
            ],
            "tags": ["企业所得税", "居民企业", "非居民企业", "预提所得税", "境外所得"],
            "relations": []
        },
        {
            "question_title": "正常注销与简易注销，在税务清算流程和时限要求上有何不同？",
            "question_plain": "公司不想经营了，听说有正常注销和简易注销两种方式，税务上两种方式处理有何不同？",
            "stage_code": "CLS",
            "module_code": "DEC",
            "question_type": "type_compare",
            "one_line_answer": "正常注销须经过税务清算，提交清算所得税申报，税务注销时间较长；简易注销适用于无债权债务或债权债务已清偿完毕的企业，免于提交清算所得税申报，税务注销时间短。",
            "detailed_answer": "正常注销与简易注销的税务处理差异主要体现在清算环节。正常注销时，企业在注销前须进行税务清算，包括：对资产进行全面清查、处理债权债务、清偿应纳税款、向税务机关申报清算所得税（如清算所得为正数须缴纳企业所得税），税务机关审核后方可出具税务注销文书，整个流程通常需要数月。简易注销则适用于领取营业执照后未开展经营活动，或申请注销登记前债权债务已清算完结（或债务虽未清偿但已提供担保）的企业，此种情形下免于提交清算所得税申报，税务注销流程大大简化，可在很短时间内完成。两者在工商环节也有区别：简易注销须先在国家企业信用信息公示系统公示20天（部分地区45天），无异议后方可办理。",
            "core_definition": "正常注销：企业因解散、被吊销等原因申请注销登记前，依法进行清算（包括税务清算），清偿全部债务后申请税务和工商注销。简易注销：对符合条件的企业，免于经过清算程序，简化材料和流程，快速办理注销登记。",
            "applicable_conditions": "正常注销：一般企业，尤其是有债权债务未清的企业。简易注销：领取营业执照后未开展经营活动的企业；或债权债务已清算完毕或已提供担保的企业（上市公司除外）。",
            "exceptions_boundary": "简易注销公示期内如有债权人提出异议，企业须转为正常注销程序；存在未结清的税务欠税、发票欠缴的，不能办理简易注销；曾经提交虚假清算报告的企业，3年内不得再次申请简易注销。",
            "practical_steps": "正常注销税务处理：（1）到主管税务机关申请注销税务登记；（2）进行存货、固定资产清理，处理应税事项；（3）填报《企业所得税清算所得税申报表》；（4）结清所有税款、滞纳金、罚款；（5）交回剩余发票和税控设备；（6）取得税务注销证明。\n简易注销税务处理：（1）在公示系统填报并公示简易注销承诺书（若无债权债务声明）；（2）公示期满后30日内向登记机关申请注销登记；（3）如登记机关要求提交清税证明，主管税务机关出具《清税证明》。",
            "risk_warning": "正常注销未清税：注销后税务机关仍可追缴欠税，股东可能承担无限责任。简易注销虚假承诺：提交虚假材料取得简易注销登记，登记机关可撤销注销登记，恢复企业主体资格，原股东承担原有责任。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "正常注销,简易注销,税务清算,清算所得税,债权债务,注销登记",
            "high_frequency_flag": True,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-001", "support_type": "support_direct", "support_note": "清算企业所得税的法律规定"},
                {"policy_code": "GOV-Tax-007", "support_type": "support_procedure", "support_note": "注销税务登记的办理程序和材料要求"}
            ],
            "tags": ["注销登记", "税务清算", "简易注销", "正常注销", "企业所得税清算"],
            "relations": [
                {"question_code": "CLS-CLEAR-010", "relation_type": "related"},
                {"question_code": "CLS-CLEAR-016", "relation_type": "related"},
                {"question_code": "CLS-DEC-003", "relation_type": "related"}
            ]
        },
        {
            "question_title": "走逃失联企业与正常经营企业，在税务处理和发票管理上有何本质区别？",
            "question_plain": "什么是走逃失联企业？为什么有些企业突然就无法取得发票了？走逃企业有什么税务风险？",
            "stage_code": "RISK",
            "module_code": "RISK",
            "question_type": "type_compare",
            "one_line_answer": "走逃失联企业是税务部门认定的已走逃企业（无法联系、无真实业务），其开出的发票属于异常凭证，收到这些发票的企业进项税不得抵扣，已抵扣的须转出。",
            "detailed_answer": "走逃失联企业（又称'非正常户'）是指已办理税务登记但无法联系、查无下落的纳税人，包括连续三个月所有税种均未进行申报且拒绝或无法联系的企业。税务机关在其认定走逃后，会将企业列入异常凭证目录，开出的增值税专用发票会被判定为'异常增值税扣税凭证'，收到这些发票的企业（善意取得除外）不得抵扣进项税，已抵扣的须做进项税转出，补缴增值税、企业所得税，并可能面临罚款。正常经营企业则依法享有发票领购、开具和抵扣的权利，税务机关对其发票监管为日常管理而非异常监控。两者在税务上的'待遇'完全不同：正常企业发票是正常的抵扣凭证，走逃企业的发票是烫手山芋。",
            "core_definition": "走逃失联企业：已办理税务登记的纳税人，通过实地核查、电话、信函等方式均无法联系，且已连续三个月未申报，税务机关将其认定为非正常户。异常增值税扣税凭证：增值税发票开具方被认定为非正常户、走逃失联后，其开具的增值税专用发票成为购货方的异常凭证。",
            "applicable_conditions": "走逃失联认定：企业已办理税务登记；无法通过实地核查确认实际经营地址；电话、邮寄均无法送达；连续3个月未申报。收到异常凭证：作为购买方取得了已被列为异常的发票，无论是否为善意取得。",
            "exceptions_boundary": "善意取得虚开增值税发票：能够证明交易真实、发票开具符合规定、不知道或不应当知道发票为虚开的，可以继续抵扣（须提供证据）；但如果开票方被认定为虚开且无法证明善意，仍须转出。",
            "practical_steps": "发现发票为异常凭证的处理：（1）立即停止抵扣，将已抵扣进项税做进项转出；（2）向主管税务机关提交《增值税进项税额转出情况说明》；（3）配合税务机关核查，提供相关合同、运输凭证、入库单等证据材料；（4）如能证明为善意取得，可申请继续抵扣；（5）换开合规发票。",
            "risk_warning": "取得异常凭证后继续抵扣：构成偷税，除补缴税款外，处0.5倍至5倍罚款，滞纳金从滞纳之日起按日万分之五计算。故意取得走逃企业发票：构成虚开增值税专用发票罪的共犯，最高可判无期徒刑。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "走逃失联,非正常户,异常凭证,进项税转出,虚开发票,发票风险",
            "high_frequency_flag": True,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-004", "support_type": "support_direct", "support_note": "异常增值税扣税凭证的处理规定"},
                {"policy_code": "GOV-RISK-001", "support_type": "support_direct", "support_note": "非正常户认定标准和后续管理"}
            ],
            "tags": ["发票风险", "走逃失联", "异常凭证", "进项税转出", "非正常户", "虚开发票"],
            "relations": [
                {"question_code": "RISK-RISK-001", "relation_type": "related"},
                {"question_code": "RISK-RISK-002", "relation_type": "related"}
            ]
        },
        {
            "question_title": "虚开发票与善意取得发票，税务处理和法律后果有何本质区别？",
            "question_plain": "同样收到了虚开的发票，为什么有的是违法要处罚，有的却可以继续抵扣？这两种情况怎么区分？",
            "stage_code": "RISK",
            "module_code": "RISK",
            "question_type": "type_compare",
            "one_line_answer": "虚开发票是有意为之的违法行为，开票方和受票方均面临严厉处罚；善意取得发票是受骗上当，接受方提供了真实交易证据后可继续抵扣，不构成违法。",
            "detailed_answer": "虚开发票与善意取得发票的本质区别在于主观故意性。虚开发票是指开具与实际经营业务情况不符的发票，包括开具虚假交易内容的发票（无货虚开）、开具数量或金额不实的发票（有的多开）、让他人为自己开具与实际不符的发票（介绍虚开）等，这些行为均以骗取国家税款为目的，主观上明知故犯，是严重的税收违法犯罪行为，刑事处罚最高至无期徒刑。善意取得虚开发票是指在真实交易中，销售方提供了虚开的发票，但购买方不知情、不知道或不应当知道发票为虚开，且有真实的货物或服务交易，接受方可以继续抵扣进项税（在提供充分证据证明真实交易的前提下）；但如果无法证明真实交易，则不得抵扣。",
            "core_definition": "虚开发票：为他人开具、为自己开具、让他人为自己开具、介绍他人开具与实际经营业务情况不符的发票。善意取得：在真实货物或服务交易中，不知悉发票为虚开的合法受票行为。",
            "applicable_conditions": "虚开发票：任何为骗取税款而开具与实际不符发票的行为，无论金额大小。善意取得：交易真实存在、发票形式合法、无法识别发票虚假（不知情）。",
            "exceptions_boundary": "有真实交易但发票开具错误（如税目税率错误）：属于开票错误，可换开发票，不属于虚开。有真实交易但销货方走逃后认定为虚开的：如能证明真实交易，可善意取得抵扣。",
            "practical_steps": "虚开发票处理（受票方）：（1）立即转出已抵扣进项税；（2）补缴增值税及附加、企业所得税；（3）配合税务机关调查；（4）如有充分证据证明不知情，可申请善意取得认定。\n善意取得处理：（1）收集整理真实交易的相关证据（合同、出入库单、运输凭证、付款记录等）；（2）向主管税务机关提交情况说明和证据；（3）经税务机关核实确认善意后，可继续抵扣或办理退税。",
            "risk_warning": "明知虚开仍接受：构成虚开增值税专用发票的共同犯罪，移送司法机关追究刑事责任，最高无期徒刑。即使不知情但无法证明真实交易：进项税转出，补缴增值税和企业所得税。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "虚开发票,善意取得,进项税抵扣,虚开专用发票,真实交易,发票风险",
            "high_frequency_flag": True,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-004", "support_type": "support_direct", "support_note": "虚开发票和善意取得的区分标准及处理规定"},
                {"policy_code": "GOV-RISK-001", "support_type": "support_procedure", "support_note": "发票风险的预防和管理"}
            ],
            "tags": ["虚开发票", "善意取得", "进项税抵扣", "发票犯罪", "税务风险"],
            "relations": [
                {"question_code": "RISK-RISK-001", "relation_type": "related"},
                {"question_code": "RISK-RISK-002", "relation_type": "related"}
            ]
        },
        {
            "question_title": "税务约谈与税务稽查，在程序性质和应对策略上有何本质不同？",
            "question_plain": "收到了税务机关的约谈通知和稽查通知，有什么区别？企业应该如何分别应对？",
            "stage_code": "RISK",
            "module_code": "RISK",
            "question_type": "type_compare",
            "one_line_answer": "约谈是税务机关了解情况、核实问题的非正式程序，通常可柔性沟通；稽查是正式立案的执法检查，有法定程序和更强法律效力，两者性质和后果完全不同。",
            "detailed_answer": "税务约谈（纳税评估约谈）是税务机关在日常管理或纳税评估中发现纳税人存在涉税疑点，通过约谈方式了解情况、核实信息、给予纳税人解释说明机会的一种非正式程序，约谈后纳税人可自查补正，通常不会直接定性偷税。税务稽查是税务机关依法对纳税人进行立案检查的执法行为，依据《税务稽查工作规程》，有选案、检查、审理、执行四个法定环节，取得的证据具有法律效力，可以对企业作出补税、罚款、滞纳金决定，情节严重的移送公安机关。约谈通常是批量风险筛查后的初步核实，稽查则是针对性深入调查；约谈中企业的配合态度会影响后续是否走向稽查程序。",
            "core_definition": "税务约谈：税务机关在纳税评估中，对存在涉税疑点的纳税人，通过约见谈话方式了解情况、核实信息的非正式行政程序。税务稽查：税务机关依法对纳税人、扣缴义务人履行纳税义务和扣缴义务情况进行检查的法定行政执法程序。",
            "applicable_conditions": "约谈：日常评估发现数据异常、税负偏低、发票用量异常等风险点时触发。稽查：举报案件、上级交办、专项检查、或约谈后疑点未消除的案件。",
            "exceptions_boundary": "重大税收违法案件（如涉嫌虚开发票、偷逃税达到一定金额）不经过约谈直接立案稽查；达到重大案件标准的走逃企业，税务机关可直接依法处理。",
            "practical_steps": "约谈应对：（1）收到约谈通知书后，认真核实相关业务和数据；（2）准备相关合同、凭证、账簿等资料；（3）如发现问题，主动自查补报，争取从轻处罚；（4）配合态度积极，有利于后续关系维护。\n稽查应对：（1）立即联系专业税务律师或税务师事务所介入；（2）不要自行销毁、隐匿任何凭证资料；（3）所有提供给税务机关的资料留存复印件；（4）严格按《稽查工作规程》核查执法人员身份；（5）对稽查人员提出的问题，回答以事实为基础，不主动承认未核实的事项。",
            "risk_warning": "约谈阶段不配合：可能直接升级为稽查立案。稽查中发现重大问题：补税+0.5倍至5倍罚款+每日万分之五滞纳金；涉嫌犯罪的移送司法机关，最高7年有期徒刑（逃税罪）。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "税务约谈,纳税评估,税务稽查,稽查程序,偷税,发票风险",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-RISK-001", "support_type": "support_direct", "support_note": "税务稽查的法定程序和纳税人权利义务"},
                {"policy_code": "GOV-RISK-002", "support_type": "support_procedure", "support_note": "纳税评估约谈的程序和要求"}
            ],
            "tags": ["税务稽查", "纳税评估", "约谈", "偷税", "税务风险"],
            "relations": []
        },
        {
            "question_title": "企业所得税自行申报与源泉扣缴，在纳税主体和税款计算方式上有何不同？",
            "question_plain": "我企业要给境外公司支付特许权使用费，听说这笔税不用自己去报，是对方扣？这和自行申报有什么区别？",
            "stage_code": "TAX",
            "module_code": "TAX",
            "question_type": "type_compare",
            "one_line_answer": "源泉扣缴是支付方作为扣缴义务人，在付款时直接按预提税率扣下税款并代为申报缴纳；自行申报是纳税义务人自行计算、填报、缴纳税款。两者纳税主体不同。",
            "detailed_answer": "自行申报与源泉扣缴的核心区别在于纳税义务人和税款计算方式不同。自行申报适用于居民企业和在中国境内设立机构场所的非居民企业，纳税人自行计算应税收入、成本费用和应纳税额，按期向税务机关申报缴纳。源泉扣缴（又称代扣代缴）适用于非居民企业取得的股息红利、利息、特许权使用费、租金等消极所得，以及特定情形下的人员薪酬所得，由支付方（扣缴义务人）作为'二道贩子'，在付款时按法定预提税率（通常10%，双边协定可降低）扣下税款，并在次月15日内向主管税务机关申报解缴。源泉扣缴的计税基础是收入全额（不扣除费用），而自行申报是收入减成本费用的应税所得额。",
            "core_definition": "自行申报：纳税义务人作为申报主体，自行计算应纳税额并向税务机关申报缴纳的征纳方式。源泉扣缴（代扣代缴）：支付方作为扣缴义务人，在向纳税人支付款项时，按规定税率扣下应纳税款并代为申报缴纳的征纳方式。",
            "applicable_conditions": "自行申报：居民企业；在中国设立机构场所的非居民企业（机构场所所得）。源泉扣缴：向境外支付股息红利、利息、特许权使用费、租金等（无机构场所的非居民取得境内所得）。",
            "exceptions_boundary": "源泉扣缴优惠税率：符合双边税收协定'受益所有人'条件的，可申请享受协定优惠税率（5%至10%不等），须向税务机关提交《税收居民身份证明》等资料。境内支付方向非居民支付特许权使用费，无论是否约定税款承担方式，均须履行扣缴义务。",
            "practical_steps": "作为扣缴义务人（代扣代缴）：（1）识别是否为应扣缴的非居民所得；（2）付款时计算应扣缴税额（收入×10%或其他协定税率）；（3）在申报期内（次月15日内）填报《代扣代缴税款报告表》；（4）入库后取得税收缴款凭证交付非居民。\n作为非居民纳税人（如在中国有机构场所）：（1）按期自行申报机构场所相关所得；（2）如协定税率低于10%，须向主管税务机关提交协定待遇申请，经审批后适用低税率。",
            "risk_warning": "应扣未扣：处应扣未扣税款50%以上3倍以下罚款；构成偷税的，追缴税款、滞纳金并处罚款。扣缴义务人将已扣税款挪作他用：涉嫌构成挪用税款行为，情节严重的可构成挪用税款罪。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "源泉扣缴,代扣代缴,预提所得税,特许权使用费,股息红利,非居民企业",
            "high_frequency_flag": False,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-CIT-004", "support_type": "support_direct", "support_note": "非居民企业所得税源泉扣缴规定"},
                {"policy_code": "GOV-Tax-006", "support_type": "support_procedure", "support_note": "代扣代缴申报程序"}
            ],
            "tags": ["企业所得税", "源泉扣缴", "代扣代缴", "预提税", "非居民企业"],
            "relations": []
        },
        {
            "question_title": "发票作废与发票红冲，在适用情形和税务处理上有何本质区别？",
            "question_plain": "开出去的发票发现有问题，有的说作废，有的说红冲，两者有何不同？税务处理上有区别吗？",
            "stage_code": "OPR",
            "module_code": "INV",
            "question_type": "type_compare",
            "one_line_answer": "作废适用于当月开出的错误发票（未跨月、未认证），在开票系统中直接作废即可；红冲适用于已跨月或已认证的发票，需要开具负数发票冲抵原销项税。",
            "detailed_answer": "发票作废与发票红冲都是对已开具发票的错误进行纠正的方式，但适用情形和税务处理完全不同。发票作废的条件：发票在开具的当月收回全部联次，在增值税发票管理系统中点击'作废'按钮，作废发票的销项税不再计入当期应纳税额，纸质发票须全部联次注明'作废'字样。发票红冲的条件：发票已跨月（次月以后）；或发票已交给购买方且购买方已认证抵扣；或销售方自己已抄报税。在这些情况下不能作废，只能在系统中开具负数（红字）发票冲减原销项税额，已认证的还需要购买方申请开具《开具红字增值税专用发票信息表》后，销售方凭信息表开具红字发票。无论哪种方式，都不能简单地将原发票撕毁，必须通过系统走正规流程。",
            "core_definition": "发票作废：当月开具的发票因信息错误，在收回纸质发票全部联次后，在开票系统中作废该发票，该发票不再有效。发票红冲（开具红字发票）：对已跨月或已认证的发票，通过开具负数发票冲减原销项税额，同时冲减原对应的进项税额（购买方已认证时）。",
            "applicable_conditions": "作废：开具发票当月且受票方未认证抵扣，收回全部联次。 红冲：已跨月开具的发票；或受票方已认证抵扣；或开票方已抄报税无法作废。",
            "exceptions_boundary": "即使当月发票作废，如对方已认证或已抄报税，仍须走红冲程序；部分特殊发票（如机动车统一销售发票）有特殊的作废和红冲规定；作废发票需在发票管理系统内完整操作，口头作废无效。",
            "practical_steps": "发票作废步骤：（1）确认符合作废条件（当月、未认证）；（2）收回全部纸质发票联次；（3）在开票系统'发票作废'模块选择对应发票作废；（4）在纸质发票各联次注明'作废'字样，整理保存备查。\n发票红冲步骤（已认证）：（1）购买方向其主管税务机关填报《开具红字增值税专用发票信息表》；（2）税务机关审核后出具《信息表》；（3）销售方凭《信息表》在开票系统中开具红字发票；（4）红字发票作为进项税转出的凭证入账。",
            "risk_warning": "跨月发票自行作废（不红冲）：发票管理系统留有记录，税务机关可查到；被认定为未按规定处理，导致少缴税构成偷税。已认证发票未按规定红冲：购买方已抵扣的进项税须转出补税，税务机关可对销售方处未开具发票的罚款。",
            "scope_level": "scope_national",
            "answer_certainty": "certain_clear",
            "keywords": "发票作废,发票红冲,红字发票,认证抵扣,进项税转出,开票错误",
            "high_frequency_flag": True,
            "newbie_flag": False,
            "policy_links": [
                {"policy_code": "GOV-VAT-004", "support_type": "support_direct", "support_note": "发票作废和红冲的具体条件和程序规定"},
                {"policy_code": "GOV-VAT-002", "support_type": "support_procedure", "support_note": "开具红字发票的详细操作流程"}
            ],
            "tags": ["发票作废", "发票红冲", "红字发票", "认证抵扣", "发票管理"],
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
    data = batch_compare
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
                 scope_level, answer_certainty, keywords, high_frequency_flag, newbie_flag,
                 status, version_no, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,'active','v1.0',?,?)""",
                (code, q["question_title"], q["question_plain"], q["stage_code"], q["module_code"],
                 q["question_type"], q["one_line_answer"], q["detailed_answer"], q["core_definition"],
                 q["applicable_conditions"], q["exceptions_boundary"], q["practical_steps"], q["risk_warning"],
                 q["scope_level"], q["answer_certainty"], q["keywords"], q["high_frequency_flag"], q["newbie_flag"],
                 now_ts, now_ts))
        except Exception as e:
            print(f"  跳过(主表): {code} {q['question_title'][:20]} -> {e}")
            skipped += 1
            continue

        qid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # policy_links
        link_count = 0
        for pl in q.get("policy_links", []):
            pol_id = resolve_policy_id(conn, pl["policy_code"])
            if pol_id:
                conn.execute("""INSERT INTO question_policy_link
                    (question_id, policy_id, support_type, support_note, display_order)
                    VALUES (?,?,?,?,?)""",
                    (qid, pol_id, pl["support_type"], pl.get("support_note",""), link_count))
                link_count += 1

        # tags
        for tag in q.get("tags", []):
            cur = conn.cursor()
            cur.execute("SELECT id FROM tag_dict WHERE tag_name = ?", (tag,))
            tr = cur.fetchone()
            if tr:
                conn.execute("INSERT OR IGNORE INTO question_tag_link (question_id, tag_id) VALUES (?,?)", (qid, tr['id']))

        # relations
        for rel in q.get("relations", []):
            cur = conn.cursor()
            cur.execute("SELECT id FROM question_master WHERE question_code = ?", (rel["question_code"],))
            rr = cur.fetchone()
            if rr:
                conn.execute("""INSERT INTO question_relation
                    (question_id, related_id, relation_type, display_order)
                    VALUES (?,?,?,1)""",
                    (qid, rr['id'], rel["relation_type"]))

        # update_log
        conn.execute("""INSERT INTO question_update_log
            (question_id, version_no, update_date, update_type,
             update_reason, updated_by, reviewed_by, change_summary)
            VALUES (?, 1, ?, 'create', ?, 'batch_import', '', ?)""",
            (qid, now_ts, "批量导入初始数据", f"创建问题 {code}"))

        print(f"  +{code} | {q['question_title'][:35]}... | links:{link_count}")
        imported += 1

    conn.commit()
    conn.close()
    print(f"\n导入完成: {imported}条成功, {skipped}条跳过")

if __name__ == "__main__":
    main()
