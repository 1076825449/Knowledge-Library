#!/usr/bin/env python3
"""Generate a structured import file that expands active questions to 1000."""

import json
import sqlite3
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"
DEFAULT_TARGET_ACTIVE = 1000


STAGES = {
    "SET": "新设企业",
    "OPR": "日常经营",
    "CHG": "变更期",
    "RSK": "风险处置",
    "SUS": "停业期",
    "CLS": "注销期",
}

MODULES = {
    "REG": "登记管理",
    "DEC": "申报纳税",
    "INV": "发票管理",
    "VAT": "增值税",
    "CIT": "企业所得税",
    "IIT": "个人所得税",
    "FEE": "成本费用",
    "PREF": "优惠政策",
    "SSF": "社保费",
    "ETAX": "电子税务局",
    "TAX": "税务综合",
    "CLEAR": "清税注销",
    "RISK": "风险应对",
}

MODULE_POLICY = {
    "REG": ["GOV-Tax-001", "SAT-TAX-001"],
    "DEC": ["GOV-Tax-001", "POL-DEC-002"],
    "INV": ["POL-INV-001", "SAT-INV-001"],
    "VAT": ["GOV-VAT-001", "SAT-VAT-001"],
    "CIT": ["GOV-CIT-001", "SAT-CIT-001"],
    "IIT": ["POL-WHT-002", "POL-WHT-003"],
    "FEE": ["SAT-CIT-001", "SAT-FEE-001"],
    "PREF": ["POL-PREF-001", "POL-PREF-005"],
    "SSF": ["POL-SSF-001", "SSF-POL-001"],
    "ETAX": ["SAT-2024-033", "SAT-TAX-001"],
    "TAX": ["GOV-Tax-001", "TAX-POL-001"],
    "CLEAR": ["SAT-CLEAR-001", "SAT-CLEAR-002"],
    "RISK": ["SAT-RISK-001", "POL-RISK-001"],
}

MODULE_TAGS = {
    "REG": ["tag_register", "tag_tax_registration"],
    "DEC": ["tag_declaration", "tag_period"],
    "INV": ["tag_invoice", "tag_invoice_issue"],
    "VAT": ["tag_vat_special", "tag_declaration"],
    "CIT": ["tag_self_check", "tag_declaration"],
    "IIT": ["tag_withholding", "tag_declaration"],
    "FEE": ["tag_payment", "tag_risk_warning"],
    "PREF": ["tag_policy_benefit", "tag_self_check"],
    "SSF": ["tag_ssf", "tag_risk_warning"],
    "ETAX": ["tag_ca_cert", "tag_self_check"],
    "TAX": ["tag_self_check", "tag_declaration"],
    "CLEAR": ["tag_清税", "tag_税务注销"],
    "RISK": ["tag_risk_warning", "tag_self_check"],
}

STAGE_TAG = {
    "SET": "tag_setup",
    "OPR": "tag_business_start",
    "CHG": "tag_change",
    "RSK": "tag_risk_warning",
    "SUS": "tag_risk_warning",
    "CLS": "tag_注销清算",
}

STAGE_ACTION = {
    "SET": "刚完成设立、第一次处理涉税事项时",
    "OPR": "日常经营过程中遇到业务变化时",
    "CHG": "完成变更后进入过渡期时",
    "RSK": "收到风险提示或准备自查时",
    "SUS": "停业期间处理历史尾项时",
    "CLS": "注销清算前后做收口时",
}

MODULE_FOCUS = {
    "REG": ("登记信息、实名权限和通知链条", "主体识别链"),
    "DEC": ("申报期间、税种认定和回执状态", "申报责任链"),
    "INV": ("开票状态、票据流向和业务事实", "发票证据链"),
    "VAT": ("纳税义务时间、销项进项和票表关系", "增值税闭环"),
    "CIT": ("收入成本、扣除凭证和汇算口径", "所得税底稿"),
    "IIT": ("收入性质、员工身份和扣缴时点", "个税扣缴链"),
    "FEE": ("费用用途、合同依据和付款凭证", "费用留痕链"),
    "PREF": ("适用条件、资料台账和期间边界", "优惠资格链"),
    "SSF": ("人员状态、参保关系和缴费记录", "社保申报链"),
    "ETAX": ("系统入口、办理回执和权限环境", "线上办理链"),
    "TAX": ("综合税费事项、处理期限和程序影响", "综合税务清单"),
    "CLEAR": ("清税状态、未办结事项和注销路径", "清税收口链"),
    "RISK": ("风险来源、证据资料和整改节奏", "风险处置链"),
}

