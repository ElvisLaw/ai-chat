"""CLI 主入口 - AI Chat 命令行界面。"""

import asyncio
from typing import Annotated

import typer
from rich.console import Console
from rich.markdown import Markdown

from ..conversation import ChatService, InMemoryConversationStore
from ..conversation.models import Role
from ..settings import get_settings
from .factory import create_llm_client_factory
from .rag import rag_app

console = Console()

# 创建主 Typer app
app = typer.Typer(help="AI Chat CLI - 与 AI 对话的终端界面")

# 注册 RAG 子命令
app.add_typer(rag_app, name="rag")


class CLIChatService:
    """CLI 专用的 ChatService 封装。"""

    def __init__(self):
        settings = get_settings()
        factory = create_llm_client_factory(settings)
        self._service = ChatService(
            store=InMemoryConversationStore(),
            llm_client_factory=factory,
        )
        self._conversation_id: str | None = None

    async def chat(
        self,
        message: str,
        provider: str = "openai",
        model: str | None = None,
        stream: bool = False,
    ) -> str:
        """发送消息并获取回复。"""
        if stream:
            return await self._chat_stream(message, provider, model)
        else:
            response, conv_id = await self._service.chat(
                message=message,
                provider=provider,
                model=model,
                conversation_id=self._conversation_id,
            )
            self._conversation_id = conv_id
            return response

    async def _chat_stream(
        self,
        message: str,
        provider: str,
        model: str | None,
    ) -> str:
        """流式聊天。"""
        generator, conv_id = self._service.stream(
            message=message,
            provider=provider,
            model=model,
            conversation_id=self._conversation_id,
        )
        self._conversation_id = conv_id

        full_response = ""
        for chunk in generator:
            print(chunk, end="", flush=True)
            full_response += chunk
        print()
        return full_response

    def get_history(self) -> list[tuple[Role, str]]:
        """获取当前会话历史。"""
        if not self._conversation_id:
            return []
        store = self._service._store
        conv = store.get(self._conversation_id)
        if not conv:
            return []
        return [(msg.role, msg.content) for msg in conv.messages]

    def clear_history(self) -> None:
        """清除会话历史。"""
        self._conversation_id = None


# 全局 CLI 服务实例
_chat_service: CLIChatService | None = None


def get_chat_service() -> CLIChatService:
    """获取或创建全局 CLI 服务实例。"""
    global _chat_service
    if _chat_service is None:
        _chat_service = CLIChatService()
    return _chat_service


@app.command()
def main(
    message: Annotated[str, typer.Argument(help="要发送的消息")],
    provider: Annotated[str, typer.Option(help="LLM 提供商 (openai/anthropic/agent)", case_sensitive=False)] = "openai",
    model: Annotated[str | None, typer.Option(help="模型名称")] = None,
    stream: Annotated[bool, typer.Option(help="启用流式输出")] = False,
) -> None:
    """发送单条消息给 AI。

    用法:
        ai-chat "你好"
        ai-chat "你好" --provider agent
    """
    settings = get_settings()

    # 验证 provider
    if provider not in ("openai", "anthropic", "agent"):
        console.print(f"[red]不支持的 provider: {provider}[/red]")
        raise typer.Exit(1)

    # 验证 API key
    if provider == "openai" and not settings.is_openai_configured():
        console.print("[red]OpenAI API key 未配置[/red]")
        console.print("请设置 OPENAI_API_KEY 环境变量")
        raise typer.Exit(1)
    if provider == "anthropic" and not settings.is_anthropic_configured():
        console.print("[red]Anthropic API key 未配置[/red]")
        console.print("请设置 ANTHROPIC_API_KEY 环境变量")
        raise typer.Exit(1)
    if provider == "agent" and not settings.is_openai_configured():
        console.print("[red]Agent 模式需要 OpenAI API key[/red]")
        console.print("请设置 OPENAI_API_KEY 环境变量")
        raise typer.Exit(1)

    _run_single_message(message, provider, model, stream)


