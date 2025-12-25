# DaVinci Resolveスクリプトフォルダ内に配置するエントリーポイント
import sys
import os

# プロジェクトのルートディレクトリ（davinci_resolve_mcpフォルダ）を追加
# ここにsrcフォルダが入っている
project_root = r"C:\Users\giohe\Desktop\Dev\repository\davinci_resolve_mcp"
sys.path.insert(0, project_root)

# mcp-server-demoフォルダをパスに追加
mcp_server_path = os.path.join(project_root, "mcp-server-demo\src")
sys.path.insert(0, mcp_server_path)

import davinci_mcp_server

# 実行
if __name__ == "__main__":
    # DaVinci内部のグローバル変数 'app' からResolveインスタンスを取得
    # 'app' はDaVinci Consoleで実行時に自動的に利用可能
    resolve = app.GetResolve()
    
    # 取得したresolveインスタンスを外部スクリプトに渡す
    # api_test.main(resolve)
    
    # MCPサーバーをresolveインスタンスと一緒に起動
    print("Starting MCP server with DaVinci Resolve instance...")
    davinci_mcp_server.run_server(resolve=resolve)
