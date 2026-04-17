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

@tags_bp.route('', methods=['POST'])
def create_tag():
    """创建新标签（仅 business 类型）"""
    from flask import request, jsonify
    data = request.get_json() or {}
    tag_code = (data.get('tag_code') or '').strip()
    tag_name = (data.get('tag_name') or '').strip()
    if not tag_code or not tag_name:
        return jsonify({'error': 'tag_code 和 tag_name 均不能为空'}), 400
    if len(tag_code) > 64:
        return jsonify({'error': 'tag_code 长度不能超过 64'}), 400
    if len(tag_name) > 128:
        return jsonify({'error': 'tag_name 长度不能超过 128'}), 400
    try:
        svc.create_tag(tag_code, tag_name, tag_category='business')
        return jsonify({'success': True, 'tag_code': tag_code}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 409
