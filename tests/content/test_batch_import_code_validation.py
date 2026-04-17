"""
测试 batch_import_questions.py 的 override_code 前缀校验逻辑。
"""
import pytest
import json
import tempfile
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
import sys
sys.path.insert(0, str(ROOT_DIR / "scripts" / "content"))
from batch_import_questions import import_questions


class TestOverrideCodeValidation:
    """override_code 必须符合 <stage>-<module>-NNN 格式"""

    def _run_import(self, questions):
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False, encoding="utf-8") as f:
            json.dump({"questions": questions}, f)
            path = f.name
        try:
            from batch_import_questions import import_questions
            return import_questions({"questions": questions})
        finally:
            Path(path).unlink(missing_ok=True)

    def test_wrong_prefix_rejected(self):
        """stage=SET, module=DEC，但 override_code 以 PREF 开头 → 应报错拒绝"""
        result = self._run_import([{
            "question_title": "测试错误前缀",
            "stage_code": "SET",
            "module_code": "DEC",
            "question_code": "PREF-DEC-001",
            "one_line_answer": "测试",
        }])
        errors = result["errors"]
        assert any("前缀不匹配" in e for e in errors), \
            f"期望报错包含'前缀不匹配'，实际 errors={errors}"

    def test_wrong_module_in_prefix_rejected(self):
        """stage=OPR, module=REG，但 override_code 是 OPR-DEC-001 → 应报错拒绝"""
        result = self._run_import([{
            "question_title": "测试错误模块前缀",
            "stage_code": "OPR",
            "module_code": "REG",
            "question_code": "OPR-DEC-001",
            "one_line_answer": "测试",
        }])
        errors = result["errors"]
        assert any("前缀不匹配" in e for e in errors), \
            f"期望报错包含'前缀不匹配'，实际 errors={errors}"

    def test_non_digit_suffix_rejected(self):
        """override_code 序号不是3位数字 → 应报错拒绝"""
        result = self._run_import([{
            "question_title": "测试序号格式",
            "stage_code": "SET",
            "module_code": "DEC",
            "question_code": "SET-DEC-1",   # 少位
            "one_line_answer": "测试",
        }])
        errors = result["errors"]
        assert any("序号格式错误" in e for e in errors), \
            f"期望报错包含'序号格式错误'，实际 errors={errors}"

    def test_old_etax_prefix_rejected(self):
        """旧的 ETAX-DEC-001 格式 → 应报错拒绝"""
        result = self._run_import([{
            "question_title": "测试旧ETA前缀",
            "stage_code": "OPR",
            "module_code": "DEC",
            "question_code": "ETAX-DEC-001",
            "one_line_answer": "测试",
        }])
        errors = result["errors"]
        assert any("前缀不匹配" in e for e in errors)

    def test_old_pref_stage_rejected(self):
        """旧的 PREF-BAS-001 格式 → 应报错拒绝"""
        result = self._run_import([{
            "question_title": "测试旧PREF前缀",
            "stage_code": "OPR",
            "module_code": "REG",
            "question_code": "PREF-BAS-001",
            "one_line_answer": "测试",
        }])
        errors = result["errors"]
        assert any("前缀不匹配" in e for e in errors)
