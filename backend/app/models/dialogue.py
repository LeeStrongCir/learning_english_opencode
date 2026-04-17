from pydantic import BaseModel
import time


class Message(BaseModel):
    """对话消息"""
    role: str  # "ai" 或 "user"
    content: str
    timestamp: float = None

    def __init__(self, **data):
        if "timestamp" not in data:
            data["timestamp"] = time.time()
        super().__init__(**data)


class DialogueSession(BaseModel):
    """对话会话"""
    session_id: str
    grade: int
    unit: int
    lesson_id: str
    scenario_id: str
    messages: list[Message] = []
    is_active: bool = True
    created_at: float = None

    def __init__(self, **data):
        if "created_at" not in data:
            data["created_at"] = time.time()
        super().__init__(**data)


class DialogueRequest(BaseModel):
    """开始对话请求"""
    grade: int
    unit: int
    lesson_id: str
    scenario_id: str


class DialogueTurnRequest(BaseModel):
    """对话一轮请求"""
    session_id: str
    user_message: str  # 用户说的话（文字）


class DialogueTurnResponse(BaseModel):
    """对话一轮响应"""
    session_id: str
    ai_message: str
    audio_url: str = None  # TTS生成的音频URL
    turn_number: int
