
resolve = app.GetResolve() # type: ignore

# プロジェクトとタイムラインを取得
project = resolve.GetProjectManager().GetCurrentProject()
timeline = project.GetCurrentTimeline()

if timeline:
    # タイムライン上のトラック数を取得
    track_count = timeline.GetTrackCount("video")
    print(f"ビデオトラック数: {track_count}")
    
    # 各トラックのアイテムを取得
    for track_index in range(1, track_count + 1):
        items = timeline.GetItemListInTrack("video", track_index)
        print(f"\n=== トラック {track_index} ===")
        print(f"アイテム数: {len(items)}")
        
        for i, item in enumerate(items):
            print(f"\n--- アイテム {i+1} ---")
            
            # TimelineItem のすべてのメソッドを表示
            print("利用可能なメソッド:")
            methods = [m for m in dir(item) if not m.startswith('_')]
            for method in methods:
                print(f"  - {method}")
            
            # プロパティを取得して表示
            print("\nプロパティ:")
            try:
                # GetProperty() で取得できるプロパティ
                props = item.GetProperty()
                if isinstance(props, dict):
                    for key, value in props.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"  プロパティ: {props}")
            except Exception as e:
                print(f"  GetProperty() エラー: {e}")
            
            # 個別のプロパティ取得メソッドを試す
            print("\n個別プロパティ:")
            try:
                print(f"  Name: {item.GetName()}")
                print(f"  Duration: {item.GetDuration()}")
                print(f"  Start: {item.GetStart()}")
                print(f"  End: {item.GetEnd()}")
                print(f"  LeftOffset: {item.GetLeftOffset()}")
                print(f"  RightOffset: {item.GetRightOffset()}")
            except Exception as e:
                print(f"  個別プロパティ取得エラー: {e}")
            
            # MediaPoolItem を取得
            print("\nMediaPoolItem 情報:")
            try:
                media_pool_item = item.GetMediaPoolItem()
                if media_pool_item:
                    clip_props = media_pool_item.GetClipProperty()
                    if isinstance(clip_props, dict):
                        for key, value in clip_props.items():
                            print(f"  {key}: {value}")
                    else:
                        print(f"  クリッププロパティ: {clip_props}")
            except Exception as e:
                print(f"  MediaPoolItem エラー: {e}")

else:
    print("現在開いているタイムラインがありません")
