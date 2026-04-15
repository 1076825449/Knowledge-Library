# ============================================================
# backend/routes/questions.py
# 问题相关 API 路由
# ============================================================

from flask import Blueprint, request, jsonify
from services.question_service import QuestionService

questions_bp = Blueprint('questions', __name__)
svc = QuestionService()

@questions_bp.route('/', methods=['GET'])
def list_questions():
    """问题列表"""
    stage = request.args.get('stage')
    module = request.args.get('module')
    tag = request.args.get('tag')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))

    result = svc.list_questions(
        stage=stage,
        module=module,
        tag=tag,
        page=page,
        page_size=page_size
    )
    return jsonify(result)

@questions_bp.route('/<question_code>', methods=['GET'])
def get_question(question_code):
    """问题详情"""
    result = svc.get_question_detail(question_code)
    if result:
        return jsonify(result)
    return jsonify({'error': '问题不存在'}), 404

@questions_bp.route('/stages', methods=['GET'])
def get_stages():
    """获取所有生命周期阶段"""
    return jsonify(svc.get_stages())

@questions_bp.route('/modules', methods=['GET'])
def get_modules():
    """获取所有主题模块"""
    return jsonify(svc.get_modules())

@questions_bp.route('/high-frequency', methods=['GET'])
def get_high_frequency():
    """高频问题"""
    limit = int(request.args.get('limit', 10))
    return jsonify(svc.get_high_frequency(limit))

@questions_bp.route('/newbie', methods=['GET'])
def get_newbie():
    """新手必看"""
    limit = int(request.args.get('limit', 10))
    return jsonify(svc.get_newbie(limit))

@questions_bp.route('/recent-updates', methods=['GET'])
def get_recent_updates():
    """最近更新"""
    limit = int(request.args.get('limit', 10))
    return jsonify(svc.get_recent_updates(limit))
