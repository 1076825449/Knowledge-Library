#!/usr/bin/env python3
"""补2条VAT问题到现有的batch JSON"""
import json, sys
sys.path.insert(0, '/Volumes/外接硬盘/vibe coding/网站/知识库/scripts/content')

path = '/Volumes/外接硬盘/vibe coding/网站/知识库/scripts/content/batch_expand_fee_cit_iit.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_qs = [
  {
    "question_title": "增值税小规模纳税人适用哪些免税政策？月销售额多少以内可以免征增值税？",
    "question_plain": "公司是增值税小规模纳税人，听说有免税额度，具体是什么政策？一个月销售额不超过多少可以免征？",
    "stage_code": "OPR",
    "module_code": "VAT",
    "question_type": "type_what",
    "one_line_answer": "小规模纳税人月销售额10万元以下（含10万元）免征增值税，以1个季度为纳税期的，季度销售额30万元以下免征增值税。",
    "detailed_answer": "根据《增值税暂行条例》及实施细则，小规模纳税人的免税政策如下：一、免税标准：按月纳税的，月销售额10万元以下（含10万元）免征增值税；按季度纳税的，季度销售额30万元以下（含30万元）免征增值税。适用对象为已登记为增值税小规模纳税人的企业、个体工商户和其他个人。二、销售额计算：销售额为纳税人销售货物、劳务、服务、无形资产和不动产的总金额，包括开具发票金额和未开具发票金额；适用免税政策的销售额为扣除本期发生的销售不动产的销售额后的余额。三、开票注意事项：享受免税的小规模纳税人，开具增值税普通发票（税率栏显示"免税"）即可；若开具增值税专用发票，则专用发票部分须缴纳增值税。四、常见误区：小规模纳税人的免税是针对销售额的免税，不是税率上的优惠；免税额是指不含税销售额；兼营销售货物、劳务、服务、无形资产和不动产的，销售额须分别核算，未分别核算的须从高适用税率或合并计税。",
    "core_definition": "小规模纳税人免税销售额标准：月销售额10万元以下（季度30万元以下）。",
    "applicable_conditions": "适用于已认定为增值税小规模纳税人的企业和个体工商户。",
    "exceptions_boundary": "开具了增值税专用发票的部分须征税；不动产销售额须从免税额度中扣除后再判断是否超过免税标准。",
    "practical_steps": "步骤1：确认自身为小规模纳税人身份\n步骤2：按月或按季度统计销售额（含税）\n步骤3：扣除本期不动产销售额后，判断是否在10万或30万以内\n步骤4：免税范围内开具普通发票（税率栏免税）\n步骤5：超标准部分按征收率（1%或3%）申报缴纳增值税",
    "risk_warning": "错误开具专用发票导致无法享受免税；隐瞒销售额逃避纳税义务存在被查处风险。",
    "scope_level": "scope_national",
    "answer_certainty": "certain_clear",
    "keywords": "小规模纳税人,免税销售额,月10万元,季度30万元,免税政策,普通发票,专用发票",
    "high_frequency_flag": True,
    "newbie_flag": True,
    "policy_links": [
      {"policy_code": "POL-VAT-001", "support_type": "support_direct", "support_note": "《增值税暂行条例》及免税标准：小规模纳税人月销售额10万元以下免征增值税"}
    ]
  },
  {
    "question_title": "企业出口货物或服务，增值税有哪些退税政策？退税率如何确定？",
    "question_plain": "公司有出口业务，货物要出口到海外，听说出口可以退增值税。这个退税是怎么算的？哪些货物可以退？退税率是多少？",
    "stage_code": "OPR",
    "module_code": "VAT",
    "question_type": "type_procedure",
    "one_line_answer": "出口货物和跨境服务适用增值税零税率或免税加退税政策。外贸企业退税按进项税额计算；生产企业退税按免抵退方法计算；退税率按商品编码和政策确定。",
    "detailed_answer": "出口退税是增值税体系中的重要环节，具体规则如下：一、适用范围：在中国报关出口的货物适用免抵退政策（生产企业）或免退政策（外贸企业）；跨境应税行为（提供交通运输、邮政、基础电信、建筑、不动产租赁服务等）适用零税率。二、零税率与免税的区别：零税率（税率0%）是指出口环节免税，并退还以前环节已纳增值税；免税是指出口环节不征税，但不退已纳增值税；目前大多数出口货物适用零税率。三、退税率：退税率由财政部和税务总局根据商品编码（HS编码）确定，不同商品退税率不同（0%、3%、6%、9%、13%等）；退税率不等于征税率，部分商品征13%退9%或征13%退0%。四、计算方法：外贸企业：应退税额=进项税额发票金额乘以退税率；生产企业：免抵退税额=出口销售额乘以退税率，再与当期进项税额比较，较小者退税。五、申报要求：须在出口后90天内收齐退税单证（报关单、发票、出口收汇凭证），并在认证系统里做进项发票认证。",
    "core_definition": "出口退（免）税：国家对出口货物和跨境服务退还或免征其在国内生产和流通环节已缴纳的增值税。",
    "applicable_conditions": "适用于有出口业务（报关离境、跨境提供应税服务）的企业。",
    "exceptions_boundary": "出口加工贸易货物、进料加工复出口货物的退税规则另有规定；特殊商品（如资源类产品）可能不退税或退税率为零。",
    "practical_steps": "步骤1：确认出口商品的海关商品编码（HS编码）并查询对应退税率\n步骤2：确认企业类型（外贸企业按免退政策，生产企业按免抵退政策）\n步骤3：收集出口报关单、增值税进项发票、收汇凭证\n步骤4：外贸企业在认证系统做进项发票认证\n步骤5：按期在电子税务局或单一窗口系统填报出口货物劳务退免税申报表",
    "risk_warning": "逾期未收齐退税单证将无法办理退税；虚报出口骗取退税是严重违法行为，将受刑事处罚。",
    "scope_level": "scope_national",
    "answer_certainty": "certain_conditional",
    "keywords": "出口退税,免抵退,免退税,退税率,外贸企业,生产企业,HS编码,报关单",
    "high_frequency_flag": True,
    "newbie_flag": False,
    "policy_links": [
      {"policy_code": "POL-VAT-001", "support_type": "support_direct", "support_note": "《增值税暂行条例》及出口退（免）税规定：出口货物适用零税率并退还以前环节已纳税款"}
    ]
  }
]

data['questions'].extend(new_qs)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(f"OK: {len(data['questions'])} questions in file")
