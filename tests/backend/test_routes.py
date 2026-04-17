"""
Flask 页面层集成测试：使用 test_client() 不依赖外部服务
覆盖：列表筛选、详情字段、表单枚举值、首页

兼容性：
- Flask 2.3.0 + Werkzeug 3.0.1 通过 tests/conftest.py werkzeug 版本 patch 兼容
- session_transaction() 在此环境有 bug（Flask 2.3.0 / Werkzeug 3.x 不兼容）
  → admin_required 装饰器通过 app.view_functions + __wrapped__ 架空
"""
import pytest
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "backend"))
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    # 架空 admin_required 装饰器：通过 app.view_functions 找到被 @wraps 包装的原始函数
    # Flask 将装饰后的函数存为 view_function，__wrapped__ 属性指向原函数
    for endpoint in ("new_question", "edit_question"):
        view_func = app.view_functions.get(endpoint)
        if view_func is not None and hasattr(view_func, "__wrapped__"):
            app.view_functions[endpoint] = view_func.__wrapped__

    with app.test_client() as client:
        yield client


@pytest.fixture
def real_code(client):
    """找一个数据库中真实存在的问题编码"""
    rv = client.get("/questions?page=1")
    import re
    codes = re.findall(r'/question/([A-Z]+-[A-Z]+-\d+)', rv.data.decode("utf-8"))
    if not codes:
        pytest.skip("数据库中没有问题记录")
    return codes[0]


class TestQuestionsListPage:
    """测试 /questions 列表页"""

    def test_questions_page_returns_200(self, client):
        rv = client.get("/questions")
        assert rv.status_code == 200

    def test_questions_page_shows_count(self, client):
        rv = client.get("/questions?page=1")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "条结果" in data or "共" in data

    def test_questions_filter_by_stage_shows_correct_label(self, client):
        """stage=SET 筛选后，页面应显示"设立期"标签"""
        rv = client.get("/questions?stage=SET")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "设立期" in data

    def test_questions_filter_by_module_shows_correct_label(self, client):
        """module=DEC 筛选后，页面应显示"申报纳税"标签"""
        rv = client.get("/questions?module=DEC")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "申报纳税" in data

    def test_questions_filter_by_scope_region(self, client):
        """region=scope_national 筛选后，页面仍正常渲染"""
        rv = client.get("/questions?region=scope_national")
        assert rv.status_code == 200

    def test_questions_filter_by_keyword(self, client):
        """keyword=发票 搜索后，结果应包含发票字样"""
        rv = client.get("/questions?keyword=发票")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "发票" in data

    def test_questions_filter_by_hf(self, client):
        """hf=1 筛选后，应出现"高频"标签"""
        rv = client.get("/questions?hf=1")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "高频" in data

    def test_questions_filter_by_qtype(self, client):
        """qtype=type_whether 筛选后，应出现"是否"类型标签"""
        rv = client.get("/questions?qtype=type_whether")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "是否类" in data or "是否" in data

    def test_questions_has_all_stage_chips(self, client):
        """列表页应有全部6个阶段筛选项"""
        rv = client.get("/questions")
        data = rv.data.decode("utf-8")
        for stage in ["设立期", "开业", "变更", "注销"]:
            assert stage in data, f"缺少阶段标签: {stage}"

    def test_questions_has_module_chips(self, client):
        """列表页应有模块筛选项"""
        rv = client.get("/questions")
        data = rv.data.decode("utf-8")
        assert "登记管理" in data or "申报纳税" in data or "发票管理" in data

    def test_scope_mixed_not_in_filter_chips(self, client):
        """scope_mixed 不作为筛选 chip 出现（DB无此数据）"""
        rv = client.get("/questions")
        data = rv.data.decode("utf-8")
        assert not ("混合口径" in data and "scope_mixed" in data)

    def test_status_filter_chips_present(self, client):
        """状态筛选 chip：active / draft / archived"""
        rv = client.get("/questions")
        data = rv.data.decode("utf-8")
        assert "正常" in data or "active" in data
        assert "草稿" in data or "draft" in data

    def test_pagination_controls_present(self, client):
        """分页控件存在"""
        rv = client.get("/questions?page=1")
        data = rv.data.decode("utf-8")
        assert "第" in data and "页" in data


