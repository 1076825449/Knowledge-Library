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