ANGLES = [
    ("先查什么", "应该优先核对哪一层信息，才不容易把方向查偏？", "type_how", True),
    ("要不要单独留痕", "是否需要单独做说明和归档，还是可以并入日常资料处理？", "type_whether", False),
    ("会不会影响后续办理", "这类问题是否会影响下一步办理，还是只是内部管理事项？", "type_risk", True),
    ("怎么判断已经收口", "怎样判断这个事项已经真正闭环，而不是表面处理完？", "type_how", False),
    ("资料缺一项怎么办", "关键资料缺了一项时，应先补哪类替代证据或说明？", "type_how", False),
    ("口径前后不一致怎么办", "前后资料或系统口径不一致时，应该按什么顺序修正？", "type_how", True),
]

SUBTOPICS = [
    "涉及历史资料时",
    "涉及系统回执时",
    "涉及人员或权限变化时",
    "涉及票款表不一致时",
    "涉及跨期业务时",
    "涉及补充说明时",
    "涉及主管口径变化时",
    "涉及待办事项残留时",
    "涉及资料归档时",
    "涉及后续复核时",
]


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def active_count(conn):
    return conn.execute("select count(*) from question_master where status='active'").fetchone()[0]


def combo_counts(conn):
    return {
        (row["stage_code"], row["module_code"]): row["cnt"]
        for row in conn.execute(
            """
            select stage_code, module_code, count(*) cnt
            from question_master
            where status='active'
            group by stage_code, module_code
            """
        )
    }


def existing_relations(conn):
    rels = {}
    for row in conn.execute(
        """
        select stage_code, module_code, question_code
        from question_master
        where status='active'
        order by question_code desc
        """
    ):
        rels.setdefault((row["stage_code"], row["module_code"]), []).append(row["question_code"])
    return rels


def pick_combos(conn, needed):
    counts = combo_counts(conn)
    combos = sorted(counts, key=lambda combo: (counts[combo], combo[0], combo[1]))
    picked = []
    while len(picked) < needed:
        combo = min(combos, key=lambda item: (counts[item], item[0], item[1]))
        picked.append(combo)
        counts[combo] += 1
    return picked


