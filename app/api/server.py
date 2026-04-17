"""FastAPI 应用主入口。"""

from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import HealthResponse
from .routes.chat import router as chat_router
from .routes.rag import router as rag_router
from ..clients import create_llm_client, ConfigurationError
from ..conversation import ChatService, InMemoryConversationStore
from ..rag import RAGService
from ..settings import get_settings


def _get_llm_client(provider: str) -> object:
    """获取 LLM 客户端实例。

    Args:
        provider: LLM 提供商名称。

    Returns:
        LLM 客户端实例。

    Raises:
        HTTPException: 如果配置缺失或不支持的提供商。
    """
    settings = get_settings()

    try:
        if provider == "openai":
            api_key = settings.openai_api_key
            base_url = settings.openai_base_url
            if not api_key:
                raise RuntimeError("OpenAI API key not configured")
            return create_llm_client("openai", api_key, base_url=base_url)
        elif provider == "anthropic":
            api_key = settings.anthropic_api_key
            if not api_key:
                raise RuntimeError("Anthropic API key not configured")
            return create_llm_client("anthropic", api_key)
        elif provider == "agent":
            # Agent 使用 OpenAI API key（如果配置了）
            api_key = settings.openai_api_key
            base_url = settings.openai_base_url
            model = settings.get_default_model("openai")
            return create_llm_client("agent", api_key, model=model, base_url=base_url)
        else:
            raise RuntimeError(f"Unsupported provider: {provider}")
    except ConfigurationError as e:
        raise RuntimeError(str(e)) from e


def _make_llm_client_factory() -> "Callable[[str], object]":
    """创建 LLM 客户端工厂函数。"""
    return _get_llm_client


# 全局应用实例（lifespan 管理其 state）
_app_instance: FastAPI | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理。

    在应用启动时创建 store 和 service，存入 app.state。
    """
    store = InMemoryConversationStore()
    service = ChatService(
        store=store,
        llm_client_factory=_make_llm_client_factory(),
    )
    rag_service = RAGService()
    app.state.store = store
    app.state.chat_service = service
    app.state.rag_service = rag_service
    yield
    # 目前 InMemoryConversationStore 不需要清理
    # 后续接入 Redis/DB 时在此处清理连接


def create_app() -> FastAPI:
    """创建并配置 FastAPI 应用。

    Returns:
        配置好的 FastAPI 实例。
    """
    global _app_instance

    settings = get_settings()

    app = FastAPI(
        title="AI Chat API",
        description="AI Chat 应用的 Web API 接口",
        version="0.1.0",
        lifespan=lifespan,
    )

    # 配置 CORS 中间件
    cors_origins = settings.cors_origins
    if isinstance(cors_origins, str) and cors_origins != "*":
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
    app.include_router(rag_router)

    @app.get("/health", response_model=HealthResponse, tags=["health"])
    async def health_check() -> HealthResponse:
        """健康检查端点。

        Returns:
            服务状态。
        """
        return HealthResponse(status="ok")

    _app_instance = app
    return app


# 创建默认应用实例
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )
