# 健康检查路由
# @author fortune
# @date 2026-03-18 21:55:00

from flask import Blueprint, jsonify

bp = Blueprint('health', __name__)


@bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'ok',
        'message': 'DramaPipeline API 运行正常',
        'service': 'dramapipeline'
    })
