def build_dialogue_prompt(scenario, key_vocabulary, key_sentences, grade, conversation_history, user_message):
    """
    构建对话Prompt

    参数:
        scenario: 情景对象，包含ai_role, user_role, description, goal等
        key_vocabulary: 目标词汇列表
        key_sentences: 目标句型列表
        grade: 年级 (1-6)
        conversation_history: 对话历史列表 [{"role": "ai"/"user", "content": "..."}]
        user_message: 用户当前消息

    返回:
        完整的messages列表，用于发送给LLM
    """

    # 根据年级调整语言难度
    grade_level = {
        1: "非常简单，使用最基础的单词和短句",
        2: "很简单，使用基础单词和短句",
        3: "简单，使用常见单词和简单句",
        4: "适中，可以使用稍复杂的句子",
        5: "中等偏上，可以使用复合句",
        6: "中等，可以使用较丰富的词汇和句型",
    }
    language_level = grade_level.get(grade, grade_level[3])

    # 构建系统提示词
    system_prompt = f"""你是一个专业的小学英语情景对话老师。现在你要和一个小学{grade}年级的孩子进行英语对话练习。

## 当前情景
- 情景名称: {scenario.name_cn}
- 情景描述: {scenario.description}
- 你扮演的角色: {scenario.ai_role}
- 孩子扮演的角色: {scenario.user_role}
- 对话目标: {scenario.goal}

## 目标词汇
{', '.join(key_vocabulary)}

## 目标句型
{chr(10).join(key_sentences)}

## 对话规则
1. 请完全代入"{scenario.ai_role}"这个角色，用第一人称与孩子对话
2. 引导孩子使用上面的目标词汇和句型进行对话
3. 使用{language_level}的英语，确保{grade}年级的孩子能理解
4. 每次回复控制在1-3句话，不要太长
5. 孩子说英语时，如果犯错，先给予鼓励（如"Good try!" "Nice effort!"），然后温和地纠正
6. 必要时可以用简短的中文解释帮助孩子理解
7. 对话控制在8-12轮后自然结束，结束时要表扬孩子
8. 保持积极、友好、有耐心的态度
9. 回复格式：主要用英语，需要解释时可以用中文（用括号标注）

请现在开始对话，保持角色一致性。"""

    # 构建消息列表
    messages = [{"role": "system", "content": system_prompt}]

    # 添加对话历史
    for msg in conversation_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # 添加用户当前消息
    messages.append({"role": "user", "content": user_message})

    return messages


def build_first_turn_prompt(scenario, key_vocabulary, key_sentences, grade):
    """
    构建第一轮对话的Prompt（没有用户消息时，AI先开场）

    参数:
        scenario: 情景对象
        key_vocabulary: 目标词汇列表
        key_sentences: 目标句型列表
        grade: 年级

    返回:
        完整的messages列表
    """
    system_prompt = f"""你是一个专业的小学英语情景对话老师。现在你要和一个小学{grade}年级的孩子进行英语对话练习。

## 当前情景
- 情景名称: {scenario.name_cn}
- 情景描述: {scenario.description}
- 你扮演的角色: {scenario.ai_role}
- 孩子扮演的角色: {scenario.user_role}
- 对话目标: {scenario.goal}

## 目标词汇
{', '.join(key_vocabulary)}

## 目标句型
{chr(10).join(key_sentences)}

## 要求
1. 请完全代入"{scenario.ai_role}"这个角色
2. 用简单友好的英语开场，开始这个情景对话
3. 第一句话要自然引入情景，并邀请孩子参与
4. 使用适合{grade}年级的简单英语
5. 回复控制在1-2句话

请生成开场白。"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "请开始这个情景对话，用你的角色身份说第一句话。"},
    ]

    return messages
