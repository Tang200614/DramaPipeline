# LangGraph 对话流程图：支持流式 token、prompt 模板、模型适配
# @author fortune
# @date 2026-03-18 22:00:00

import logging
import time
from typing import Any, Dict, Generator, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage

logger = logging.getLogger(__name__)
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import MessagesState

from app.graph.model_adapter import get_chat_model
from app.prompts.loader import render_prompt


def _to_langchain_messages(api_messages: List[Dict[str, Any]]) -> List[BaseMessage]:
    """
    将 API 格式消息 [{"role":"user","content":"..."}] 转为 LangChain BaseMessage 列表。
    """
    out: List[BaseMessage] = []
    for m in api_messages:
        role = (m.get('role') or 'user').lower()
        content = m.get('content', '') or ''
        if role == 'system':
            out.append(SystemMessage(content=content))
        elif role == 'user':
            out.append(HumanMessage(content=content))
        elif role == 'assistant':
            out.append(AIMessage(content=content))
    return out


def build_chat_graph(
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> Any:
    """
    构建对话 LangGraph。单节点调用 LLM，便于流式输出。
    model: 模型名，未传则用环境变量
    system_prompt: 系统 prompt，未传则从 chat_system 模板加载
    """
    llm = get_chat_model(model=model)
    if llm is None:
        raise RuntimeError('未配置 DASHSCOPE_API_KEY 或 LangChain 依赖缺失')

    sys_prompt = system_prompt or render_prompt('chat_system')

    def call_model(state: MessagesState) -> dict:
        messages = state['messages']
        if not any(isinstance(m, SystemMessage) for m in messages):
            messages = [SystemMessage(content=sys_prompt)] + list(messages)
        response = llm.invoke(messages)
        return {'messages': [response]}

    workflow = StateGraph(MessagesState)
    workflow.add_node('chat', call_model)
    workflow.add_edge(START, 'chat')
    workflow.add_edge('chat', END)
    return workflow.compile()


def stream_chat(
    messages: List[Dict[str, Any]],
    model: Optional[str] = None,
    system_prompt: Optional[str] = None,
) -> Generator[str, None, None]:
    """
    流式对话生成器，逐 token 产出内容。
    直接调用 llm.stream() 保证逐 token 输出，避免 invoke 被缓冲。
    """
    llm = get_chat_model(model=model)
    if llm is None:
        raise RuntimeError('未配置 DASHSCOPE_API_KEY 或 LangChain 依赖缺失')
    sys_prompt = system_prompt or render_prompt('chat_system')
    lc_messages = _to_langchain_messages(messages)
    if not any(isinstance(m, SystemMessage) for m in lc_messages):
        lc_messages = [SystemMessage(content=sys_prompt)] + list(lc_messages)
    chunk_idx = 0
    for chunk in llm.stream(lc_messages):
        if hasattr(chunk, 'content') and chunk.content:
            chunk_idx += 1
            logger.info('[stream_chat] chunk#%d len=%d content=%r ts=%.3f', chunk_idx, len(chunk.content), chunk.content[:50], time.time())
            yield chunk.content
