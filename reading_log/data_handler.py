import json
import uuid
import logging
from dataclasses import dataclass, asdict, field
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional

# ログ設定
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# デフォルトのログディレクトリ（iCloud Drive）
LOG_DIR = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs" / "reading-logs"
LOG_FILE = LOG_DIR / "log.json"

@dataclass
class ReadingLogEntry:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    author: str = ""  # カンマ区切りで複数著者を保存
    date: str = field(default_factory=lambda: date.today().isoformat())
    page: Optional[int] = None
    page_end: Optional[int] = None  # ページ終了（範囲指定用）
    chapter: Optional[str] = None
    chapter_end: Optional[str] = None  # 章終了（範囲指定用）
    section: Optional[str] = None
    section_end: Optional[str] = None  # 節終了（範囲指定用）
    comment: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def validate(self) -> None:
        """
        エントリーを検証します。
        タイトルが空、または位置情報（ページ/章/節）が全て未指定の場合、ValueErrorを発生させます。
        """
        if not self.title.strip():
            raise ValueError("タイトルは必須です。")
        
        if not any([self.page, self.chapter, self.section]):
             raise ValueError("ページ、章、節のいずれか1つは必須です。")

class DataHandler:
    def __init__(self, storage_path: Path = LOG_FILE):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """ストレージディレクトリとJSONファイルの存在を確認します。"""
        if not self.storage_path.parent.exists():
            self.storage_path.parent.mkdir(parents=True)
        
        if not self.storage_path.exists():
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_entries(self) -> List[ReadingLogEntry]:
        """JSONファイルから全エントリーを読み込みます。"""
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [ReadingLogEntry(**item) for item in data]
        except json.JSONDecodeError as e:
            logger.error(f"JSONデコードエラー: {e}. 空のリストを返します。")
            return []
        except FileNotFoundError:
            logger.warning(f"ファイルが見つかりません: {self.storage_path}")
            return []

    def save_entry(self, entry: ReadingLogEntry) -> None:
        """エントリーを検証してJSONファイルに保存します。"""
        entry.validate()
        entries = self.load_entries()
        entries.insert(0, entry)  # 最新を先頭に追加
        
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)

    def search_entries(self, query: str) -> List[ReadingLogEntry]:
        """タイトルまたは著者名でエントリーを検索します。"""
        entries = self.load_entries()
        if not query:
            return entries
        
        query = query.lower()
        return [
            e for e in entries 
            if query in e.title.lower() or query in e.author.lower()
        ]
