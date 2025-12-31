"""
Configuration management for reading-log application.
"""

import os
import shutil
import tomllib
from pathlib import Path
from typing import Any, Dict


# 設定ファイルのパス
CONFIG_DIR = Path.home() / ".config" / "reading-log"
CONFIG_FILE = CONFIG_DIR / "config.toml"
SAMPLE_CONFIG = Path(__file__).parent / "config.sample.toml"


class Config:
    """アプリケーション設定を管理するクラス"""
    
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._ensure_config()
        self._load_config()
    
    def _ensure_config(self) -> None:
        """設定ディレクトリとファイルの存在を確認し、必要に応じて作成"""
        # 設定ディレクトリを作成
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        # 設定ファイルが存在しない場合、サンプルをコピー
        if not CONFIG_FILE.exists():
            if SAMPLE_CONFIG.exists():
                shutil.copy(SAMPLE_CONFIG, CONFIG_FILE)
                print(f"設定ファイルを作成しました: {CONFIG_FILE}")
            else:
                raise FileNotFoundError(f"サンプル設定ファイルが見つかりません: {SAMPLE_CONFIG}")
    
    def _load_config(self) -> None:
        """設定ファイルを読み込む"""
        with open(CONFIG_FILE, 'rb') as f:
            self._config = tomllib.load(f)
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """設定値を取得"""
        return self._config.get(section, {}).get(key, default)
    
    @property
    def storage_path(self) -> Path:
        """データ保存先のパスを取得"""
        path_str = self.get('storage', 'path', 
                           '~/Library/Mobile Documents/com~apple~CloudDocs/reading-logs/log.json')
        return Path(os.path.expanduser(path_str))
    
    @property
    def min_page(self) -> int:
        """ページ番号の最小値を取得"""
        return self.get('validation', 'min_page', 0)
    
    @property
    def max_page(self) -> int:
        """ページ番号の最大値を取得"""
        return self.get('validation', 'max_page', 1000)
    
    @property
    def server_host(self) -> str:
        """サーバーホストを取得"""
        return self.get('server', 'host', '127.0.0.1')
    
    @property
    def server_port(self) -> int:
        """サーバーポートを取得"""
        return self.get('server', 'port', 5000)
    
    @property
    def debug(self) -> bool:
        """デバッグモードを取得"""
        return self.get('server', 'debug', True)
    
    @property
    def auto_open_browser(self) -> bool:
        """ブラウザ自動起動の設定を取得"""
        return self.get('ui', 'auto_open_browser', True)
    
    @property
    def browser_delay(self) -> int:
        """ブラウザ起動遅延を取得"""
        return self.get('ui', 'browser_delay', 1)


# グローバル設定インスタンス
config = Config()
