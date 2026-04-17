import json


def build_report_prompt(conversation_history, key_vocabulary, key_sentences):
    """
    构建报告生成Prompt

    参数:
        conversation_history: 完整对话历史 [{"role": "ai"/"user", "content": "..."}]
        key_vocabulary: 目标词汇列表
        key_sentences: 目标句型列表

    返回:
        完整的messages列表，用于发送给LLM生成报告
    """

    # 格式化对话历史
    formatted_history = ""
    for i, msg in enumerate(conversation_history):
        role_cn = "AI" if msg["role"] == "ai" else "学生"
        formatted_history += f"第{i+1}轮 [{role_cn}]: {msg['content']}\n"

    system_prompt = f"""你是一个专业的小学英语教师评估助手。请分析以下对话记录，为学生的学习表现生成详细的学习报告。

## 目标词汇
{', '.join(key_vocabulary)}

## 目标句型
{chr(10).join(key_sentences)}

## 对话记录
{formatted_history}

## 评估要求
请从以下维度进行评估：

1. **发音评分** (pronunciation): 根据学生使用的词汇难度和语言表现给出0-100的评分。如果有明显的发音相关文字线索（如拼写错误），请在details中列出相关单词的评分。

2. **语法评分** (grammar): 分析学生的语法使用情况，找出错误并给出纠正建议。overall为0-100分。errors数组中每个错误包含original(原句)、corrected(纠正后)、explanation(解释)。

3. **词汇使用** (vocabulary): 统计学生使用了哪些目标词汇(target_words_used)，遗漏了哪些(target_words_missed)，计算准确率(accuracy = 使用的目标词数 / 总目标词数 * 100)。

4. **总体评分** (overall_score): 综合以上各项的0-100分。

5. **优点** (strengths): 列出2-3个学生做得好的地方，用中文描述，语气积极鼓励。

6. **改进建议** (improvements): 列出2-3个可以改进的地方，用中文描述，语气温和鼓励。

7. **鼓励话语** (encouragement): 写一段鼓励孩子的话，用中文，温暖有力量，50字以内。

## 输出格式
请严格返回以下JSON格式（不要添加任何其他内容）：
{{
    "pronunciation": {{
        "overall": 85.0,
        "details": {{"hello": 90.0, "name": 80.0}}
    }},
    "grammar": {{
        "overall": 80.0,
        "errors": [{{"original": "I am name is", "corrected": "My name is", "explanation": "介绍名字应该用My name is"}}]
    }},
    "vocabulary": {{
        "target_words_used": ["hello", "name"],
        "target_words_missed": ["hi"],
        "accuracy": 66.7
    }},
    "overall_score": 82.0,
    "strengths": ["敢于开口说英语，非常勇敢", "能正确使用hello打招呼"],
    "improvements": ["可以多练习介绍自己的句型", "注意区分I和my的用法"],
    "encouragement": "你今天表现很棒！继续加油，相信你会越来越厉害的！"
}}"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "请分析以上对话，生成学习报告，只返回JSON。"},
    ]

    return messages
