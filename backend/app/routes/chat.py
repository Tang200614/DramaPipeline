# 对话路由 - LangGraph 封装，支持流式 SSE、prompt 解析、模型适配（便于微调）
# @author fortune
# @date 2026-03-18

import os
import json
import logging
import requests
from flask import Blueprint, request, jsonify, Response, stream_with_context
from app.chat_store import (
    create_session,
    get_session,
    list_sessions,
    get_messages,
    add_message,
    update_session_title,
    delete_session,
)

logger = logging.getLogger(__name__)

bp = Blueprint('chat', __name__)

# OpenAI 兼容模式（LangGraph 不可用时回退）
COMPATIBLE_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
TEXT_GEN_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
MULTIMODAL_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'

# LangGraph 流式（优先使用）
try:
    from app.graph.chat_graph import stream_chat
    _LANGGRAPH_AVAILABLE = True
except ImportError:
    _LANGGRAPH_AVAILABLE = False


@bp.route('/chat/completion', methods=['POST'])
def chat_completion():
    """对话接口，调用通义 DashScope API"""
    try:
        data = request.get_json() or {}
        messages = data.get('messages', [])
        model = data.get('model') or os.getenv('DASHSCOPE_MODEL', 'qwen-plus')

        if not messages:
            return jsonify({'code': 0, 'msg': 'messages 不能为空', 'data': None}), 200

        api_key = os.getenv('DASHSCOPE_API_KEY', '').strip()
        if not api_key:
            logger.error('DASHSCOPE_API_KEY 未配置')
            return jsonify({
                'code': 0,
                'msg': '服务端未配置通义 API Key，请在 .env 中设置 DASHSCOPE_API_KEY',
                'data': None
            }), 200

        # qwen3.5 系列走 multimodal 端点
        use_multimodal = '3.5' in model or 'vl' in model.lower()
        url = MULTIMODAL_URL if use_multimodal else TEXT_GEN_URL

        payload = {
            'model': model,
            'input': {'messages': messages},
            'parameters': {'result_format': 'message'},
        }

        resp = requests.post(
            url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=60,
        )

        try:
            body = resp.json() if resp.text else {}
        except ValueError:
            body = {'message': resp.text[:200] if resp.text else '无效响应'}
        if resp.status_code >= 400 or body.get('code', '') not in ('', '200'):
            err_msg = body.get('message', '') or f'HTTP {resp.status_code}'
            logger.error('通义 API 错误: status=%s code=%s', resp.status_code, body.get('code'))
            return jsonify({
                'code': 0,
                'msg': f'通义 API 错误: {err_msg}',
                'data': None
            }), 200

        output = body.get('output', {})
        choices = output.get('choices', [])
        content = ''
        if choices:
            msg = choices[0].get('message', {})
            raw = msg.get('content', '')
            if isinstance(raw, list):
                # multimodal 返回 [{"text":"..."}]
                content = ''.join(p.get('text', '') for p in raw if isinstance(p, dict))
            else:
                content = raw or ''
        if not content:
            content = output.get('text', '')

        logger.info('chat 出参成功 reply_len=%d', len(content or ''))
        return jsonify({
            'code': 1,
            'msg': '成功',
            'data': {'content': content or '', 'role': 'assistant'}
        })
    except requests.RequestException as e:
        logger.exception('chat 请求异常: %s', e)
        return jsonify({
            'code': 0,
            'msg': f'网络请求失败: {str(e)}',
            'data': None
        }), 200
    except Exception as e:
        logger.exception('chat 异常: %s', e)
        return jsonify({
            'code': 0,
            'msg': f'请求失败: {str(e)}',
            'data': None
        }), 200


@bp.route('/chat/completion/stream', methods=['POST'])
def chat_completion_stream():
    """流式对话接口，SSE 推送。优先 LangGraph，回退兼容模式 API"""
    try:
        data = request.get_json() or {}
        messages = data.get('messages', [])
        model = data.get('model') or os.getenv('DASHSCOPE_MODEL', 'qwen-plus')
        session_id = data.get('session_id')
        system_prompt = data.get('system_prompt')

        if not messages:
            return jsonify({'code': 0, 'msg': 'messages 不能为空', 'data': None}), 200

        user_content = messages[-1].get('content', '') if messages and messages[-1].get('role') == 'user' else ''
        if not session_id:
            title = (user_content[:30] + '...') if len(user_content) > 30 else (user_content or '新对话')
            session_id = create_session(title)
        add_message(session_id, 'user', user_content)

        api_key = os.getenv('DASHSCOPE_API_KEY', '').strip()
        if not api_key:
            return jsonify({
                'code': 0,
                'msg': '服务端未配置通义 API Key',
                'data': None
            }), 200

        # qwen3.5 系列需走 compatible-mode，ChatTongyi 的默认 URL 不支持
        # 环境变量 STREAM_USE_COMPATIBLE=1 时强制走兼容模式
        use_compatible = (
            os.getenv('STREAM_USE_COMPATIBLE', '').strip() in ('1', 'true', 'yes')
            or '3.5' in model or 'vl' in model.lower()
        )
        if use_compatible:
            return _stream_via_compatible_api(messages, model, session_id)
        if _LANGGRAPH_AVAILABLE:
            return _stream_via_langgraph(messages, model, session_id, system_prompt)
        return _stream_via_compatible_api(messages, model, session_id)
    except Exception as e:
        logger.exception('chat stream 异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200


def _stream_via_langgraph(messages, model, session_id, system_prompt):
    """通过 LangGraph 流式输出，逐 token 推送，禁用缓冲"""
    full_content = []

    def generate():
        nonlocal full_content
        try:
            token_idx = 0
            for token in stream_chat(
                messages=messages,
                model=model,
                system_prompt=system_prompt,
            ):
                token_idx += 1
                full_content.append(token)
                logger.info('[SSE yield] token#%d len=%d', token_idx, len(token))
                chunk = f'data: {json.dumps({"content": token, "session_id": session_id}, ensure_ascii=False)}\n\n'
                yield chunk.encode('utf-8')
        except Exception as e:
            logger.exception('LangGraph stream 异常: %s', e)
            yield f'data: {json.dumps({"error": str(e), "session_id": session_id}, ensure_ascii=False)}\n\n'.encode('utf-8')
        finally:
            assistant_text = ''.join(full_content)
            if assistant_text:
                add_message(session_id, 'assistant', assistant_text)
            # 流式结束标记，供前端更新 loading 状态
            yield f'data: {json.dumps({"done": True, "session_id": session_id}, ensure_ascii=False)}\n\n'.encode('utf-8')

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
        },
        direct_passthrough=True,
    )


