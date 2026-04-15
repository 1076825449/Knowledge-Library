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

    result = svc.search_questions(keyword, page, page_size)
    return jsonify(result)
