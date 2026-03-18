# prompt 模板加载与变量解析
# 支持 {{variable}} 格式占位符，便于自定义 prompt 与微调场景
# @author 举顾（technology@yiju.net）
# @date 2026-03-18 22:00:00

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

# 模板目录，相对于 app 包
_PROMPTS_DIR = Path(__file__).resolve().parent


def _read_template(name: str) -> str:
    """
    从 prompts 目录读取模板文件内容。
    name: 模板名（不含扩展名），如 chat_system
    """
    for ext in ('.txt', '.md', ''):
        path = _PROMPTS_DIR / f'{name}{ext}'
        if path.exists():
            return path.read_text(encoding='utf-8')
    return ''


def load_prompt(name: str) -> str:
    """
    加载指定名称的 prompt 模板原始内容（不做变量替换）。
    name: 模板名，如 chat_system、chat_user
    """
    return _read_template(name)


def render_prompt(name: str, variables: Optional[Dict[str, Any]] = None) -> str:
    """
    加载模板并按 variables 替换 {{key}} 占位符。
    variables: 键值对，如 {"role": "助手", "context": "..."}
    """
    template = load_prompt(name)
    if not template:
        return ''
    variables = variables or {}
    # 支持 {{var}} 格式，未提供则替换为空
    def repl(m: re.Match) -> str:
        key = m.group(1)
        val = variables.get(key, '')
        return str(val) if val is not None else ''
    return re.sub(r'\{\{(\w+)\}\}', repl, template)