def _stream_via_compatible_api(messages, model, session_id):
    """兼容模式 API 流式输出，直连 DashScope"""
    print(f'[stream] 开始 compatible API model={model}', flush=True)
    payload = {
        'model': model,
        'messages': messages,
        'stream': True,
        'stream_options': {'include_usage': True},
    }
    if '3.5' in model or 'vl' in model.lower():
        payload['enable_thinking'] = False
    resp = requests.post(
        COMPATIBLE_URL,
        headers={
            'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY")}',
            'Content-Type': 'application/json',
        },
        json=payload,
        stream=True,
        timeout=120,
    )
    if resp.status_code >= 400:
        err = resp.text[:500] if resp.text else f'HTTP {resp.status_code}'
        print(f'[stream] DashScope 错误: {err}', flush=True)
        logger.error('通义流式 API 错误: %s', err)
        return jsonify({'code': 0, 'msg': f'通义 API 错误: {err}', 'data': None}), 200

    full_content = []
    chunk_idx = 0

    def generate():
        nonlocal full_content, chunk_idx
        line_count = 0
        for line in resp.iter_lines(decode_unicode=True):
            line_count += 1
            if line and line.startswith('data: '):
                chunk = line[6:]
                if chunk.strip() == '[DONE]':
                    print(f'[stream] 结束 共 {chunk_idx} 块', flush=True)
                    yield f'data: {json.dumps({"done": True, "session_id": session_id}, ensure_ascii=False)}\n\n'.encode('utf-8')
                    break
                try:
                    obj = json.loads(chunk)
                    choices = obj.get('choices', [])
                    if choices:
                        delta = choices[0].get('delta', {})
                        content = delta.get('content', '') or ''
                        reasoning = delta.get('reasoning_content', '') or ''
                        if content:
                            chunk_idx += 1
                            full_content.append(content)
                            yield f'data: {json.dumps({"content": content, "session_id": session_id}, ensure_ascii=False)}\n\n'.encode('utf-8')
                        elif reasoning:
                            yield f': keepalive\n\n'.encode('utf-8')
                except json.JSONDecodeError:
                    print(f'[stream] JSON 解析失败: {chunk[:80]}', flush=True)
                    continue
        assistant_text = ''.join(full_content)
        if assistant_text:
            add_message(session_id, 'assistant', assistant_text)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
        },
        direct_passthrough=True,
    )


@bp.route('/chat/sessions', methods=['GET'])
def chat_sessions_list():
    """会话列表"""
    try:
        limit = request.args.get('limit', 50, type=int)
        sessions = list_sessions(limit=limit)
        return jsonify({'code': 1, 'msg': '成功', 'data': {'sessions': sessions}})
    except Exception as e:
        logger.exception('sessions list 异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200


@bp.route('/chat/sessions', methods=['POST'])
def chat_sessions_create():
    """创建新会话"""
    try:
        data = request.get_json() or {}
        title = data.get('title', '新对话')
        sid = create_session(title)
        return jsonify({'code': 1, 'msg': '成功', 'data': {'session_id': sid}})
    except Exception as e:
        logger.exception('session create 异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200


@bp.route('/chat/sessions/<session_id>', methods=['GET'])
def chat_sessions_detail(session_id):
    """会话详情（含消息列表，即记忆 memory）"""
    try:
        session = get_session(session_id)
        if not session:
            return jsonify({'code': 0, 'msg': '会话不存在', 'data': None}), 200
        messages = get_messages(session_id)
        msgs = [{'role': m['role'], 'content': m['content']} for m in messages]
        return jsonify({
            'code': 1,
            'msg': '成功',
            'data': {
                'session': dict(session),
                'messages': msgs,
            },
        })
    except Exception as e:
        logger.exception('session detail 异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200


@bp.route('/chat/sessions/<session_id>', methods=['DELETE'])
def chat_sessions_delete(session_id):
    """删除会话"""
    try:
        delete_session(session_id)
        return jsonify({'code': 1, 'msg': '成功', 'data': None})
    except Exception as e:
        logger.exception('session delete 异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200


@bp.route('/chat/sessions/<session_id>/title', methods=['PATCH'])
def chat_sessions_update_title(session_id):
    """更新会话标题"""
    try:
        data = request.get_json() or {}
        title = data.get('title', '')
        if not title:
            return jsonify({'code': 0, 'msg': 'title 不能为空', 'data': None}), 200
        update_session_title(session_id, title)
        return jsonify({'code': 1, 'msg': '成功', 'data': None})
    except Exception as e:
        logger.exception('session update title 异常: %s', e)
        return jsonify({'code': 0, 'msg': str(e), 'data': None}), 200
