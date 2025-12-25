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

    @mcp.tool()
    def add_solid_color_to_timeline(start_frame: int = 0, clip_name: str = "Solid Color") -> str:
        """
        Add a Solid Color clip from media pool to the current timeline
        
        Args:
            start_frame: Starting frame position for the clip (default: 0)
            clip_name: Name of the clip to search for in media pool (default: "Solid Color")
            start_position: Frame position in the clip to start from (default: None)
        
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
            
            # 2.クリップ配置時の設定(dict型に格納)
            timeline_fps = project.GetSetting('timelineFrameRate')  # タイムラインのフレームレート取得
            clip_fps = target_clip.GetClipProperty('FPS')             # クリップのフレームレート取得
            clip_len_second = 10.0              # 配置する際のクリップの長さ(秒)
            add_second = 10.0                   # タイムラインへ配置するタイミング（秒）
            clip_len_frame = clip_len_second * clip_fps # クリップの長さ(フレーム)
            info = {'mediaPoolItem':target_clip ,  # 追加するクリップ
                    'startFrame':0,        # 追加アイテムのトリミング開始フレーム（クリップFPSに依存）
                    'endFrame':clip_len_frame - 1,  # 追加アイテムのトリミング終了フレーム（クリップFPSに依存）
                    #'mediaType':1,        # 動画の映像と音声でトラック番号をずらしたい場合などに指定する
                    'trackIndex':1,        # トラック数より大きい場合、その分のトラックを追加する
                    'recordFrame':add_second * timeline_fps }    # タイムライン上の配置フレーム（タイムラインFPSに依存）

            # 3.クリップをタイムラインへ配置
            result = media_pool.AppendToTimeline([info])
            if result:
                timeline_name = timeline.GetName()
                print(f"Added '{clip_name}' to timeline '{timeline_name}' at frame {start_frame}")
                return f"Successfully added '{clip_name}' to timeline '{timeline_name}' at frame {start_frame}"
            else:
                return f"Failed to add '{clip_name}' to timeline"
                
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"
