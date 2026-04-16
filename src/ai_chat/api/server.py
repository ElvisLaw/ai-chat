"""FastAPI 应用主入口。"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import HealthResponse
from .routes.chat import router as chat_router


def load_config() -> None:
    """加载配置（延迟导入避免循环依赖）。"""
    from ..config import load_config as _load
    _load()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理。"""
    # 启动时加载配置
    load_config()
    yield
    # 关闭时清理资源（如有需要）


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用。

    Returns:
        配置好的 FastAPI 实例。
    """
    app = FastAPI(
        title="AI Chat API",
        description="AI Chat 应用的 Web API 接口",
        version="0.1.0",
        lifespan=lifespan,
    )

    # 配置 CORS 中间件
    cors_origins = os.getenv("CORS_ORIGINS", "*")
    if cors_origins != "*":
        cors_origins = cors_origins.split(",")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(chat_router)

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health_check() -> HealthResponse:
        """健康检查端点。

        Returns:
            服务状态。
        """
        return HealthResponse(status="ok")

    return app


# 创建默认应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    uvicorn.run(
        "src.ai_chat.api.server:app",
        host=host,
        port=port,
        reload=True,
    )
