# DramaPipeline Flask 应用入口
# @author fortune
# @date 2026-03-18 21:55:00

import logging
from flask import Flask, jsonify
from flask_cors import CORS

logger = logging.getLogger(__name__)


def create_app():
    """创建 Flask 应用实例"""
    app = Flask(__name__)

    @app.errorhandler(Exception)
    def handle_error(e):
        logger.exception('未捕获异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200

    # 加载环境变量
    app.config.from_prefixed_env()
    # 初始化 SQLite
    from app.db import init_db
    init_db()
    # 跨域配置（开发环境允许所有来源，避免 403）
    CORS(app, resources={r'/api/*': {'origins': '*'}}, supports_credentials=False)
    # 注册路由
    from app.routes import health, api, chat
    app.register_blueprint(health.bp, url_prefix='/api')
    app.register_blueprint(api.bp, url_prefix='/api')
    app.register_blueprint(chat.bp, url_prefix='/api')
    return app
