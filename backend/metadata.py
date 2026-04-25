# ============================================================
# backend/metadata.py
# 项目统一元数据口径：枚举标签、展示分组、表单选项
# ============================================================

QUESTION_TYPE_META = {
    "type_whether": {"label": "是否类", "active": True},
    "type_how": {"label": "怎么办类", "active": True},
    "type_define": {"label": "定义类", "active": True},
    "type_what": {"label": "是什么类", "active": True},
    "type_risk": {"label": "风险类", "active": True},
    "type_time": {"label": "时限类", "active": True},
    "type_why": {"label": "为什么类", "active": True},
    # 历史遗留值：继续兼容展示和编辑，不建议新批量导入继续扩散
    "type_steps": {"label": "步骤类", "active": False},
    "type_clarify": {"label": "澄清类", "active": False},
    "type_procedure": {"label": "办理类", "active": False},
    "type_compare": {"label": "比较类", "active": False},
    "type_compliance": {"label": "合规类", "active": False},
}

ANSWER_CERTAINTY_META = {
    "certain_clear": {"label": "明确（无条件）", "active": True},
    "certain_condition": {"label": "有条件", "active": True},
    # 历史别名，已合并到 certain_condition，兼容展示，不建议新录入使用
    "certain_conditional": {"label": "有条件", "active": False},
    "certain_dispute": {"label": "有争议", "active": True},
    "certain_practice": {"label": "实务做法", "active": True},
}

SCOPE_LEVEL_META = {
    "scope_national": {"label": "全国通用", "active": True},
    "scope_local": {"label": "地方口径", "active": True},
    "scope_mixed": {"label": "混合口径", "active": False},
}

STATUS_META = {
    "active": {"label": "正常"},
    "draft": {"label": "草稿"},
    "pending": {"label": "待复核"},
    "archived": {"label": "归档"},
    "obsolete": {"label": "过时"},
}

POLICY_LEVEL_META = {
    "level_law": {"label": "法律"},
    "level_admin": {"label": "行政法规"},
    "level_department": {"label": "部门规章"},
    "level_bulletin": {"label": "规范性文件"},
    "level_local": {"label": "地方文件"},
}

POLICY_STATUS_META = {
    "pol_effective": {"label": "现行有效"},
    "pol_partial": {"label": "部分失效"},
    "pol_expired": {"label": "已失效"},
    "pol_replaced": {"label": "已替代"},
    "pol_uncertain": {"label": "状态待核"},
}

SUPPORT_TYPE_META = {
    "support_direct": {"label": "直接依据", "group": "direct", "active": True},
    "citation": {"label": "引文依据（历史）", "group": "direct", "active": False},
    "support_procedure": {"label": "办理依据", "group": "procedure", "active": True},
    "support_definition": {"label": "定义依据", "group": "other", "active": True},
    "support_risk": {"label": "风险依据", "group": "other", "active": True},
    "support_local": {"label": "地方执行依据", "group": "other", "active": True},
    "support_aux": {"label": "辅助依据", "group": "other", "active": True},
}

RELATION_TYPE_META = {
    "related": {"label": "相关问题"},
    "next_step": {"label": "下一步"},
    "prerequisite": {"label": "前提问题"},
    "similar": {"label": "相似问题"},
    "see_also": {"label": "交叉参考"},
}

STAGE_LABELS = {
    "SET": "设立期",
    "OPR": "开业/日常经营期",
    "CHG": "变更期",
    "RSK": "风险异常期",
    "SUS": "停业期",
    "CLS": "注销期",
}

MODULE_LABELS = {
    "REG": "登记管理",
    "DEC": "申报纳税",
    "INV": "发票管理",
    "VAT": "增值税",
    "CIT": "企业所得税",
    "IIT": "个人所得税",
    "SSF": "社保费",
    "FEE": "成本费用",
    "PREF": "优惠政策",
    "RISK": "风险应对",
    "CLEAR": "清税注销",
    "TAX": "税务综合",
    "ETAX": "电子税务局/系统办理",
}


def active_options(meta):
    return [{"code": code, **data} for code, data in meta.items() if data.get("active", True)]


def all_options(meta):
    return [{"code": code, **data} for code, data in meta.items()]
