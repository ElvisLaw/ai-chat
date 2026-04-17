"""CLI 模块测试。"""

import pytest
from typer.testing import CliRunner

from app.cli.main import app

runner = CliRunner()


def test_cli_help():
    """测试 CLI --help 命令。"""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "AI Chat CLI" in result.stdout
    assert "main" in result.stdout
    assert "interactive" in result.stdout


def test_cli_history_subcommand():
    """测试 history 子命令。"""
    result = runner.invoke(app, ["history"])
    assert result.exit_code == 0


def test_cli_clear_subcommand():
    """测试 clear 子命令。"""
    result = runner.invoke(app, ["clear"])
    assert result.exit_code == 0


def test_cli_main_command():
    """测试 main 子命令（发送消息）。"""
    result = runner.invoke(app, ["main", "hello"])
    # 如果 API key 未配置会返回错误（exit code 1），否则尝试调用 AI
    # 我们只验证命令不会因参数错误而崩溃（exit code 2）
    assert result.exit_code in (0, 1)
