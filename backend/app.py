# ============================================================
# backend/app.py
# Flask 应用入口
# ============================================================

import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response
from flask_cors import CORS
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

from routes.questions import questions_bp
from routes.search import search_bp
from routes.tags import tags_bp
from config import Config
from metadata import (
    QUESTION_TYPE_META, ANSWER_CERTAINTY_META, SCOPE_LEVEL_META,
    STATUS_META, POLICY_LEVEL_META, POLICY_STATUS_META,
    SUPPORT_TYPE_META, RELATION_TYPE_META, STAGE_LABELS, MODULE_LABELS,
    active_options, all_options,
)

def create_app():
    app = Flask(__name__,
                 template_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'),
                 static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))
    app.secret_key = Config.SECRET_KEY
    CORS(app)
    app.jinja_env.add_extension('jinja2.ext.do')

    # 注册蓝图
    app.register_blueprint(questions_bp, url_prefix='/api/questions')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(tags_bp, url_prefix='/api/tags')

    @app.context_processor
    def inject_metadata():
        return {
            'site_name': Config.SITE_NAME,
            'site_url': Config.SITE_URL.rstrip('/'),
            'site_description': Config.SITE_DESCRIPTION,
            'question_type_meta': QUESTION_TYPE_META,
            'answer_certainty_meta': ANSWER_CERTAINTY_META,
            'scope_level_meta': SCOPE_LEVEL_META,
            'status_meta': STATUS_META,
            'policy_level_meta': POLICY_LEVEL_META,
            'policy_status_meta': POLICY_STATUS_META,
            'support_type_meta': SUPPORT_TYPE_META,
            'relation_type_meta': RELATION_TYPE_META,
            'stage_labels': STAGE_LABELS,
            'module_labels': MODULE_LABELS,
            'question_type_options': all_options(QUESTION_TYPE_META),
            'active_question_type_options': active_options(QUESTION_TYPE_META),
            'answer_certainty_options': all_options(ANSWER_CERTAINTY_META),
            'scope_level_options': all_options(SCOPE_LEVEL_META),
            'status_options': [
                {'code': 'active', 'label': STATUS_META['active']['label']},
                {'code': 'draft', 'label': STATUS_META['draft']['label']},
                {'code': 'archived', 'label': STATUS_META['archived']['label']},
            ],
            'support_type_options': all_options(SUPPORT_TYPE_META),
            'relation_type_options': all_options(RELATION_TYPE_META),
        }

    # ---------- 认证工具函数 ----------
    def get_authenticated_user():
        """返回当前登录用户信息，无则返回 None"""
        user_id = session.get('user_id')
        if not user_id:
            return None
        import sqlite3
        conn = sqlite3.connect(str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db'))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM users WHERE id = ? AND is_active = 1', (user_id,)).fetchone()
        conn.close()
        return dict(user) if user else None

    def require_auth(roles=None):
        """验证登录状态的装饰器，roles 可为 str 或 list"""
        if isinstance(roles, str):
            roles = [roles]
        def decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                user = get_authenticated_user()
                if not user:
                    if request.is_json:
                        return jsonify({'error': '请先登录'}), 401
                    return redirect(url_for('login'))
                if roles and user['role'] not in roles:
                    if request.is_json:
                        return jsonify({'error': '权限不足'}), 403
                    return redirect(url_for('index'))
                return f(*args, **kwargs)
            return decorated
        return decorator

    def require_login(f):
        return require_auth()(f)

    def require_admin(f):
        return require_auth('admin')(f)

    # ---------- 登录 / 登出 ----------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '')
            if not username or not password:
                return render_template('admin_login.html', error='请输入用户名和密码')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            user = cur.execute(
                "SELECT * FROM users WHERE username = ? AND is_active = 1", (username,)
            ).fetchone()
            conn.close()
            if user and check_password_hash(user['password_hash'], password):
                session.clear()
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                next_url = request.args.get('next', '/')
                return redirect(next_url)
            return render_template('admin_login.html', error='用户名或密码错误')
        if get_authenticated_user():
            return redirect(url_for('index'))
        return render_template('admin_login.html', error=None)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    # ---------- 用户管理（admin only） ----------
    @app.route('/admin/users')
    @require_admin
    def admin_users():
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        users = cur.execute("SELECT id, username, display_name, role, is_active, created_at, last_login FROM users ORDER BY id").fetchall()
        conn.close()
        return render_template('admin_users.html', users=[dict(u) for u in users])

    @app.route('/admin/users/add', methods=['POST'])
    @require_admin
    def admin_add_user():
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        display_name = request.form.get('display_name', '').strip()
        role = request.form.get('role', 'viewer')
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        if len(password) < 8:
            return jsonify({'error': '密码长度至少8位'}), 400
        if role not in ('admin', 'editor', 'reviewer', 'viewer'):
            return jsonify({'error': '无效的角色'}), 400
        pw_hash = generate_password_hash(password)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, display_name, role) VALUES (?, ?, ?, ?)",
                (username, pw_hash, display_name or username, role)
            )
            conn.commit()
            return jsonify({'success': True})
        except sqlite3.IntegrityError:
            return jsonify({'error': '用户名已存在'}), 409
        finally:
            conn.close()

    @app.route('/admin/users/<int:user_id>/toggle', methods=['POST'])
    @require_admin
    def admin_toggle_user(user_id):
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_active = NOT is_active WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    @app.route('/admin/users/<int:user_id>/change-role', methods=['POST'])
    @require_admin
    def admin_change_role(user_id):
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        role = request.form.get('role', '')
        if role not in ('admin', 'editor', 'reviewer', 'viewer'):
            return jsonify({'error': '无效的角色'}), 400
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    @app.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
    @require_admin
    def admin_reset_password(user_id):
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        password = request.form.get('password', '')
        if len(password) < 8:
            return jsonify({'error': '密码长度至少8位'}), 400
        pw_hash = generate_password_hash(password)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (pw_hash, user_id))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

    @app.route('/profile', methods=['GET', 'POST'])
    @require_login
    def profile():
        import sqlite3
        db_path = str(Path(__file__).parent.parent / 'database' / 'db' / 'tax_knowledge.db')
        user = get_authenticated_user()
        if request.method == 'POST':
            display_name = request.form.get('display_name', '').strip()
            new_password = request.form.get('new_password', '')
            if new_password:
                if len(new_password) < 8:
                    return render_template('profile.html', user=user, error='新密码长度至少8位')
                pw_hash = generate_password_hash(new_password)
            else:
                pw_hash = None
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            if pw_hash:
                cur.execute("UPDATE users SET display_name = ?, password_hash = ? WHERE id = ?",
                            (display_name, pw_hash, user['id']))
            else:
                cur.execute("UPDATE users SET display_name = ? WHERE id = ?",
                            (display_name, user['id']))
            conn.commit()
            conn.close()
            return redirect(url_for('profile'))
        return render_template('profile.html', user=user, error=None)

    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    @app.route('/robots.txt')
    def robots_txt():
        body = "\n".join([
            "User-agent: *",
            "Allow: /",
            f"Sitemap: {Config.SITE_URL.rstrip('/')}/sitemap.xml",
            ""
        ])
        return Response(body, mimetype='text/plain')

    @app.route('/sitemap.xml')
    def sitemap_xml():
        from services.question_service import QuestionService
        svc = QuestionService()
        base = Config.SITE_URL.rstrip('/')
        static_pages = [
            ('/', None),
            ('/questions', None),
            ('/about', None),
            ('/methodology', None),
            ('/launch-readiness', None),
        ]
        urls = [(f"{base}{path}", lastmod) for path, lastmod in static_pages]
        for item in svc.get_all_active_question_codes():
            urls.append((f"{base}/question/{item['question_code']}", item.get('updated_at')))

        xml = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        for loc, lastmod in urls:
            xml.append("  <url>")
            xml.append(f"    <loc>{loc}</loc>")
            if lastmod:
                xml.append(f"    <lastmod>{lastmod}</lastmod>")
            xml.append("  </url>")
        xml.append("</urlset>")
        return Response("\n".join(xml), mimetype='application/xml')

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
        stats = svc.get_stats()
        return render_template('index.html',
                               stages=stages, modules=modules,
                               high_freq=high_freq, newbie=newbie, recent=recent,
                               stats=stats)

    @app.route('/about')
    def about():
        from services.question_service import QuestionService
        svc = QuestionService()
        return render_template('about.html', stats=svc.get_stats())

    @app.route('/methodology')
    def methodology():
        from services.question_service import QuestionService
        svc = QuestionService()
        return render_template('methodology.html', stats=svc.get_stats())

    @app.route('/launch-readiness')
    def launch_readiness():
        from services.question_service import QuestionService
        svc = QuestionService()
        return render_template('launch_readiness.html', stats=svc.get_stats())

    @app.route('/questions')
    def questions_list():
        from services.question_service import QuestionService
        svc = QuestionService()
        stage = request.args.get('stage')
        module = request.args.get('module')
        tag = request.args.get('tag')
        qtype = request.args.get('qtype')
        page = int(request.args.get('page', 1))
        page_size = 10

        result = svc.list_questions(
            stage=stage, module=module, tag=tag,
            page=page, page_size=page_size,
            hf=request.args.get('hf'),
            newbie=request.args.get('newbie'),
            keyword=request.args.get('keyword'),
            region=request.args.get('region'),
            status=request.args.get('status'),
            qtype=qtype
        )
        stages = svc.get_stages()
        modules = svc.get_modules()
        all_tags = svc.get_all_tags()
        business_tags = [t for t in all_tags if t['tag_category'] == 'business']
        question_types = svc.get_question_types()
        keyword = request.args.get('keyword', '')
        current_region = request.args.get('region', '')
        current_status = request.args.get('status', '')

        return render_template('questions.html',
                               stages=stages, modules=modules, all_tags=all_tags,
                               business_tags=business_tags,
                               questions=result['questions'], total=result['total'],
                               page=page, page_size=page_size,
                               current_stage=stage, current_module=module, current_tag=tag,
                               keyword=keyword,
                               current_region=current_region, current_status=current_status,
                               question_types=question_types, current_qtype=qtype)

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
    @require_admin
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
            # to_dict() loses multi-value fields (e.g. multiple tags checked)
            # Re-add tags as a list so create_question can process them
            data['tags'] = request.form.getlist('tags')
            # 处理多选标签
            tag_codes = data.get('tags')
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
            except ValueError as e:
                return render_template('new_question.html',
                                       stages=stages, modules=modules,
                                       business_tags=business_tags,
                                       all_policies=all_policies,
                                       form_error=str(e)), 400
            except Exception as e:
                return f"<script>alert('创建失败：{e}');window.history.back();</script>"

        return render_template('new_question.html',
                               stages=stages, modules=modules,
                               business_tags=business_tags,
                               all_policies=all_policies)

    # ---------- 编辑问题页面 ----------
    @app.route('/question/<question_code>/edit', methods=['GET', 'POST'])
    @require_admin
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
            # to_dict() loses multi-value fields (multiple tags checked)
            data['tags'] = request.form.getlist('tags')

            # 解析关联问题
            relations = []
            for i in range(5):  # 最多5条关联
                rel_code = request.form.get(f'relation_code_{i}', '').strip()
                rel_type = request.form.get(f'relation_type_{i}', 'related')
                rel_order = request.form.get(f'relation_order_{i}', '1').strip()
                if rel_code:
                    relations.append({
                        'related_code': rel_code,
                        'relation_type': rel_type,
                        'display_order': int(rel_order) if rel_order.isdigit() else 1
                    })
            data['relations'] = relations

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
            except ValueError as e:
                # 校验错误：重新渲染编辑表单并显示错误
                stages = svc.get_stages()
                modules = svc.get_modules()
                all_tags = svc.get_all_tags()
                business_tags = [t for t in all_tags if t['tag_category'] == 'business']
                all_policies = svc.get_all_policies()
                return render_template('edit_question.html',
                                       detail=detail, stages=stages, modules=modules,
                                       all_tags=all_tags, business_tags=business_tags,
                                       all_policies=all_policies,
                                       form_error=str(e)), 400
            except Exception as e:
                return f"<script>alert('更新失败：{e}');window.history.back();</script>"

        return render_template('edit_question.html',
                               detail=detail, stages=stages, modules=modules,
                               all_tags=all_tags, business_tags=business_tags,
                               all_policies=all_policies)

    @app.route('/admin/quality')
    @require_admin
    def admin_quality():
        from services.question_service import QuestionService
        svc = QuestionService()
        gaps = svc.get_quality_gaps(limit=200)
        summary = svc.get_quality_gap_summary()
        return render_template('quality_dashboard.html', gaps=gaps, summary=summary)

    # ---------- 导航条加新增入口 ----------
    # （导航条在 base.html 里直接写死，这里不需要改动）

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
