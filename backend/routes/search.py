# ============================================================
# backend/routes/search.py
# 搜索相关 API 路由
# ============================================================

from flask import Blueprint, request, jsonify
from services.question_service import QuestionService

search_bp = Blueprint('search', __name__)
svc = QuestionService()

@search_bp.route('/', methods=['GET'])
def search():
    """搜索问题"""
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))

    if not keyword:
        return jsonify({'questions': [], 'total': 0})

    result = svc.list_questions(
        stage=request.args.get('stage'),
        module=request.args.get('module'),
        tag=request.args.get('tag'),
        page=page,
        page_size=page_size,
        keyword=keyword,
        region=request.args.get('region'),
        status=request.args.get('status'),
        qtype=request.args.get('qtype'),
        hf=request.args.get('hf'),
        newbie=request.args.get('newbie'),
    )
    result['keyword'] = keyword
    return jsonify(result)
