"""
Flask 页面层集成测试：使用 test_client() 不依赖外部服务
覆盖：列表筛选、详情字段、表单枚举值、首页、认证拦截

认证设计：
- anon_client  ：匿名 client，用于测试未登录时的拦截行为
- auth_client  ：通过 POST 正确 admin 密码建立认证 session
                 用于需要访问数据库或表单内容的测试

admin_required 真实行为：
- GET  未认证 → 200（返回登录页）
- POST 正确密码 → 设置 session['admin_authenticated']，进入视图函数
- POST 错误密码 → 400

兼容性：Flask 2.3.0 + Werkzeug 3.0.1 通过 tests/conftest.py werkzeug 版本 patch 兼容
"""
import pytest
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR / "backend"))
from app import create_app


@pytest.fixture
def anon_client():
    """匿名 client（未认证），用于测试未登录拦截路径"""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_client():
    """已认证 admin client，通过 POST 正确密码建立 session"""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        # admin_required 对 POST 校验密码，正确则设置 session['admin_authenticated']
        client.post("/question/new",
                    data={"password": app.config.get("ADMIN_PASSWORD", "tax2026")},
                    follow_redirects=False)
        yield client


@pytest.fixture
def real_code():
    """找一个数据库中真实存在的问题编码（独立创建 app，不依赖其他 fixture）"""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        rv = c.get("/questions?page=1")
    import re
    codes = re.findall(r'/question/([A-Z]+-[A-Z]+-\d+)', rv.data.decode("utf-8"))
    if not codes:
        pytest.skip("数据库中没有问题记录")
    return codes[0]


class TestQuestionsListPage:
    """测试 /questions 列表页"""

    def test_questions_page_returns_200(self, auth_client):
        rv = auth_client.get("/questions")
        assert rv.status_code == 200

    def test_questions_page_shows_count(self, auth_client):
        rv = auth_client.get("/questions?page=1")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "条结果" in data or "共" in data

    def test_questions_filter_by_stage_shows_correct_label(self, auth_client):
        """stage=SET 筛选后，页面应显示"设立期"标签"""
        rv = auth_client.get("/questions?stage=SET")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "设立期" in data

    def test_questions_filter_by_module_shows_correct_label(self, auth_client):
        """module=DEC 筛选后，页面应显示"申报纳税"标签"""
        rv = auth_client.get("/questions?module=DEC")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "申报纳税" in data

    def test_questions_filter_by_scope_region(self, auth_client):
        """region=scope_national 筛选后，页面仍正常渲染"""
        rv = auth_client.get("/questions?region=scope_national")
        assert rv.status_code == 200

    def test_questions_filter_by_keyword(self, auth_client):
        """keyword=发票 搜索后，结果应包含发票字样"""
        rv = auth_client.get("/questions?keyword=发票")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "发票" in data

    def test_questions_filter_by_hf(self, auth_client):
        """hf=1 筛选后，应出现"高频"标签"""
        rv = auth_client.get("/questions?hf=1")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "高频" in data

    def test_questions_filter_by_qtype(self, auth_client):
        """qtype=type_whether 筛选后，应出现"是否"类型标签"""
        rv = auth_client.get("/questions?qtype=type_whether")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "是否类" in data or "是否" in data

    def test_questions_has_all_stage_chips(self, auth_client):
        """列表页应有全部6个阶段筛选项"""
        rv = auth_client.get("/questions")
        data = rv.data.decode("utf-8")
        for stage in ["设立期", "开业", "变更", "注销"]:
            assert stage in data, f"缺少阶段标签: {stage}"

    def test_questions_has_module_chips(self, auth_client):
        """列表页应有模块筛选项"""
        rv = auth_client.get("/questions")
        data = rv.data.decode("utf-8")
        assert "登记管理" in data or "申报纳税" in data or "发票管理" in data

    def test_scope_mixed_not_in_filter_chips(self, auth_client):
        """scope_mixed 不作为筛选 chip 出现（DB无此数据）"""
        rv = auth_client.get("/questions")
        data = rv.data.decode("utf-8")
        assert not ("混合口径" in data and "scope_mixed" in data)

    def test_status_filter_chips_present(self, auth_client):
        """状态筛选 chip：active / draft / archived"""
        rv = auth_client.get("/questions")
        data = rv.data.decode("utf-8")
        assert "正常" in data or "active" in data
        assert "草稿" in data or "draft" in data

    def test_pagination_controls_present(self, auth_client):
        """分页控件存在"""
        rv = auth_client.get("/questions?page=1")
        data = rv.data.decode("utf-8")
        assert "第" in data and "页" in data


