"""
DaVinci Resolve MCP サーバーのツール統合モジュール

このモジュールは、すべてのツールカテゴリを統合し、
MCPサーバーへの登録を一元管理します。
"""

from .base import set_resolve_instance, get_resolve_instance
from .project_tools import register_project_tools
from .timeline_tools import register_timeline_tools


def register_tools(mcp):
    """
    すべてのツールをMCPサーバーに登録
    
    Args:
        mcp: FastMCPインスタンス
    """
    # 各カテゴリのツールを登録
    register_project_tools(mcp)
    register_timeline_tools(mcp)


# 外部から使用できるようにエクスポート
__all__ = [
    'register_tools',
    'set_resolve_instance',
    'get_resolve_instance',
]
