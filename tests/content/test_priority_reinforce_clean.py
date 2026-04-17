"""
验证 priority_reinforce.py 在当前 DB 下不再输出旧 PREF/ETAX 叙述。
"""
import pytest
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
REINFORCE_SCRIPT = PROJECT_ROOT / "scripts" / "content" / "priority_reinforce.py"
DB_PATH = PROJECT_ROOT / "database" / "db" / "tax_knowledge.db"


class TestPriorityReinforceClean:
    """报告不应包含已失效的 PREF/ETAX 硬编码叙述"""

    def test_no_stale_pref_module_section(self):
        """报告不应出现 'PREF模块（税收优惠）' 这个段落标题"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        assert "PREF模块（税收优惠）" not in output, \
            "报告仍包含旧的 'PREF模块' 段落，应已替换为动态模块视角"

    def test_no_stale_etax_module_section(self):
        """报告不应出现 'ETAX模块' 的批次建议"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        assert "ETAX模块" not in output, \
            "报告仍包含旧的 'ETAX模块' 叙述"

    def test_no_old_etax_codes_in_suggestions(self):
        """下一批建议不应出现 ETAX-DEC / ETAX-REG 等旧编码"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        # 这些是旧的 ETAX 编码，前缀已不存在
        stale_codes = ["ETAX-DEC-004", "ETAX-DEC-005", "ETAX-REG-003", "ETAX-REG-004"]
        for code in stale_codes:
            assert code not in output, \
                f"报告仍包含旧编码 {code}，该编码已不存在于 DB"

    def test_no_stale_zero_declare_batch_reference(self):
        """不应出现硬编码的零申报问题 OPR-DEC-011/012/013"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        # 批次建议不应写死具体编码
        assert "OPR-DEC-011" not in output or "OPR-DEC-012" not in output or "OPR-DEC-013" not in output or \
            ("批次" not in output or "零申报" not in output), \
            "批次建议不应硬编码具体问题编码，应为动态数据"

    def test_no_stale_risk_batch_reference(self):
        """不应出现硬编码的 OPR-RISK-007 / OPR-RISK-010"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        assert "OPR-RISK-007" not in output or "OPR-RISK-010" not in output, \
            "批次建议不应硬编码 OPR-RISK-007/010"

    def test_script_exits_zero_when_db_clean(self):
        """DB 无脏数据时，脚本应正常退出（exit 0）"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, \
            f"脚本异常退出: returncode={result.returncode}, stderr={result.stderr[:200]}"

    def test_report_mentions_stage_module_matrix(self):
        """报告应包含阶段×模块矩阵（验证动态内容正常产出）"""
        result = subprocess.run(
            ["python3", str(REINFORCE_SCRIPT)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        assert "阶段×模块覆盖矩阵" in output, "报告应包含动态矩阵"
        assert "下一批内容建设建议" in output, "报告应包含动态批次建议"
