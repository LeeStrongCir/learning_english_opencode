from pydantic import BaseModel
from typing import Optional


class Grade(BaseModel):
    """年级和学期"""
    grade: int  # 1-6年级
    semester: str  # "upper" 上册 / "lower" 下册


class Unit(BaseModel):
    """单元信息"""
    unit_number: int
    title: str
    title_cn: str  # 中文标题


class Lesson(BaseModel):
    """课时信息"""
    lesson_id: str
    unit_number: int
    title: str
    key_vocabulary: list[str]
    key_sentences: list[str]


class Scenario(BaseModel):
    """情景信息"""
    scenario_id: str
    lesson_id: str
    name: str
    name_cn: str
    description: str  # 情景描述
    ai_role: str  # AI扮演的角色
    user_role: str  # 用户扮演的角色
    goal: str  # 对话目标
