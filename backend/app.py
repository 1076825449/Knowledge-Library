# ============================================================
# backend/app.py
# Flask 应用入口
# ============================================================

import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from routes.questions import questions_bp
from routes.search import search_bp
from routes.tags import tags_bp

def create_app():
    app = Flask(__name__,
                 template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
                 static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))
    CORS(app)

    # 注册蓝图
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(tags_bp, url_prefix='/api/tags')

    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    # ---------- 前端页面路由 ----------
    @app.route('/')
    def index():
        from services.question_service import QuestionService
        svc = QuestionService()
        stages = svc.get_stages()
        modules = svc.get_modules()
        high_freq = svc.get_high_frequency(limit=6)
        newbie = svc.get_newbie(limit=6)
        recent = svc.get_recent_updates(limit=6)
        return render_template('index.html',
                               stages=stages, modules=modules,
                               high_freq=high_freq, newbie=newbie, recent=recent)

    @app.route('/questions')
    def questions_list():
        from services.question_service import QuestionService
        svc = QuestionService()
        stage = request.args.get('stage')
        module = request.args.get('module')
        tag = request.args.get('tag')
        page = int(request.args.get('page', 1))
        page_size = 10

        result = svc.list_questions(
            stage=stage, module=module, tag=tag,
            page=page, page_size=page_size,
            hf=request.args.get('hf'),
            newbie=request.args.get('newbie'),
            keyword=request.args.get('keyword'),
            region=request.args.get('region'),
            status=request.args.get('status')
        )
        stages = svc.get_stages()
        modules = svc.get_modules()
        all_tags = svc.get_all_tags()
        keyword = request.args.get('keyword', '')
        current_region = request.args.get('region', '')
        current_status = request.args.get('status', '')

        return render_template('questions.html',
                               stages=stages, modules=modules, all_tags=all_tags,
                               questions=result['questions'], total=result['total'],
                               page=page, page_size=page_size,
                               current_stage=stage, current_module=module, current_tag=tag,
                               keyword=keyword,
                               current_region=current_region, current_status=current_status)

    @app.route('/question/<question_code>')
    def question_detail(question_code):
        from services.question_service import QuestionService
        svc = QuestionService()
        detail = svc.get_question_detail(question_code)
        if not detail:
            return "问题不存在", 404
        stages = svc.get_stages()
        modules = svc.get_modules()
        return render_template('detail.html',
                               detail=detail, stages=stages, modules=modules)

    # ---------- 新增问题页面 ----------
    @app.route('/question/new', methods=['GET', 'POST'])
    def new_question():
        from services.question_service import QuestionService
        svc = QuestionService()
        stages = svc.get_stages()
        modules = svc.get_modules()
        all_tags = svc.get_all_tags()
        business_tags = [t for t in all_tags if t['tag_category'] == 'business']
        all_policies = svc.get_all_policies()

        if request.method == 'POST':
            data = request.form.to_dict()
            # 处理多选标签
            tag_codes = request.form.getlist('tags')
            try:
                code = svc.create_question(data)
                # 处理政策依据关联（最多3条）
                for i in range(1, 4):
                    policy_id = request.form.get(f'policy_id_{i}')
                    support_type = request.form.get(f'support_type_{i}')
                    support_note = request.form.get(f'support_note_{i}', '')
                    if policy_id and support_type:
                        svc.add_policy_link(code, int(policy_id), support_type, support_note, i)
                return f"<script>alert('问题 {code} 创建成功！');window.location.href='/question/{code}';</script>"
            except Exception as e:
                return f"<script>alert('创建失败：{e}');window.history.back();</script>"

        return render_template('new_question.html',
                               stages=stages, modules=modules,
                               business_tags=business_tags,
                               all_policies=all_policies)

    # ---------- 编辑问题页面 ----------
    @app.route('/question/<question_code>/edit', methods=['GET', 'POST'])
    def edit_question(question_code):
        from services.question_service import QuestionService
        svc = QuestionService()
        detail = svc.get_question_detail(question_code)
        if not detail:
            return "问题不存在", 404

        stages = svc.get_stages()
        modules = svc.get_modules()
        all_tags = svc.get_all_tags()
        business_tags = [t for t in all_tags if t['tag_category'] == 'business']
        all_policies = svc.get_all_policies()

        if request.method == 'POST':
            data = request.form.to_dict()
            try:
                svc.update_question(question_code, data)
                # 处理政策关联更新（简化：先删再插）
                cur_policy_ids = [p['id'] for p in detail.get('policies', [])]
                for i in range(1, 4):
                    policy_id_str = request.form.get(f'policy_id_{i}')
                    support_type = request.form.get(f'support_type_{i}')
                    support_note = request.form.get(f'support_note_{i}', '')
                    if policy_id_str and support_type:
                        policy_id = int(policy_id_str)
                        if policy_id not in cur_policy_ids:
                            svc.add_policy_link(question_code, policy_id, support_type, support_note, i)
                        else:
                            # 已存在，删掉让 add_policy_link 重插
                            svc.remove_policy_link(question_code, policy_id)
                            svc.add_policy_link(question_code, policy_id, support_type, support_note, i)
                return f"<script>alert('问题 {question_code} 更新成功！');window.location.href='/question/{question_code}';</script>"
            except Exception as e:
                return f"<script>alert('更新失败：{e}');window.history.back();</script>"

        return render_template('edit_question.html',
                               detail=detail, stages=stages, modules=modules,
                               business_tags=business_tags, all_policies=all_policies)

    # ---------- 导航条加新增入口 ----------
    # （导航条在 base.html 里直接写死，这里不需要改动）

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
