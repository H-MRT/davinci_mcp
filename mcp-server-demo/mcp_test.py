"""
FastMCP quickstart example.

Run from the repository root:
    uv run examples/snippets/servers/fastmcp_quickstart.py
"""

import sys
import io

# DaVinci Resolveの特殊なstderr/stdoutをラップ
class FlushableWrapper:
    def __init__(self, original):
        self.original = original
    
    def write(self, text):
        if hasattr(self.original, 'write'):
            return self.original.write(text)
        return 0
    
    def flush(self):
        if hasattr(self.original, 'flush'):
            self.original.flush()
        # flush がなくても何もしない（エラーを回避）
    
    def isatty(self):
        """ターミナルかどうかを返す（DaVinci Resolve環境ではFalse）"""
        if hasattr(self.original, 'isatty'):
            return self.original.isatty()
        return False
    
    def fileno(self):
        """ファイル記述子を返す（利用不可の場合は例外）"""
        if hasattr(self.original, 'fileno'):
            return self.original.fileno()
        raise OSError("fileno not available")
    
    def readable(self):
        """読み取り可能かを返す"""
        if hasattr(self.original, 'readable'):
            return self.original.readable()
        return False
    
    def writable(self):
        """書き込み可能かを返す"""
        if hasattr(self.original, 'writable'):
            return self.original.writable()
        return True
    
    def __getattr__(self, name):
        return getattr(self.original, name)

# DaVinci Resolve環境対応: stderr/stdoutをラップ
if not hasattr(sys.stderr, 'flush') or not callable(getattr(sys.stderr, 'flush', None)):
    sys.stderr = FlushableWrapper(sys.stderr)
if not hasattr(sys.stdout, 'flush') or not callable(getattr(sys.stdout, 'flush', None)):
    sys.stdout = FlushableWrapper(sys.stdout)

from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)

# グローバル変数としてresolveインスタンスを保持
resolve_instance = None


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# DaVinci Resolveを使用するツールの例
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


# # Add a dynamic greeting resource
# @mcp.resource("greeting://{name}")
# def get_greeting(name: str) -> str:
#     """Get a personalized greeting"""
#     return f"Hello, {name}!"


# # Add a prompt
# @mcp.prompt()
# def greet_user(name: str, style: str = "friendly") -> str:
#     """Generate a greeting prompt"""
#     styles = {
#         "friendly": "Please write a warm, friendly greeting",
#         "formal": "Please write a formal, professional greeting",
#         "casual": "Please write a casual, relaxed greeting",
#     }

#     return f"{styles.get(style, styles['friendly'])} for someone named {name}."


def run_server(resolve=None, transport="streamable-http"):
    """MCPサーバーを起動する関数
    
    Args:
        resolve: DaVinci Resolveインスタンス(オプション)
        transport: 使用するトランスポート方式(デフォルト: streamable-http)
    """
    global resolve_instance
    resolve_instance = resolve
    print("mcp_test running...???")
    mcp.run(transport=transport)


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
