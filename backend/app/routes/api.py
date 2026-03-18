# 主 API 路由
# @author fortune
# @date 2026-03-18 21:55:00

from flask import Blueprint, jsonify, request
import os

bp = Blueprint('api', __name__)


@bp.route('/status', methods=['GET'])
def get_status():
    """获取系统状态（参考 zeroclaw）"""
    return jsonify({
        'provider': 'dramapipeline',
        'model': os.getenv('DASHSCOPE_MODEL', 'qwen3.5-plus'),
        'uptime_seconds': 0,
        'gateway_port': 5001,
        'locale': 'zh-CN',
        'memory_backend': 'memory',
        'paired': True,
        'channels': {},
        'health': {
            'components': {
                'api': {'status': 'ok', 'restart_count': 0},
                'backend': {'status': 'ok', 'restart_count': 0}
            }
        }
    })


@bp.route('/config', methods=['GET'])
def get_config():
    """获取配置（占位）"""
    return jsonify({
        'format': 'json',
        'content': '{}'
    })