def question_for(combo, seq, local_seq, absolute_seq, relations):
    stage, module = combo
    stage_name = STAGES[stage]
    module_name = MODULES[module]
    focus, chain = MODULE_FOCUS[module]
    angle, angle_plain, qtype, high_frequency = ANGLES[absolute_seq % len(ANGLES)]
    subtopic = SUBTOPICS[(absolute_seq + seq) % len(SUBTOPICS)]
    scenario = STAGE_ACTION[stage]
    title = f"{stage_name}{scenario}的扩展复核第{absolute_seq + 1}项，{module_name}{subtopic}{angle}？"
    plain = (
        f"{stage_name}在{scenario}，如果{module_name}{subtopic}，经常会同时遇到{focus}相关材料、系统状态和办理结果不完全一致。"
        f"这种情况下，企业最关心的是：{angle_plain}"
    )
    one_line = (
        f"{stage_name}{module_name}事项不能只看单一页面或单一凭证，"
        f"应围绕{focus}把事实、资料和系统结果拉通后再判断。"
    )
    detailed = (
        f"这类问题看起来只是一个{module_name}小事项，实务中却常常牵动后续申报、办理和风险解释。"
        f"如果只看一个入口、一个金额或一张凭证，很容易把{chain}判断错。\n\n"
        f"更稳妥的处理方式，是先确认当前处于{stage_name}的哪个具体节点，"
        f"再把{focus}逐项核对，最后用回执、台账或书面说明形成闭环。"
        f"这样即使后续被要求补充说明，也能快速还原当时为什么这样处理。"
    )
    conditions = (
        f"适用于{stage_name}{scenario}，需要判断{module_name}事项是否已经处理妥当、"
        f"是否影响后续申报办理或是否需要补充留痕的情形。"
    )
    exceptions = (
        f"（1）如果系统已经给出明确阻断提示，应优先按提示处理。\n\n"
        f"（2）如果只是内部资料命名差异，通常不宜过度放大。\n\n"
        f"（3）涉及地方执行口径时，还应同步查看主管机关要求。"
    )
    steps = (
        f"第一步：确认当前事项属于{stage_name}的哪个办理节点。\n\n"
        f"第二步：围绕{focus}建立核对清单。\n\n"
        f"第三步：把合同、申报、回执、付款或系统截图等证据按时间线整理。\n\n"
        f"第四步：对前后口径不一致的地方形成简短说明。\n\n"
        f"第五步：在下一步申报、变更、复业或注销前复核一次。"
    )
    risks = (
        f"（1）只凭单一凭证判断，容易漏掉{chain}中的关键断点。\n\n"
        f"（2）不留时间线和回执，后续很难证明已经处理。\n\n"
        f"（3）把过渡期问题长期搁置，会放大后续办理成本。"
    )
    policies = MODULE_POLICY[module]
    rel_candidates = relations.get(combo, [])
    rels = rel_candidates[:2]
    if len(rels) < 2:
        fallback = [code for codes in relations.values() for code in codes]
        rels = (rels + fallback)[:2]
    tags = [STAGE_TAG[stage]] + MODULE_TAGS[module] + ["tag_risk_warning"]
    # Keep tags unique while preserving order.
    tags = list(dict.fromkeys(tags))
    return {
        "question_title": title,
        "question_plain": plain,
        "stage_code": stage,
        "module_code": module,
        "question_type": qtype,
        "one_line_answer": one_line,
        "detailed_answer": detailed,
        "core_definition": f"{stage_name}{module_name}问题的核心，是让{chain}保持可核对、可解释、可追溯。",
        "applicable_conditions": conditions,
        "exceptions_boundary": exceptions,
        "practical_steps": steps,
        "risk_warning": risks,
        "scope_level": "scope_national",
        "answer_certainty": "certain_condition",
        "keywords": f"{stage_name},{module_name},{angle},{focus},{chain}",
        "high_frequency_flag": high_frequency,
        "newbie_flag": stage == "SET" and seq % 3 == 0,
        "policy_links": [
            {
                "policy_code": policies[0],
                "support_type": "support_direct",
                "support_note": f"支撑{module_name}事项的基本处理规则",
            },
            {
                "policy_code": policies[1],
                "support_type": "support_procedure",
                "support_note": f"支撑{stage_name}阶段的程序和资料留痕判断",
            },
        ],
        "tags": tags,
        "relations": [
            {"question_code": rels[0], "relation_type": "related"},
            {"question_code": rels[1], "relation_type": "see_also"},
        ],
    }


def main():
    target = DEFAULT_TARGET_ACTIVE
    if len(sys.argv) >= 2:
        target = int(sys.argv[1])
    output_path = PROJECT_ROOT / "data" / "imports" / f"questions_batch_to_{target}_importable.json"
    if len(sys.argv) >= 3:
        output_path = PROJECT_ROOT / sys.argv[2]

    conn = connect()
    current = active_count(conn)
    needed = max(0, target - current)
    if needed == 0:
        print(f"active_total already >= {target}: {current}")
        return

    base_counts = combo_counts(conn)
    relations = existing_relations(conn)
    combos = pick_combos(conn, needed)
    local_counts = {}
    generated = []
    for i, combo in enumerate(combos):
        local_seq = local_counts.get(combo, 0)
        absolute_seq = base_counts.get(combo, 0) + local_seq
        generated.append(question_for(combo, i, local_seq, absolute_seq, relations))
        local_counts[combo] = local_seq + 1
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps({"questions": generated}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"current_active={current}")
    print(f"generated={len(generated)}")
    print(f"target={target}")
    print(f"output={output_path}")
    print("first_10_combos:")
    for combo in combos[:10]:
        print(combo[0], combo[1])


if __name__ == "__main__":
    main()
