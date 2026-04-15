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
            keyword=request.args.get('keyword')
        )
        stages = svc.get_stages()
        modules = svc.get_modules()
        all_tags = svc.get_all_tags()
        keyword = request.args.get('keyword', '')

        return render_template('questions.html',
                               stages=stages, modules=modules, all_tags=all_tags,
                               questions=result['questions'], total=result['total'],
                               page=page, page_size=page_size,
                               current_stage=stage, current_module=module, current_tag=tag,
                               keyword=keyword)

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

        if request.method == 'POST':
            data = request.form.to_dict()
            # 处理多选标签
            tag_codes = request.form.getlist('tags')
            try:
                code = svc.create_question(data)
                return f"<script>alert('问题 {code} 创建成功！');window.location.href='/question/{code}';</script>"
            except Exception as e:
                return f"<script>alert('创建失败：{e}');window.history.back();</script>"

        return render_template('new_question.html',
                               stages=stages, modules=modules,
                               business_tags=business_tags)

    # ---------- 导航条加新增入口 ----------
    # （导航条在 base.html 里直接写死，这里不需要改动）

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
