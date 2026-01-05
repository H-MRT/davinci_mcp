#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DaVinci Resolve API テストスクリプト
DaVinci Resolveが起動している状態で実行してください
"""

import sys
import os


def get_resolve():
    """DaVinci Resolveインスタンスを取得"""
    try:
        # Windows環境でのDaVinci Resolve APIモジュールのパス設定
        resolve_script_api = os.path.join(
            os.environ.get('PROGRAMDATA', 'C:\\ProgramData'),
            'Blackmagic Design',
            'DaVinci Resolve',
            'Support',
            'Developer',
            'Scripting',
            'Modules'
        )
        
        print(f"🔍 APIモジュールパス: {resolve_script_api}")
        print(f"🔍 パスの存在確認: {os.path.exists(resolve_script_api)}")
        
        if os.path.exists(resolve_script_api):
            sys.path.append(resolve_script_api)
            print("✅ sys.pathにAPIモジュールパスを追加")
        else:
            print("⚠️ APIモジュールパスが見つかりません")
        
        print("🔍 DaVinciResolveScriptをインポート中...")
        import DaVinciResolveScript as dvr_script
        print("✅ DaVinciResolveScriptのインポート成功")
        
        print("🔍 scriptapp('Resolve')を呼び出し中...")
        resolve = dvr_script.scriptapp("Resolve")
        
        if resolve is None:
            print("❌ scriptapp('Resolve')がNoneを返しました")
            print("   → DaVinci Resolveが起動しているか確認してください")
            print("   → 環境設定 > システム > 一般 で「外部スクリプトの使用」が有効か確認してください")
        else:
            print("✅ Resolveインスタンスの取得成功")
        
        return resolve
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("   → DaVinciResolveScript.pyが正しい場所にあるか確認してください")
        return None
    except Exception as e:
        print(f"❌ 予期しないエラー: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_basic_connection():
    """基本的な接続テスト"""
    print("=" * 60)
    print("DaVinci Resolve API 基本接続テスト")
    print("=" * 60)
    
    resolve = get_resolve()
    if not resolve:
        print("❌ DaVinci Resolveに接続できません")
        print("\n確認事項:")
        print("1. DaVinci Resolveが起動しているか")
        print("2. スクリプトAPIがインストールされているか")
        return False
    
    print("✅ DaVinci Resolveに接続成功")
    return resolve


def test_project_manager(resolve):
    """プロジェクトマネージャーのテスト"""
    print("\n" + "=" * 60)
    print("プロジェクトマネージャーテスト")
    print("=" * 60)
    
    try:
        project_manager = resolve.GetProjectManager()
        if not project_manager:
            print("❌ プロジェクトマネージャーの取得に失敗")
            return None
        
        print("✅ プロジェクトマネージャー取得成功")
        return project_manager
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None


def test_current_project(project_manager):
    """現在のプロジェクト情報を取得"""
    print("\n" + "=" * 60)
    print("現在のプロジェクト情報")
    print("=" * 60)
    
    try:
        current_project = project_manager.GetCurrentProject()
        if not current_project:
            print("❌ 現在プロジェクトが開かれていません")
            return None
        
        project_name = current_project.GetName()
        print(f"✅ プロジェクト名: {project_name}")
        
        # タイムライン数を取得
        timeline_count = current_project.GetTimelineCount()
        print(f"📊 タイムライン数: {timeline_count}")
        
        return current_project
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None


def test_current_timeline(project):
    """現在のタイムライン情報を取得"""
    print("\n" + "=" * 60)
    print("現在のタイムライン情報")
    print("=" * 60)
    
    try:
        current_timeline = project.GetCurrentTimeline()
        if not current_timeline:
            print("⚠️ 現在タイムラインが開かれていません")
            return None
        
        timeline_name = current_timeline.GetName()
        frame_rate = current_timeline.GetSetting("timelineFrameRate")
        width = current_timeline.GetSetting("timelineResolutionWidth")
        height = current_timeline.GetSetting("timelineResolutionHeight")
        
        print(f"✅ タイムライン名: {timeline_name}")
        print(f"🎬 フレームレート: {frame_rate} fps")
        print(f"📐 解像度: {width}x{height}")
        
        # トラック数を取得
        video_tracks = current_timeline.GetTrackCount("video")
        audio_tracks = current_timeline.GetTrackCount("audio")
        print(f"🎥 ビデオトラック数: {video_tracks}")
        print(f"🔊 オーディオトラック数: {audio_tracks}")
        
        return current_timeline
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None


def test_media_pool(project):
    """メディアプール情報を取得"""
    print("\n" + "=" * 60)
    print("メディアプール情報")
    print("=" * 60)
    
    try:
        media_pool = project.GetMediaPool()
        if not media_pool:
            print("❌ メディアプールの取得に失敗")
            return None
        
        print("✅ メディアプール取得成功")
        
        root_folder = media_pool.GetRootFolder()
        if root_folder:
            clip_count = len(root_folder.GetClipList())
            print(f"📁 ルートフォルダーのクリップ数: {clip_count}")
        
        return media_pool
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None


def add_test_clips_to_timeline(resolve,project, media_pool, timeline):
    """タイムラインにテストクリップを追加"""
    print("\n" + "=" * 60)
    print("タイムラインにテストクリップを追加")
    print("=" * 60)
    
    try:
        if not timeline:
            # タイムラインがない場合は作成
            print("📝 新しいタイムラインを作成中...")
            timeline = media_pool.CreateEmptyTimeline("Test Timeline")
            if not timeline:
                print("❌ タイムラインの作成に失敗")
                return None
            print("✅ 新しいタイムライン作成成功")
            project.SetCurrentTimeline(timeline)
        
        # カラージェネレーターを追加
        print("🎨 カラージェネレーターを追加中...")
        
        project = resolve.GetProjectManager().GetCurrentProject()
        pool = project.GetMediaPool()
        cliplist = pool.GetCurrentFolder().GetClipList()
        add_clip = None
        for clip in cliplist :  # 目的のクリップを検索
            if clip.GetClipProperty('Clip Name') == 'TestClip' :
                add_clip = clip
                break
            
        add_position = 100  # 追加位置フレーム
        
        # recordFrameの不具合回避: ダミークリップ方式を使用
        # ステップ1: recordFrame位置までダミークリップを追加
        print("🔧 ダミークリップを追加中(recordFrame位置まで)...")
        dummy_clip_config = {
            "mediaPoolItem": add_clip,
            "startFrame": 0,
            "endFrame": add_position - 1,  # recordFrame(100)までの長さ = 100フレーム
            'trackIndex': 1,
        }
        
        dummy_result = media_pool.AppendToTimeline([dummy_clip_config])
        if not dummy_result:
            print("❌ ダミークリップの追加に失敗")
            return None
        print("✅ ダミークリップの追加成功")
        
        # ステップ2: 本来追加したいクリップを追加(recordFrameを指定しない)
        print("🎨 本来のクリップを追加中...")
        generator_red = {
            "mediaPoolItem": add_clip,
            "startFrame": 0,
            "endFrame": add_position + 49,  # 50フレーム分の長さ
            'trackIndex': 1
            # recordFrameを指定しない - 自動的にダミーの次の位置に追加される
        }
        
        result = media_pool.AppendToTimeline([generator_red])
        if not result:
            print("❌ 本来のクリップの追加に失敗")
            return None
        print("✅ 本来のクリップの追加成功")
        
        # ステップ3: ダミークリップを削除
        print("🗑️ ダミークリップを削除中...")
        track_items = timeline.GetItemListInTrack("video", 1)
        if track_items and len(track_items) > 0:
            first_item = track_items[0]  # 最初のアイテム(ダミークリップ)
            delete_result = timeline.DeleteClips([first_item])
            if delete_result:
                print("✅ ダミークリップの削除成功")
            else:
                print("⚠️ ダミークリップの削除に失敗")
        else:
            print("⚠️ ダミークリップが見つかりませんでした")
        
        # タイムライン情報を再表示
        print(f"\n📊 タイムライン更新後の情報:")
        print(f"   タイムライン名: {timeline.GetName()}")
        print(f"   ビデオトラック数: {timeline.GetTrackCount('video')}")
        print(f"   オーディオトラック数: {timeline.GetTrackCount('audio')}")
        
        return timeline
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def main(resolve=None):
    """メインテスト関数
    
    Args:
        resolve: DaVinci Resolveインスタンス（省略時は自動取得を試みる）
    """
    print("\n🎬 DaVinci Resolve API テスト開始\n")
    
    # resolveインスタンスが渡されていない場合は取得を試みる
    if resolve is None:
        print("🔍 Resolveインスタンスが渡されていません。自動取得を試みます...")
        resolve = app.GetResolve()# type: ignore
        if not resolve:
            return
    else:
        print("✅ Resolveインスタンスを受け取りました（DaVinci内部実行）")
    
    # 2. プロジェクトマネージャーテスト
    project_manager = test_project_manager(resolve)
    if not project_manager:
        return
    
    # 3. 現在のプロジェクト情報
    project = test_current_project(project_manager)
    if not project:
        print("\n⚠️ プロジェクトを開いてから再度実行してください")
        return
    
    # 4. タイムライン情報
    timeline = test_current_timeline(project)
    
    # 5. メディアプール情報
    media_pool = test_media_pool(project)
    
    # 6. タイムラインにテストクリップを追加
    if media_pool:
        timeline = add_test_clips_to_timeline(resolve,project, media_pool, timeline)
        if timeline:
            print("✅ タイムラインへのクリップ追加完了")
    
    print("\n" + "=" * 60)
    print("✅ テスト完了")
    print("=" * 60)


if __name__ == "__main__":
    main()
