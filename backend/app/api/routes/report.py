import logging

from fastapi import APIRouter, HTTPException

from app.models.report import DialogueReport
from app.api.routes.dialogue import dialogue_sessions
from app.services.report_service import report_service
from app.data.pep_textbook import get_lesson

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{session_id}", response_model=DialogueReport)
async def get_report(session_id: str):
    """
    获取学习报告

    根据会话ID获取对应的学习报告。
    如果报告尚未生成（对话未结束），会实时生成。
    """
    # 获取会话
    session = dialogue_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="对话会话不存在")

    # 获取教材数据
    semester = "upper" if session.grade <= 3 else "lower"
    lesson = get_lesson(session.grade, semester, session.lesson_id)

    if not lesson:
        raise HTTPException(status_code=404, detail="教材数据不存在")

    # 如果对话还未结束，也可以生成报告
    report = await report_service.generate_report(
        session=session,
        key_vocabulary=lesson["key_vocabulary"],
        key_sentences=lesson["key_sentences"],
    )

    return report
