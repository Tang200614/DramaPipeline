# 模型适配层：统一 ChatModel 获取，便于接入通义、微调模型等
# @author fortune
# @date 2026-03-18 22:00:00

import os
from typing import Any, Optional

try:
    from langchain_community.chat_models.tongyi import ChatTongyi
    _CHAT_TONGYI_AVAILABLE = True
except ImportError:
    _CHAT_TONGYI_AVAILABLE = False


def get_chat_model(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    streaming: bool = True,
) -> Optional[Any]:
    """
    获取 ChatModel 实例。优先使用通义，后续可扩展微调模型。
    model: 模型名，如 qwen-plus、qwen-turbo，或微调模型 ID
    api_key: DashScope API Key，未传则从环境变量读取
    streaming: 是否启用流式（LangGraph 会通过 stream_mode 捕获 token）
    """
    api_key = (api_key or os.getenv('DASHSCOPE_API_KEY', '')).strip()
    if not api_key:
        return None
    model = model or os.getenv('DASHSCOPE_MODEL', 'qwen-plus')
    if not _CHAT_TONGYI_AVAILABLE:
        return None
    # 通义兼容微调模型：传入微调后的 model_id 即可
    return ChatTongyi(
        model=model,
        api_key=api_key,
        streaming=streaming,
    )
