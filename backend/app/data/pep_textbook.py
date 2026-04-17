"""
人教版PEP小学英语教材数据（三年级起点）

包含各年级、单元、课时、情景等结构化数据
"""

TEXTBOOK_DATA = {
    "grade3_upper": {
        "grade": 3,
        "semester": "upper",
        "units": [
            {
                "unit_number": 1,
                "title": "Hello!",
                "title_cn": "你好！",
                "lessons": [
                    {
                        "lesson_id": "g3u1_lesson1",
                        "title": "Part A Let's talk",
                        "key_vocabulary": ["hello", "hi", "I", "am", "is", "my", "name"],
                        "key_sentences": [
                            "Hello, I'm ...",
                            "Hi, my name is ...",
                            "What's your name?"
                        ],
                        "scenarios": [
                            {
                                "scenario_id": "g3u1_s1",
                                "name": "Meeting a New Friend",
                                "name_cn": "认识新朋友",
                                "description": "开学第一天，你在教室里遇到了一个新同学，你们互相认识。",
                                "ai_role": "新同学",
                                "user_role": "你自己",
                                "goal": "互相介绍姓名"
                            },
                            {
                                "scenario_id": "g3u1_s2",
                                "name": "At the School Gate",
                                "name_cn": "在校门口",
                                "description": "早上到校门口，你遇到了同班同学，互相打招呼。",
                                "ai_role": "同班同学",
                                "user_role": "你自己",
                                "goal": "用英语打招呼并介绍自己"
                            }
                        ]
                    },
                    {
                        "lesson_id": "g3u1_lesson2",
                        "title": "Part B Let's talk",
                        "key_vocabulary": ["hello", "hi", "goodbye", "bye", "see", "you"],
                        "key_sentences": [
                            "Hello, I'm ...",
                            "Goodbye!",
                            "See you!"
                        ],
                        "scenarios": [
                            {
                                "scenario_id": "g3u1_s3",
                                "name": "After School",
                                "name_cn": "放学后",
                                "description": "放学了，你和同学互相道别。",
                                "ai_role": "好朋友",
                                "user_role": "你自己",
                                "goal": "用英语道别"
                            }
                        ]
                    }
                ]
            },
            {
                "unit_number": 2,
                "title": "Colours",
                "title_cn": "颜色",
                "lessons": [
                    {
                        "lesson_id": "g3u2_lesson1",
                        "title": "Part A Let's talk",
                        "key_vocabulary": ["red", "green", "yellow", "blue", "colour"],
                        "key_sentences": [
                            "What colour is it?",
                            "It's red/green/yellow/blue.",
                            "I see red/green..."
                        ],
                        "scenarios": [
                            {
                                "scenario_id": "g3u2_s1",
                                "name": "Painting Class",
                                "name_cn": "绘画课",
                                "description": "美术课上，老师让大家认识颜色，你和同学一起讨论看到的颜色。",
                                "ai_role": "同学",
                                "user_role": "你自己",
                                "goal": "识别和说出颜色"
                            },
                            {
                                "scenario_id": "g3u2_s2",
                                "name": "Rainbow After Rain",
                                "name_cn": "雨后的彩虹",
                                "description": "下雨后天晴了，天空出现了彩虹，你和朋友讨论彩虹的颜色。",
                                "ai_role": "朋友",
                                "user_role": "你自己",
                                "goal": "描述彩虹的颜色"
                            }
                        ]
                    },
                    {
                        "lesson_id": "g3u2_lesson2",
                        "title": "Part B Let's talk",
                        "key_vocabulary": ["red", "green", "yellow", "blue", "black", "white", "brown"],
                        "key_sentences": [
                            "Colour it brown!",
                            "OK!",
                            "I see blue/green..."
                        ],
                        "scenarios": [
                            {
                                "scenario_id": "g3u2_s3",
                                "name": "Colouring a Picture",
                                "name_cn": "给画涂色",
                                "description": "你和同学一起给一幅画涂色，讨论用什么颜色。",
                                "ai_role": "同学",
                                "user_role": "你自己",
                                "goal": "表达颜色偏好并涂色"
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "grade3_lower": {
        "grade": 3,
        "semester": "lower",
        "units": [
            {
                "unit_number": 1,
                "title": "Welcome back to school!",
                "title_cn": "欢迎回到学校！",
                "lessons": [
                    {
                        "lesson_id": "g3d1_lesson1",
                        "title": "Part A Let's talk",
                        "key_vocabulary": ["boy", "girl", "teacher", "student", "new", "friend"],
                        "key_sentences": [
                            "Hi, I'm ...",
                            "I'm from ...",
                            "Welcome!"
                        ],
                        "scenarios": [
                            {
                                "scenario_id": "g3d1_s1",
                                "name": "New Semester",
                                "name_cn": "新学期",
                                "description": "新学期开始了，班上来了新同学，大家互相介绍。",
                                "ai_role": "新同学",
                                "user_role": "你自己",
                                "goal": "介绍自己和欢迎新同学"
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "grade4_upper": {
        "grade": 4,
        "semester": "upper",
        "units": [
            {
                "unit_number": 1,
                "title": "My classroom",
                "title_cn": "我的教室",
                "lessons": [
                    {
                        "lesson_id": "g4u1_lesson1",
                        "title": "Part A Let's talk",
                        "key_vocabulary": ["classroom", "window", "door", "picture", "light", "blackboard"],
                        "key_sentences": [
                            "What's in the classroom?",
                            "Let's go and see.",
                            "It's near the window."
                        ],
                        "scenarios": [
                            {
                                "scenario_id": "g4u1_s1",
                                "name": "New Classroom",
                                "name_cn": "新教室",
                                "description": "你们搬到了新教室，你和同学一起参观并讨论教室里有什么。",
                                "ai_role": "同学",
                                "user_role": "你自己",
                                "goal": "描述教室里的物品和位置"
                            }
                        ]
                    }
                ]
            }
        ]
    }
}


def get_textbook(grade: int, semester: str) -> dict:
    """
    获取指定年级和学期的教材数据

    参数:
        grade: 年级 (1-6)
        semester: 学期 ("upper" 上册 / "lower" 下册)

    返回:
        教材数据字典，如果不存在则返回None
    """
    key = f"grade{grade}_{semester}"
    return TEXTBOOK_DATA.get(key)


def get_unit(grade: int, semester: str, unit_number: int) -> dict:
    """
    获取指定单元数据

    参数:
        grade: 年级
        semester: 学期
        unit_number: 单元号

    返回:
        单元数据字典，如果不存在则返回None
    """
    textbook = get_textbook(grade, semester)
    if not textbook:
        return None

    for unit in textbook.get("units", []):
        if unit["unit_number"] == unit_number:
            return unit

    return None


def get_lesson(grade: int, semester: str, lesson_id: str) -> dict:
    """
    获取指定课时数据

    参数:
        grade: 年级
        semester: 学期
        lesson_id: 课时ID

    返回:
        课时数据字典，如果不存在则返回None
    """
    textbook = get_textbook(grade, semester)
    if not textbook:
        return None

    for unit in textbook.get("units", []):
        for lesson in unit.get("lessons", []):
            if lesson["lesson_id"] == lesson_id:
                return lesson

    return None


def get_scenario(grade: int, semester: str, scenario_id: str) -> dict:
    """
    获取指定情景数据

    参数:
        grade: 年级
        semester: 学期
        scenario_id: 情景ID

    返回:
        情景数据字典，如果不存在则返回None
    """
    textbook = get_textbook(grade, semester)
    if not textbook:
        return None

    for unit in textbook.get("units", []):
        for lesson in unit.get("lessons", []):
            for scenario in lesson.get("scenarios", []):
                if scenario["scenario_id"] == scenario_id:
                    return scenario

    return None


def get_all_grades() -> list:
    """获取所有可用的年级学期列表"""
    result = []
    for key in TEXTBOOK_DATA:
        parts = key.replace("grade", "").split("_")
        grade = int(parts[0])
        semester = parts[1]
        result.append({"grade": grade, "semester": semester, "key": key})
    return result
