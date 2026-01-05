"""
DaVinci Resolve MCP サーバーの基底クラスと共通機能
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


def get_resolve_instance():
    """
    DaVinci Resolveインスタンスを取得
    
    Returns:
        DaVinci Resolveインスタンス（存在しない場合はNone）
    """
    return resolve_instance
