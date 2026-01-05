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
    def get_project_name() -> str:
        """Get current DaVinci Resolve project name"""
        if resolve_instance is None:
            return "No Resolve instance available"
        
        project_manager = resolve_instance.GetProjectManager()
        current_project = project_manager.GetCurrentProject()
        if current_project:
            return current_project.GetName()
        return "No project opened"

    @mcp.tool()
    def add_solid_color_to_timeline(start_frame: int = 0, clip_duration: int = 50, clip_name: str = "Solid Color", ) -> str:
        """
        Add a Solid Color clip from media pool to the current timeline
        
        Args:
            start_frame: Starting frame position for the clip (default: 0)
            clip_duration: Duration of the clip in frames (default: 50)
            clip_name: Name of the clip to search for in media pool (default: "Solid Color")
        
        Returns:
            Success or error message
        """
        if resolve_instance is None:
            return "No Resolve instance available"
        
        try:
            # Get current project
            project = resolve_instance.GetProjectManager().GetCurrentProject()
            if not project:
                return "No project is currently open"
            
            # Get current timeline
            timeline = project.GetCurrentTimeline()
            if not timeline:
                return "No timeline is currently open. Please open or create a timeline first."
            
            # Get media pool and search for the clip
            media_pool = project.GetMediaPool()
            if not media_pool:
                return "Failed to get media pool"
            
            current_folder = media_pool.GetCurrentFolder()
            if not current_folder:
                return "Failed to get current folder in media pool"
            
            clip_list = current_folder.GetClipList()
            if not clip_list:
                return "No clips found in current media pool folder"
            
            # Search for the target clip
            target_clip = None
            for clip in clip_list:
                if clip.GetClipProperty('Clip Name') == clip_name:
                    target_clip = clip
                    break
            
            if not target_clip:
                return f"Clip '{clip_name}' not found in current media pool folder"
            
            # recordFrameの不具合回避: ダミークリップ方式を使用
            # ステップ1: recordFrame位置までダミークリップを追加
            if start_frame > 0:
                dummy_clip_config = {
                    "mediaPoolItem": target_clip,
                    "startFrame": 0,
                    "endFrame": start_frame - 1,  # start_frameまでの長さ
                    'trackIndex': 1,
                }
                
                dummy_result = media_pool.AppendToTimeline([dummy_clip_config])
                if not dummy_result:
                    return "Failed to add dummy clip"
            
            # ステップ2: 本来追加したいクリップを追加(recordFrameを指定しない)
            clip_config = {
                "mediaPoolItem": target_clip,
                "startFrame": 0,
                "endFrame": clip_duration - 1,
                'trackIndex': 1
                # recordFrameを指定しない - 自動的にダミーの次の位置に追加される
            }
            
            result = media_pool.AppendToTimeline([clip_config])
            if not result:
                return "Failed to add clip to timeline"
            
            # ステップ3: ダミークリップを削除（start_frame > 0の場合のみ）
            if start_frame > 0:
                track_items = timeline.GetItemListInTrack("video", 1)
                if track_items and len(track_items) > 0:
                    first_item = track_items[0]  # 最初のアイテム(ダミークリップ)
                    delete_result = timeline.DeleteClips([first_item])
                    if not delete_result:
                        return "Failed to delete dummy clip (but main clip was added)"
            
            timeline_name = timeline.GetName()
            return f"Successfully added '{clip_name}' to timeline '{timeline_name}' at frame {start_frame} (duration: {clip_duration} frames)"
                
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"
