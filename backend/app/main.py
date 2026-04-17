from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用实例
app = FastAPI(
    title="小学英语情景对话学习助手",
    description="基于AI的小学英语情景对话学习系统API",
    version="1.0.0",
)

# 添加CORS中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    logger.info("=" * 50)
    logger.info("小学英语情景对话学习助手 API 启动中...")
    logger.info(f"LLM模型: {settings.llm_model}")
    logger.info(f"LLM Base URL: {settings.llm_base_url}")
    logger.info(f"ASR服务: {'已配置' if settings.asr_api_key else '未配置(使用模拟模式)'}")
    logger.info(f"TTS服务: {'已配置' if settings.tts_api_key else '未配置(使用模拟模式)'}")
    logger.info("=" * 50)


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "小学英语情景对话学习助手",
        "version": "1.0.0",
    }


# 注册路由
from app.api.routes import dialogue, report

app.include_router(dialogue.router, prefix="/api/dialogue", tags=["对话"])
app.include_router(report.router, prefix="/api/report", tags=["学习报告"])
