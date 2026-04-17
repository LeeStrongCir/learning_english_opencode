from pydantic import BaseModel


class PronunciationScore(BaseModel):
    """发音评分"""
    overall: float  # 0-100
    details: dict[str, float] = {}  # 单词 -> 分数


class GrammarScore(BaseModel):
    """语法评分"""
    overall: float
    errors: list[dict] = []  # [{ "original": "", "corrected": "", "explanation": "" }]


class VocabularyUsage(BaseModel):
    """词汇使用情况"""
    target_words_used: list[str]
    target_words_missed: list[str]
    accuracy: float


class DialogueReport(BaseModel):
    """对话学习报告"""
    session_id: str
    total_turns: int
    pronunciation: PronunciationScore
    grammar: GrammarScore
    vocabulary: VocabularyUsage
    overall_score: float
    strengths: list[str]
    improvements: list[str]
    encouragement: str