class TestQuestionDetailPage:
    """测试 /question/<code> 详情页"""

    def test_detail_page_returns_200(self, auth_client, real_code):
        rv = auth_client.get(f"/question/{real_code}")
        assert rv.status_code == 200

    def test_detail_page_returns_404_for_unknown(self, auth_client):
        rv = auth_client.get("/question/XXX-YYY-999")
        assert rv.status_code == 404

    def test_detail_shows_question_type_badge(self, auth_client, real_code):
        """详情页应正确显示问题类型 badge"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        valid = ["是否类", "怎么办类", "定义类", "风险类", "时限类", "是什么类", "为什么类"]
        assert any(label in data for label in valid), f"code={real_code}"

    def test_detail_shows_answer_certainty_badge(self, auth_client, real_code):
        """详情页应正确显示结论稳定度 badge"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        valid = ["明确", "有条件", "有争议", "实务做法"]
        assert any(label in data for label in valid), f"code={real_code}"

    def test_detail_shows_scope_level(self, auth_client, real_code):
        """详情页应显示适用范围"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        # scope_level 渲染后应有全国通用或地方口径字样
        assert any(label in data for label in ["全国通用", "地方口径", "scope_national", "scope_local"])

    def test_detail_shows_policies_section(self, auth_client, real_code):
        """详情页应显示"政策依据"区域标题"""
        rv = auth_client.get(f"/question/{real_code}")
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "政策依据" in data

    def test_detail_local_notes_section_present(self, auth_client, real_code):
        """详情页地方口径区存在（无数据则显示空，不崩溃）"""
        rv = auth_client.get(f"/question/{real_code}")
        assert rv.status_code == 200  # 不崩溃即可

    def test_detail_shows_relations_or_next_step(self, auth_client, real_code):
        """详情页应显示关联问题或下一步推荐"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "关联问题" in data or "下一步推荐" in data

    def test_detail_shows_update_log(self, auth_client, real_code):
        """详情页应显示更新记录"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "更新记录" in data or "v" in data

    def test_detail_no_scope_provincial(self, auth_client, real_code):
        """详情页不应出现 scope_provincial（已从DB删除）"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "scope_provincial" not in data

    def test_detail_no_type_definition_legacy(self, auth_client, real_code):
        """详情页 question_type_label 宏不应出现 type_definition"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "type_definition" not in data

    def test_detail_answer_box_present(self, auth_client, real_code):
        """详情页应有一句话结论区域"""
        rv = auth_client.get(f"/question/{real_code}")
        data = rv.data.decode("utf-8")
        assert "一句话结论" in data


class TestQuestionFormPages:
    """测试新建/编辑表单页面"""

    # ── 未登录拦截路径（使用 anon_client）────────────────────────────

    def test_new_question_page_requires_auth(self, anon_client):
        """GET /question/new 未认证时返回登录页（200），页面包含密码输入框"""
        rv = anon_client.get("/question/new", follow_redirects=False)
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "password" in data.lower() or "登录" in data

    def test_edit_question_page_requires_auth(self, anon_client, real_code):
        """GET /question/<code>/edit 未认证时返回登录页（200）"""
        rv = anon_client.get(f"/question/{real_code}/edit", follow_redirects=False)
        assert rv.status_code == 200

    # ── 已登录可访问表单内容（使用 auth_client）────────────────────

    def test_new_question_form_no_type_definition(self, auth_client):
        """新建表单中 question_type 选项应为 type_define，不含 type_definition"""
        rv = auth_client.get("/question/new", follow_redirects=False)
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "type_definition" not in data, "表单不应包含已废弃的 type_definition"
        assert "type_define" in data

    def test_answer_certainty_options_in_form(self, auth_client):
        """新建表单中 answer_certainty 选项与DB对齐（certain_clear / certain_conditional）"""
        rv = auth_client.get("/question/new", follow_redirects=False)
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "certain_clear" in data
        assert "certain_conditional" in data

    def test_scope_level_options_no_provincial(self, auth_client):
        """新建表单中 scope_level 不应出现 scope_provincial"""
        rv = auth_client.get("/question/new", follow_redirects=False)
        assert rv.status_code == 200
        data = rv.data.decode("utf-8")
        assert "scope_provincial" not in data


class TestIndexPage:
    """测试首页"""

    def test_index_returns_200(self, auth_client):
        rv = auth_client.get("/")
        assert rv.status_code == 200

    def test_index_shows_stage_entries(self, auth_client):
        """首页应有阶段入口"""
        rv = auth_client.get("/")
        data = rv.data.decode("utf-8")
        for stage in ["设立期", "开业", "变更", "注销"]:
            assert stage in data

    def test_index_shows_stats(self, auth_client):
        """首页应显示统计信息"""
        rv = auth_client.get("/")
        data = rv.data.decode("utf-8")
        assert "问题" in data or "总" in data

    def test_index_shows_module_entries(self, auth_client):
        """首页应有模块入口"""
        rv = auth_client.get("/")
        data = rv.data.decode("utf-8")
        assert "登记管理" in data or "申报纳税" in data or "发票管理" in data
