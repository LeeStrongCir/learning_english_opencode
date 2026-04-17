import json
import logging
from app.services.llm_service import llm_service
from app.prompts.report_template import build_report_prompt
from app.models.report import (
    DialogueReport,
    PronunciationScore,
    GrammarScore,
    VocabularyUsage,
)

logger = logging.getLogger(__name__)


class ReportService:
    """学习报告生成服务"""

    async def generate_report(self, session, key_vocabulary, key_sentences) -> DialogueReport:
        """
        根据对话会话生成学习报告

        参数:
            session: DialogueSession对象，包含完整的对话历史
            key_vocabulary: 目标词汇列表
            key_sentences: 目标句型列表

        返回:
            DialogueReport对象
        """
        try:
            # 构建对话历史（只取用户的消息用于分析）
            conversation_history = [
                {"role": msg.role, "content": msg.content} for msg in session.messages
            ]

            # 构建报告生成Prompt
            messages = build_report_prompt(conversation_history, key_vocabulary, key_sentences)

            # 调用LLM生成报告
            response_text = await llm_service.chat_completion(
                messages=messages,
                temperature=0.3,  # 使用较低温度以获得更稳定的分析结果
            )

            # 解析LLM返回的JSON
            report_data = self._parse_llm_response(response_text)

            # 构建报告对象
            report = DialogueReport(
                session_id=session.session_id,
                total_turns=len([m for m in session.messages if m.role == "user"]),
                pronunciation=PronunciationScore(
                    overall=report_data.get("pronunciation", {}).get("overall", 70.0),
                    details=report_data.get("pronunciation", {}).get("details", {}),
                ),
                grammar=GrammarScore(
                    overall=report_data.get("grammar", {}).get("overall", 70.0),
                    errors=report_data.get("grammar", {}).get("errors", []),
                ),
                vocabulary=VocabularyUsage(
                    target_words_used=report_data.get("vocabulary", {}).get("target_words_used", []),
                    target_words_missed=report_data.get("vocabulary", {}).get("target_words_missed", []),
                    accuracy=report_data.get("vocabulary", {}).get("accuracy", 0.0),
                ),
                overall_score=report_data.get("overall_score", 70.0),
                strengths=report_data.get("strengths", ["继续加油！"]),
                improvements=report_data.get("improvements", ["多多练习"]),
                encouragement=report_data.get("encouragement", "你很棒，继续努力！"),
            )

            return report

        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            # 返回默认报告
            return self._generate_default_report(session)

    def _parse_llm_response(self, response_text: str) -> dict:
        """
        解析LLM返回的JSON响应

        参数:
            response_text: LLM返回的文本

        返回:
            解析后的字典
        """
        # 尝试直接解析JSON
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass

        # 尝试从Markdown代码块中提取JSON
        try:
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_str = response_text.split("```")[1].split("```")[0].strip()
            else:
                json_str = response_text

            return json.loads(json_str)
        except (json.JSONDecodeError, IndexError) as e:
            logger.error(f"解析LLM报告JSON失败: {str(e)}")
            raise

    def _generate_default_report(self, session) -> DialogueReport:
        """
        生成默认报告（当LLM调用失败时使用）

        参数:
            session: DialogueSession对象

        返回:
            默认的DialogueReport对象
        """
        user_messages = [m for m in session.messages if m.role == "user"]
        return DialogueReport(
            session_id=session.session_id,
            total_turns=len(user_messages),
            pronunciation=PronunciationScore(overall=70.0, details={}),
            grammar=GrammarScore(overall=70.0, errors=[]),
            vocabulary=VocabularyUsage(
                target_words_used=[],
                target_words_missed=[],
                accuracy=0.0,
            ),
            overall_score=70.0,
            strengths=["完成了对话练习"],
            improvements=["建议多练习目标词汇和句型"],
            encouragement="完成对话就是进步，继续加油！",
        )


# 全局报告服务实例
report_service = ReportService()
