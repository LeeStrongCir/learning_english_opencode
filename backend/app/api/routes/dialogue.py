import uuid
import time
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.models.dialogue import (
    DialogueSession,
    DialogueRequest,
    DialogueTurnRequest,
    DialogueTurnResponse,
    Message,
)
from app.models.report import DialogueReport
from app.services.llm_service import llm_service
from app.services.tts_service import tts_service
from app.services.report_service import report_service
from app.data.pep_textbook import get_lesson, get_scenario, get_textbook
from app.prompts.dialogue_template import build_dialogue_prompt, build_first_turn_prompt

logger = logging.getLogger(__name__)

router = APIRouter()

# 内存存储对话会话（生产环境应使用数据库）
dialogue_sessions: dict[str, DialogueSession] = {}


@router.post("/start", response_model=DialogueSession)
async def start_dialogue(request: DialogueRequest):
    """
    开始新对话

    根据教材信息创建新的对话会话，AI会首先根据情景开场
    """
    # 根据年级确定学期（简化处理，1-3年级上册对应grade3_upper）
    semester = "upper" if request.grade <= 3 else "lower"
    grade_key = f"grade{request.grade}_{semester}"

    # 获取教材数据
    lesson = get_lesson(request.grade, semester, request.lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail=f"课时 {request.lesson_id} 不存在")

    scenario = get_scenario(request.grade, semester, request.scenario_id)

    if not scenario:
        raise HTTPException(status_code=404, detail=f"情景 {request.scenario_id} 不存在")

    # 创建新会话
    session_id = str(uuid.uuid4())
    session = DialogueSession(
        session_id=session_id,
        grade=request.grade,
        unit=request.unit,
        lesson_id=request.lesson_id,
        scenario_id=request.scenario_id,
    )

    # 构建第一轮对话Prompt，让AI开场
    messages = build_first_turn_prompt(
        scenario=scenario,
        key_vocabulary=lesson["key_vocabulary"],
        key_sentences=lesson["key_sentences"],
        grade=request.grade,
    )

    try:
        # 调用LLM生成开场白
        ai_content = await llm_service.chat_completion(messages, temperature=0.7)

        # 添加AI开场消息
        session.messages.append(Message(role="ai", content=ai_content))

    except Exception as e:
        logger.error(f"生成开场白失败: {str(e)}")
        # 使用默认开场白
        default_greeting = f"Hello! I'm your new friend. Let's talk about {scenario.get('name', 'today')}! What's your name?"
        session.messages.append(Message(role="ai", content=default_greeting))

    # 保存会话
    dialogue_sessions[session_id] = session

    return session


@router.post("/turn", response_model=DialogueTurnResponse)
async def dialogue_turn(request: DialogueTurnRequest):
    """
    发送一轮对话

    用户发送消息后，AI会根据情景和对话历史生成回复
    """
    # 获取会话
    session = dialogue_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="对话会话不存在或已过期")

    if not session.is_active:
        raise HTTPException(status_code=400, detail="对话已结束")

    # 添加用户消息
    session.messages.append(Message(role="user", content=request.user_message))

    # 获取教材数据
    semester = "upper" if session.grade <= 3 else "lower"
    lesson = get_lesson(session.grade, semester, session.lesson_id)

    scenario = get_scenario(session.grade, semester, session.scenario_id)

    if not lesson or not scenario:
        raise HTTPException(status_code=404, detail="教材数据不存在")

    # 构建对话历史
    conversation_history = [
        {"role": msg.role, "content": msg.content} for msg in session.messages[:-1]  # 排除刚添加的用户消息
    ]

    # 构建对话Prompt
    messages = build_dialogue_prompt(
        scenario=scenario,
        key_vocabulary=lesson["key_vocabulary"],
        key_sentences=lesson["key_sentences"],
        grade=session.grade,
        conversation_history=conversation_history,
        user_message=request.user_message,
    )

    try:
        # 调用LLM生成回复
        ai_content = await llm_service.chat_completion(messages, temperature=0.7)
    except Exception as e:
        logger.error(f"生成AI回复失败: {str(e)}")
        ai_content = "Good job! Can you say more? (抱歉，我暂时无法回复，请再说一次)"

    # 添加AI回复
    session.messages.append(Message(role="ai", content=ai_content))

    # 生成TTS音频（模拟）
    audio_url = None
    try:
        audio_url = await tts_service.synthesize_to_url(ai_content)
    except Exception as e:
        logger.warning(f"TTS合成失败: {str(e)}")

    # 计算当前轮次
    turn_number = len([m for m in session.messages if m.role == "user"])

    return DialogueTurnResponse(
        session_id=session.session_id,
        ai_message=ai_content,
        audio_url=audio_url,
        turn_number=turn_number,
    )


@router.get("/{session_id}")
async def get_dialogue(session_id: str):
    """
    获取对话历史

    返回指定会话的完整对话记录
    """
    session = dialogue_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="对话会话不存在")

    return {
        "session_id": session.session_id,
        "grade": session.grade,
        "unit": session.unit,
        "lesson_id": session.lesson_id,
        "scenario_id": session.scenario_id,
        "messages": session.messages,
        "is_active": session.is_active,
        "total_turns": len([m for m in session.messages if m.role == "user"]),
    }


@router.post("/{session_id}/end", response_model=DialogueReport)
async def end_dialogue(session_id: str):
    """
    结束对话并生成学习报告

    标记会话为已结束，并调用LLM分析对话生成学习报告
    """
    session = dialogue_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="对话会话不存在")

    if not session.is_active:
        raise HTTPException(status_code=400, detail="对话已结束")

    # 标记会话为已结束
    session.is_active = False

    # 获取教材数据
    semester = "upper" if session.grade <= 3 else "lower"
    lesson = get_lesson(session.grade, semester, session.lesson_id)

    if not lesson:
        raise HTTPException(status_code=404, detail="教材数据不存在")

    # 生成报告
    report = await report_service.generate_report(
        session=session,
        key_vocabulary=lesson["key_vocabulary"],
        key_sentences=lesson["key_sentences"],
    )

    return report
