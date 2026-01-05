"""
DaVinci Resolve プロジェクト関連のツール
"""

from .base import get_resolve_instance


def register_project_tools(mcp):
    """
    プロジェクト関連ツールをMCPサーバーに登録
    
    Args:
        mcp: FastMCPインスタンス
    """

    @mcp.tool()
    def get_project_name() -> str:
        """Get current DaVinci Resolve project name"""
        resolve = get_resolve_instance()
        if resolve is None:
            return "No Resolve instance available"
        
        project_manager = resolve.GetProjectManager()
        current_project = project_manager.GetCurrentProject()
        if current_project:
            return current_project.GetName()
        return "No project opened"
