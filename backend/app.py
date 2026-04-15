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

        result = svc.list_questions(stage=stage, module=module, tag=tag, page=page, page_size=page_size)
        stages = svc.get_stages()
        modules = svc.get_modules()
        all_tags = svc.get_all_tags()

        return render_template('questions.html',
                               stages=stages, modules=modules, all_tags=all_tags,
                               questions=result['questions'], total=result['total'],
                               page=page, page_size=page_size,
                               current_stage=stage, current_module=module, current_tag=tag)

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
