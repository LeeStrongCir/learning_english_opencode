from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类，从环境变量或.env文件读取配置"""

    # 大模型API配置
    llm_api_key: str = ""
    llm_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    llm_model: str = "qwen-turbo"

    # 语音识别配置
    asr_api_key: str = ""
    asr_api_secret: str = ""

    # 语音合成配置
    tts_api_key: str = ""
    tts_api_secret: str = ""

    # 应用配置
    app_secret: str = "default_secret_change_me"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 全局配置实例
settings = Settings()
