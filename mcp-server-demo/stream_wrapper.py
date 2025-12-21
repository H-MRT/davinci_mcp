"""
DaVinci Resolveの特殊なstderr/stdoutをラップするためのユーティリティ
"""


class FlushableWrapper:
    """
    DaVinci Resolveの特殊なstderr/stdoutをラップするクラス
    通常のPythonストリームで利用可能なメソッドをすべて提供します
    """
    
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


def setup_stream_wrappers():
    """
    sys.stderr/stdoutをFlushableWrapperでラップする
    DaVinci Resolve環境でflushメソッドが存在しない場合に対応
    """
    import sys
    
    if not hasattr(sys.stderr, 'flush') or not callable(getattr(sys.stderr, 'flush', None)):
        sys.stderr = FlushableWrapper(sys.stderr)
    if not hasattr(sys.stdout, 'flush') or not callable(getattr(sys.stdout, 'flush', None)):
        sys.stdout = FlushableWrapper(sys.stdout)
