"""
核心服务层测试：QuestionService 查询逻辑
"""
import pytest
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "backend"))
from config import Config
from services.question_service import QuestionService


@pytest.fixture
def svc():
    import os
    from config import Config
    # 恢复到真实生产 DB（不要恢复到 test_routes 留下的已删除临时文件路径）
    from pathlib import Path
    real_db = str(Path(__file__).parent.parent.parent / 'database' / 'db' / 'tax_knowledge.db')
    if os.path.exists(real_db):
        Config.DB_PATH = real_db
    return QuestionService()


class TestQuestionService:
    """测试 QuestionService 核心查询方法"""

    def test_list_questions_returns_active_only(self, svc):
        result = svc.list_questions(status='active')
        assert result['total'] > 0
        assert len(result['questions']) <= result['page_size']

    def test_list_questions_by_stage(self, svc):
        result = svc.list_questions(stage='SET')
        for q in result['questions']:
            assert q['stage_code'] == 'SET'

    def test_list_questions_by_module(self, svc):
        # 用真实 module 值 DEC（申报纳税），不用 OPR（O）
        result = svc.list_questions(module='DEC')
        assert result['total'] > 0, "DEC 模块应有数据"
        for q in result['questions']:
            assert q['module_code'] == 'DEC'

    def test_list_questions_filter_by_hf(self, svc):
        result = svc.list_questions(hf='1')
        for q in result['questions']:
            assert q['high_frequency_flag'] == 1

    def test_list_questions_filter_by_newbie(self, svc):
        result = svc.list_questions(newbie='1')
        for q in result['questions']:
            assert q['newbie_flag'] == 1

    def test_list_questions_filter_by_keyword(self, svc):
        # 用中文关键词搜索
        result = svc.list_questions(keyword='发票')
        assert result['total'] > 0
        found = any(
            '发票' in (q.get('question_title', '') or '')
            or '发票' in (q.get('one_line_answer', '') or '')
            for q in result['questions']
        )
        assert found, "搜索'发票'应有结果"

    def test_list_questions_filter_by_qtype(self, svc):
        # qtype 参数使用 question_type 字段
        result = svc.list_questions(qtype='type_whether')
        for q in result['questions']:
            assert q.get('question_type') == 'type_whether'

    def test_search_questions_reuses_list_logic(self, svc):
        """search_questions 应复用 list_questions 的搜索口径，避免页面/API 行为分叉"""
        via_list = svc.list_questions(keyword='没收入', page=1, page_size=10)
        via_search = svc.search_questions('没收入', page=1, page_size=10)
        assert via_search['total'] == via_list['total']
        assert [q['question_code'] for q in via_search['questions']] == [
            q['question_code'] for q in via_list['questions']
        ]

    def test_list_questions_default_status_is_active(self, svc):
        """不传 status 时，默认只返回 active 问题。
        list_questions() SELECT 不含 status 列，通过 get_question_detail()
        直接查 DB 验证返回的每条记录 status = 'active'。
        """
        result = svc.list_questions()
        assert result['total'] > 0, "需要至少一条数据才能验证默认 status"
        for q in result['questions']:
            code = q['question_code']
            detail = svc.get_question_detail(code)
            assert detail['status'] == 'active', f"{code} status 应为 active，实际为 {detail['status']}"

    def test_list_questions_returns_pagination(self, svc):
        result = svc.list_questions(page=1, page_size=5)
        assert result['page'] == 1
        assert result['page_size'] == 5
        assert len(result['questions']) <= 5

    def test_get_question_detail(self, svc):
        # 用一个真实存在的 question_code
        detail = svc.get_question_detail('OPR-DEC-001')
        assert detail is not None
        assert detail['question_code'] == 'OPR-DEC-001'
        assert 'policies' in detail
        assert 'tags' in detail

    def test_get_question_detail_not_exists(self, svc):
        detail = svc.get_question_detail('XXX-YYY-999')
        assert detail is None

    def test_get_stages(self, svc):
        stages = svc.get_stages()
        codes = {s['tag_code'] for s in stages}
        assert 'SET' in codes
        assert 'OPR' in codes
        assert 'CLS' in codes

    def test_get_modules(self, svc):
        modules = svc.get_modules()
        codes = {m['tag_code'] for m in modules}
        assert 'INV' in codes
        assert 'CIT' in codes
        assert 'IIT' in codes

    def test_get_question_types(self, svc):
        types = svc.get_question_types()
        assert len(types) > 0
        type_codes = {t['type_code'] for t in types}
        # question_type 字段应该包含这些值
        assert len(type_codes) >= 3, "至少应有3种不同问题类型"

    def test_get_stats(self, svc):
        stats = svc.get_stats()
        assert stats['total_questions'] >= 80
        assert stats['total_hf'] > 0
        assert stats['total_newbie'] > 0

    def test_answer_type_vs_question_type_field(self, svc):
        # 验证数据库列名是 question_type，不是 answer_type
        import sqlite3
        conn = sqlite3.connect(Config.DB_PATH)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(question_master)")
        cols = [r[1] for r in cur.fetchall()]
        conn.close()
        assert 'question_type' in cols, "question_master 表必须有 question_type 列"
        assert 'answer_type' not in cols, "question_master 表不应有 answer_type 列"

    def test_all_stage_codes_valid(self, svc):
        """所有问题的 stage_code 都必须属于 tag_dict stage 类"""
        import sqlite3
        conn = sqlite3.connect(Config.DB_PATH)
        valid = {r[0] for r in conn.execute(
            "SELECT tag_code FROM tag_dict WHERE tag_category='stage'")}
        conn.close()
        result = svc.list_questions()
        for q in result['questions']:
            assert q['stage_code'] in valid, \
                f"{q['question_code']} stage='{q['stage_code']}' 不在合法字典: {valid}"

    def test_all_module_codes_valid(self, svc):
        """所有问题的 module_code 都必须属于 tag_dict module 类"""
        import sqlite3
        conn = sqlite3.connect(Config.DB_PATH)
        valid = {r[0] for r in conn.execute(
            "SELECT tag_code FROM tag_dict WHERE tag_category='module'")}
        conn.close()
        result = svc.list_questions()
        for q in result['questions']:
            assert q['module_code'] in valid, \
                f"{q['question_code']} module='{q['module_code']}' 不在合法字典: {valid}"


