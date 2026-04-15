# ============================================================
# backend/routes/tags.py
# 标签相关 API 路由
# ============================================================

from flask import Blueprint, jsonify
from services.question_service import QuestionService

tags_bp = Blueprint('tags', __name__)
svc = QuestionService()

@tags_bp.route('/', methods=['GET'])
def get_all_tags():
    """获取所有标签"""
    return jsonify(svc.get_all_tags())

@tags_bp.route('/business', methods=['GET'])
def get_business_tags():
    """获取业务标签"""
    return jsonify(svc.get_business_tags())