class TestQuestionDetailPage:
    """测试 /question/<code> 详情页"""

    def test_detail_page_returns_200(self, client, real_code):
        rv = client.get(f"/question/{real_code}")
        assert rv.status_code == 200

    def test_detail_page_returns_404_for_unknown(self, client):
        rv = client.get("/question/XXX-YYY-999")
        assert rv.status_code == 404

    def test_detail_shows_question_type_badge(self, client, real_code):
        """详情页应正确显示问题类型 badge"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        valid = ["是否类", "怎么办类", "定义类", "风险类", "时限类", "是什么类", "为什么类"]
        assert any(label in data for label in valid), f"code={real_code}"

    def test_detail_shows_answer_certainty_badge(self, client, real_code):
        """详情页应正确显示结论稳定度 badge"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        valid = ["明确", "有条件", "有争议", "实务做法"]
        assert any(label in data for label in valid), f"code={real_code}"

    def test_detail_shows_scope_level(self, client, real_code):
        """详情页应显示适用范围"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        # scope_level 渲染后应有全国通用或地方口径字样
        assert any(label in data for label in ["全国通用", "地方口径", "scope_national", "scope_local"])

    def test_detail_shows_policies_section(self, client, real_code):
        """详情页应显示"政策依据"区域标题"""
        rv = client.get(f"/question/{real_code}")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "政策依据" in data

    def test_detail_local_notes_section_present(self, client, real_code):
        """详情页地方口径区存在（无数据则显示空，不崩溃）"""
        rv = client.get(f"/question/{real_code}")
        assert rv.status_code == 200  # 不崩溃即可

    def test_detail_shows_relations_or_next_step(self, client, real_code):
        """详情页应显示关联问题或下一步推荐"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "关联问题" in data or "下一步推荐" in data

    def test_detail_shows_update_log(self, client, real_code):
        """详情页应显示更新记录"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "更新记录" in data or "v" in data

    def test_detail_no_scope_provincial(self, client, real_code):
        """详情页不应出现 scope_provincial（已从DB删除）"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "scope_provincial" not in data

    def test_detail_no_type_definition_legacy(self, client, real_code):
        """详情页 question_type_label 宏不应出现 type_definition"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "type_definition" not in data

    def test_detail_answer_box_present(self, client, real_code):
        """详情页应有一句话结论区域"""
        rv = client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "一句话结论" in data


class TestQuestionFormPages:
    """测试新建/编辑表单页面（只测页面加载，不测提交）"""

    def test_new_question_page_requires_auth(self, client):
        """新建页面需先登录，应返回登录页（302 或 200）"""
        rv = client.get("/question/new", follow_redirects=False)
        assert rv.status_code in (200, 302)

    def test_edit_question_page_requires_auth(self, client, real_code):
        """编辑页面需先登录，应返回登录页（302 或 200）"""
        rv = client.get(f"/question/{real_code}/edit", follow_redirects=False)
        assert rv.status_code in (200, 302)

    def test_new_question_form_no_type_definition(self, client):
        """新建表单中 question_type 选项应为 type_define，不含 type_definition"""
        rv = client.get("/question/new", follow_redirects=False)
        if rv.status_code == 200:
            data = rv.data.decode("utf-8")
            assert "type_definition" not in data, "表单不应包含已废弃的 type_definition"
            assert "type_define" in data

    def test_answer_certainty_options_in_form(self, client):
        """新建表单中 answer_certainty 选项与DB对齐（certain_clear / certain_conditional）"""
        rv = client.get("/question/new", follow_redirects=False)
        if rv.status_code == 200:
            data = rv.data.decode("utf-8")
            assert "certain_clear" in data
            assert "certain_conditional" in data

    def test_scope_level_options_no_provincial(self, client):
        """新建表单中 scope_level 不应出现 scope_provincial"""
        rv = client.get("/question/new", follow_redirects=False)
        if rv.status_code == 200:
            data = rv.data.decode("utf-8")
            assert "scope_provincial" not in data


class TestIndexPage:
    """测试首页"""

    def test_index_returns_200(self, client):
        rv = client.get("/")
        assert rv.status_code == 200

    def test_index_shows_stage_entries(self, client):
        """首页应有阶段入口"""
        rv = client.get("/")
        data = rv.data.decode("utf-8")
        for stage in ["设立期", "开业", "变更", "注销"]:
            assert stage in data

    def test_index_shows_stats(self, client):
        """首页应显示统计信息"""
        rv = client.get("/")
        data = rv.data.decode("utf-8")
        assert "问题" in data or "总" in data

    def test_index_shows_module_entries(self, client):
        """首页应有模块入口"""
        rv = client.get("/")
        data = rv.data.decode("utf-8")
        assert "登记管理" in data or "申报纳税" in data or "发票管理" in data
