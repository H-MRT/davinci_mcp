"""
DaVinci Resolve MCP サーバーのツール定義
"""

# グローバル変数としてresolveインスタンスを保持
resolve_instance = None


def set_resolve_instance(resolve):
    """
    DaVinci Resolveインスタンスを設定
    
    Args:
        resolve: DaVinci Resolveインスタンス
    """
    global resolve_instance
    resolve_instance = resolve


def register_tools(mcp):
    """
    MCPサーバーにツールを登録
    
    Args:
        mcp: FastMCPインスタンス
    """
    
    @mcp.tool()
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @mcp.tool()
    def get_project_name() -> str:
        """Get current DaVinci Resolve project name"""
        if resolve_instance is None:
            return "No Resolve instance available"
        
        project_manager = resolve_instance.GetProjectManager()
        current_project = project_manager.GetCurrentProject()
        if current_project:
            return current_project.GetName()
        return "No project opened"
