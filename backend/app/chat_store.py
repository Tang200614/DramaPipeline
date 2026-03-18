# 会话与消息存储
# @author fortune
# @date 2026-03-18

import uuid
from datetime import datetime
from app.db import get_db


def create_session(title='新对话'):
    """创建新会话"""
    sid = str(uuid.uuid4())
    now = datetime.utcnow().isoformat() + 'Z'
    with get_db() as conn:
        conn.execute(
            'INSERT INTO chat_sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)',
            (sid, title, now, now),
        )
    return sid


def get_session(session_id):
    """获取会话"""
    with get_db() as conn:
        row = conn.execute('SELECT * FROM chat_sessions WHERE id = ?', (session_id,)).fetchone()
        if not row:
            return None
        return dict(row)


def list_sessions(limit=50):
    """会话列表，按更新时间倒序"""
    with get_db() as conn:
        rows = conn.execute(
            'SELECT id, title, created_at, updated_at FROM chat_sessions ORDER BY updated_at DESC LIMIT ?',
            (limit,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_messages(session_id):
    """获取会话消息列表"""
    with get_db() as conn:
        rows = conn.execute(
            'SELECT id, session_id, role, content, created_at FROM chat_messages WHERE session_id = ? ORDER BY id ASC',
            (session_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def add_message(session_id, role, content):
    """添加消息"""
    now = datetime.utcnow().isoformat() + 'Z'
    with get_db() as conn:
        conn.execute(
            'INSERT INTO chat_messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)',
            (session_id, role, content, now),
        )
        conn.execute(
            'UPDATE chat_sessions SET updated_at = ? WHERE id = ?',
            (now, session_id),
        )


def update_session_title(session_id, title):
    """更新会话标题"""
    now = datetime.utcnow().isoformat() + 'Z'
    with get_db() as conn:
        conn.execute(
            'UPDATE chat_sessions SET title = ?, updated_at = ? WHERE id = ?',
            (title, now, session_id),
        )


def delete_session(session_id):
    """删除会话及消息"""
    with get_db() as conn:
        conn.execute('DELETE FROM chat_messages WHERE session_id = ?', (session_id,))
        conn.execute('DELETE FROM chat_sessions WHERE id = ?', (session_id,))
