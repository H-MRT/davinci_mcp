"""
DaVinci Resolve MCP Server
MCPサーバーのメインエントリーポイント
"""

# DaVinci Resolve環境対応: stderr/stdoutをラップ
from stream_wrapper import setup_stream_wrappers
setup_stream_wrappers()

from fastmcp import FastMCP
from tools import register_tools, set_resolve_instance

# Create an MCP server
mcp = FastMCP("Demo", json_response=True)

# ツールを登録
register_tools(mcp)


def run_server(resolve=None, transport="streamable-http"):
    """MCPサーバーを起動する関数
    
    Args:
        resolve: DaVinci Resolveインスタンス(オプション)
        transport: 使用するトランスポート方式(デフォルト: streamable-http)
    """
    set_resolve_instance(resolve)
    mcp.run(transport=transport)


# Run with streamable HTTP transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