@app.command()
def interactive(
    provider: Annotated[str, typer.Option(help="LLM 提供商 (openai/anthropic/agent)", case_sensitive=False)] = "openai",
    model: Annotated[str | None, typer.Option(help="模型名称")] = None,
    stream: Annotated[bool, typer.Option(help="启用流式输出")] = False,
) -> None:
    """进入交互模式。

    用法:
        ai-chat-interactive
        ai-chat-interactive --provider agent
    """
    settings = get_settings()

    # 验证 provider
    if provider not in ("openai", "anthropic", "agent"):
        console.print(f"[red]不支持的 provider: {provider}[/red]")
        raise typer.Exit(1)

    # 验证 API key
    if provider == "openai" and not settings.is_openai_configured():
        console.print("[red]OpenAI API key 未配置[/red]")
        console.print("请设置 OPENAI_API_KEY 环境变量")
        raise typer.Exit(1)
    if provider == "anthropic" and not settings.is_anthropic_configured():
        console.print("[red]Anthropic API key 未配置[/red]")
        console.print("请设置 ANTHROPIC_API_KEY 环境变量")
        raise typer.Exit(1)
    if provider == "agent" and not settings.is_openai_configured():
        console.print("[red]Agent 模式需要 OpenAI API key[/red]")
        console.print("请设置 OPENAI_API_KEY 环境变量")
        raise typer.Exit(1)

    _run_interactive(provider, model, stream)


def _run_single_message(
    message: str,
    provider: str,
    model: str | None,
    stream: bool,
) -> None:
    """执行单次消息问答。"""
    service = get_chat_service()

    console.print(f"[dim]Provider: {provider}[/dim]")
    if model:
        console.print(f"[dim]Model: {model}[/dim]")
    console.print()

    console.print("[bold cyan]AI:[/bold cyan] ", end="")

    try:
        if stream:
            asyncio.run(service.chat(message, provider, model, stream=True))
        else:
            response = asyncio.run(service.chat(message, provider, model, stream=False))
            console.print(response)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        raise typer.Exit(1)


def _run_interactive(
    provider: str,
    model: str | None,
    stream: bool,
) -> None:
    """运行交互模式。"""
    service = get_chat_service()

    console.print(Markdown("## AI Chat CLI"))
    console.print(f"Provider: `{provider}` | Model: `{model or 'default'}` | Stream: `{stream}`")
    console.print("输入 [bold]exit[/bold] 或 [bold]quit[/bold] 退出\n")

    while True:
        try:
            user_input = console.input("[bold green]>>>[/bold green] ")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]再见![/dim]")
            break

        # 检查退出命令
        if user_input.strip().lower() in ("exit", "quit", "q"):
            console.print("[dim]再见![/dim]")
            break

        # 检查 history 命令
        if user_input.strip().lower() == "history":
            _show_history(service)
            continue

        # 检查 clear 命令
        if user_input.strip().lower() == "clear":
            service.clear_history()
            console.print("[dim]历史已清除[/dim]")
            continue

        # 跳过空输入
        if not user_input.strip():
            continue

        # 发送消息
        console.print("[bold cyan]AI:[/bold cyan] ", end="")
        try:
            if stream:
                asyncio.run(service.chat(user_input, provider, model, stream=True))
            else:
                response = asyncio.run(service.chat(user_input, provider, model, stream=False))
                console.print(response)
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


def _show_history(service: CLIChatService) -> None:
    """显示对话历史。"""
    history = service.get_history()
    if not history:
        console.print("[dim]暂无历史记录[/dim]")
        return

    for role, content in history:
        role_str = "User" if role == Role.user else "Assistant"
        console.print(f"\n[bold]{role_str}:[/bold]")
        console.print(content)


@app.command(name="history")
def history_cmd() -> None:
    """显示当前会话的对话历史。"""
    service = get_chat_service()
    _show_history(service)


@app.command(name="clear")
def clear_cmd() -> None:
    """清除当前会话的对话历史。"""
    service = get_chat_service()
    service.clear_history()
    console.print("[dim]历史已清除[/dim]")


if __name__ == "__main__":
    app()