class TestQualityGate:
    """质量门禁测试（只读，验证现有数据模式）"""

    @pytest.fixture
    def gate(self):
        import os
        from config import Config
        # 恢复到真实生产 DB（不要恢复到 test_routes 留下的已删除临时文件路径）
        from pathlib import Path
        real_db = str(Path(__file__).parent.parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        if os.path.exists(real_db):
            Config.DB_PATH = real_db
        from services.quality_gate import QualityGate
        return QualityGate()

    def test_validate_for_publish_blocks_needs_update_policy(self, gate):
        """关联 needs_update 政策不能发布"""
        import sqlite3, tempfile, os
        from config import Config
        # 创建临时测试数据库（隔离，不依赖 Config.DB_PATH）
        tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        tmp.close()
        src = Config.DB_PATH  # 只读参考，不修改
        conn_src = sqlite3.connect(src)
        conn_src.backup(sqlite3.connect(tmp.name))
        conn_src.close()
        # 用临时库测试
        from services.quality_gate import QualityGate
        tmp_gate = QualityGate(tmp.name)
        # 在临时库中找一个 pending_review + needs_update 组合
        conn_tmp = sqlite3.connect(tmp.name)
        conn_tmp.row_factory = sqlite3.Row
        cur = conn_tmp.cursor()
        cur.execute("""
            SELECT DISTINCT qm.question_code
            FROM question_master qm
            JOIN question_policy_link qpl ON qpl.question_id = qm.id
            JOIN policy_basis pb ON pb.id = qpl.policy_id
            WHERE qm.status = 'pending_review' AND pb.verification_status = 'needs_update'
            LIMIT 1
        """)
        row = cur.fetchone()
        conn_tmp.close()
        os.unlink(tmp.name)
        if not row:
            pytest.skip("无满足条件数据，跳过")

        result = tmp_gate.validate_for_publish(row['question_code'])
        assert not result['ok'], "关联 needs_update 政策应阻止发布"
        err_text = ' '.join(result['errors'])
        assert any(kw in err_text for kw in ['待更新', 'needs_update']), \
            f"错误应说明政策待更新：{result['errors']}"

    def test_validate_for_publish_blocks_source_pending_policy(self, gate):
        """关联 source_pending 政策不能发布"""
        import sqlite3, tempfile, os
        from config import Config
        tmp = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        tmp.close()
        conn_src = sqlite3.connect(Config.DB_PATH)
        conn_src.backup(sqlite3.connect(tmp.name))
        conn_src.close()
        from services.quality_gate import QualityGate
        tmp_gate = QualityGate(tmp.name)
        conn_tmp = sqlite3.connect(tmp.name)
        conn_tmp.row_factory = sqlite3.Row
        cur = conn_tmp.cursor()
        cur.execute("""
            SELECT DISTINCT qm.question_code
            FROM question_master qm
            JOIN question_policy_link qpl ON qpl.question_id = qm.id
            JOIN policy_basis pb ON pb.id = qpl.policy_id
            WHERE qm.status = 'pending_review' AND pb.verification_status = 'source_pending'
            LIMIT 1
        """)
        row = cur.fetchone()
        conn_tmp.close()
        os.unlink(tmp.name)
        if not row:
            pytest.skip("无满足条件数据，跳过")

        result = tmp_gate.validate_for_publish(row['question_code'])
        assert not result['ok'], "关联 source_pending 政策应阻止发布"
        err_text = ' '.join(result['errors'])
        assert any(kw in err_text for kw in ['来源', 'source_pending']), \
            f"错误应说明来源待核实：{result['errors']}"

    def test_validate_for_review_returns_valid_structure(self, gate):
        """validate_for_review 对真实 draft 条目返回正确的结构"""
        import sqlite3
        from config import Config
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # 找一条真实 draft 问题
        cur.execute("SELECT question_code FROM question_master WHERE status='draft' LIMIT 1")
        row = cur.fetchone()
        conn.close()
        if not row:
            pytest.skip("数据库中没有 draft 条目，无法测试 validate_for_review")
        code = row['question_code']
        result = gate.validate_for_review(code)
        assert isinstance(result, dict)
        assert 'ok' in result
        assert 'errors' in result
        assert 'warnings' in result
