import httpx
import logging
from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """大语言模型服务，使用OpenAI兼容接口"""

    def __init__(self):
        # 初始化OpenAI客户端，兼容通义千问等国内大模型
        self.client = AsyncOpenAI(
            api_key=settings.llm_api_key,
            base_url=settings.llm_base_url,
        )
        self.model = settings.llm_model

    async def chat_completion(self, messages, model=None, temperature=0.7, stream=False):
        """
        调用大模型生成回复

        参数:
            messages: 消息列表 [{"role": "system"/"user"/"assistant", "content": "..."}]
            model: 模型名称，默认使用配置中的模型
            temperature: 温度参数，控制随机性 (0.0-1.0)
            stream: 是否使用流式输出

        返回:
            非流式: 生成的文本内容
            流式: 异步生成器，逐块返回文本
        """
        model_name = model or self.model

        try:
            if stream:
                return self._stream_completion(messages, model_name, temperature)
            else:
                response = await self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temperature,
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"LLM调用失败: {str(e)}")
            raise

    async def _stream_completion(self, messages, model, temperature):
        """流式输出实现"""
        stream = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


# 全局LLM服务实例
llm_service = LLMService()
