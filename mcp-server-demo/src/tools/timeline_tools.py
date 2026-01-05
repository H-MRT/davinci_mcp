"""
DaVinci Resolve タイムライン関連のツール
"""

from .base import get_resolve_instance


def register_timeline_tools(mcp):
    """
    タイムライン関連ツールをMCPサーバーに登録
    
    Args:
        mcp: FastMCPインスタンス
    """

    @mcp.tool()
    def add_solid_color_to_timeline(start_frame: int = 0, duration_in_frames: int = 50, clip_name: str = "Solid Color") -> str:
        """
        Add a Solid Color clip from media pool to the current timeline
        
        This tool adds a solid color clip to the timeline at a specified frame position
        with a specified length in frames.
        
        Args:
            start_frame: The frame number where the clip should start on the timeline.
                        Frame 0 is the beginning of the timeline. (default: 0)
            duration_in_frames: The length of the clip in frames. For example, if set to 50,
                               the clip will be 50 frames long. At 24fps, this equals about 2 seconds.
                               Must be a positive integer. (default: 50)
            clip_name: The exact name of the clip to search for in the current media pool folder.
                      The clip must exist in the media pool before adding. (default: "Solid Color")
        
        Returns:
            Success or error message
        """
        resolve = get_resolve_instance()
        if resolve is None:
            return "No Resolve instance available"
        
        try:
            # Get current project
            project = resolve.GetProjectManager().GetCurrentProject()
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
                "endFrame": duration_in_frames - 1,
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
            return f"Successfully added '{clip_name}' to timeline '{timeline_name}' at frame {start_frame} (duration: {duration_in_frames} frames)"
                
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"

    @mcp.tool()
    def set_timeline_item_position(
        track_type: str = "video",
        track_index: int = 1,
        item_index: int = 1,
        pan: float | None = None,
        tilt: float | None = None,
        anchor_point_x: float | None = None,
        anchor_point_y: float | None = None
    ) -> str:
        """
        Set the position properties of a timeline item
        
        This tool changes the position of a timeline item by setting its Pan, Tilt, 
        AnchorPointX, and/or AnchorPointY properties using the TimelineItem SetProperty API.
        
        Args:
            track_type: Type of track ("video", "audio", or "subtitle"). Default: "video"
            track_index: Track number (1-based index). Default: 1
            item_index: Item position in the track (1-based index). Default: 1
            pan: Horizontal position offset. Range: -4.0*width to 4.0*width. None to skip.
            tilt: Vertical position offset. Range: -4.0*height to 4.0*height. None to skip.
            anchor_point_x: Anchor point X coordinate. Range: -4.0*width to 4.0*width. None to skip.
            anchor_point_y: Anchor point Y coordinate. Range: -4.0*height to 4.0*height. None to skip.
        
        Returns:
            Success or error message
        """
        resolve = get_resolve_instance()
        if resolve is None:
            return "No Resolve instance available"
        
        try:
            # Get current project
            project = resolve.GetProjectManager().GetCurrentProject()
            if not project:
                return "No project is currently open"
            
            # Get current timeline
            timeline = project.GetCurrentTimeline()
            if not timeline:
                return "No timeline is currently open. Please open or create a timeline first."
            
            # Validate track_type
            valid_track_types = ["video", "audio", "subtitle"]
            if track_type not in valid_track_types:
                return f"Invalid track_type '{track_type}'. Must be one of: {', '.join(valid_track_types)}"
            
            # Get track count and validate track_index
            track_count = timeline.GetTrackCount(track_type)
            if track_count == 0:
                return f"No {track_type} tracks found in timeline"
            
            if track_index < 1 or track_index > track_count:
                return f"Invalid track_index {track_index}. Must be between 1 and {track_count}"
            
            # Get items in the track
            track_items = timeline.GetItemListInTrack(track_type, track_index)
            if not track_items or len(track_items) == 0:
                return f"No items found in {track_type} track {track_index}"
            
            # Validate item_index
            if item_index < 1 or item_index > len(track_items):
                return f"Invalid item_index {item_index}. Must be between 1 and {len(track_items)}"
            
            # Get the target item (convert to 0-based index)
            target_item = track_items[item_index - 1]
            item_name = target_item.GetName()
            
            # Check if at least one property is provided
            if pan is None and tilt is None and anchor_point_x is None and anchor_point_y is None:
                return "At least one position property (pan, tilt, anchor_point_x, or anchor_point_y) must be provided"
            
            # Get timeline resolution for range validation
            # Note: We'll use a simplified validation approach since exact width/height 
            # may not be easily accessible. The API will clip values beyond range.
            
            # Apply properties
            updated_properties = []
            failed_properties = []
            
            if pan is not None:
                result = target_item.SetProperty("Pan", pan)
                if result:
                    updated_properties.append(f"Pan={pan}")
                else:
                    failed_properties.append("Pan")
            
            if tilt is not None:
                result = target_item.SetProperty("Tilt", tilt)
                if result:
                    updated_properties.append(f"Tilt={tilt}")
                else:
                    failed_properties.append("Tilt")
            
            if anchor_point_x is not None:
                result = target_item.SetProperty("AnchorPointX", anchor_point_x)
                if result:
                    updated_properties.append(f"AnchorPointX={anchor_point_x}")
                else:
                    failed_properties.append("AnchorPointX")
            
            if anchor_point_y is not None:
                result = target_item.SetProperty("AnchorPointY", anchor_point_y)
                if result:
                    updated_properties.append(f"AnchorPointY={anchor_point_y}")
                else:
                    failed_properties.append("AnchorPointY")
            
            # Build result message
            timeline_name = timeline.GetName()
            result_parts = []
            
            if updated_properties:
                result_parts.append(f"Successfully updated position for item '{item_name}' in timeline '{timeline_name}'")
                result_parts.append(f"Track: {track_type} {track_index}, Item: {item_index}")
                result_parts.append(f"Updated properties: {', '.join(updated_properties)}")
            
            if failed_properties:
                result_parts.append(f"Failed to update: {', '.join(failed_properties)}")
            
            if not updated_properties:
                return f"Failed to update any properties for item '{item_name}'"
            
            return "\n".join(result_parts)
                
        except Exception as e:
            return f"Error: {type(e).__name__}: {str(e)}"
