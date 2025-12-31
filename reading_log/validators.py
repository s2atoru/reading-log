"""
Validation utilities for reading log entries.
"""

from typing import Optional, Tuple
from reading_log.data_handler import MAX_PAGE, MIN_PAGE


def validate_page_range(
    page: Optional[str],
    page_end: Optional[str]
) -> Tuple[Optional[int], Optional[int], Optional[str]]:
    """
    ページ範囲をバリデーションします。
    
    Args:
        page: 開始ページ（文字列）
        page_end: 終了ページ（文字列）
    
    Returns:
        (page_int, page_end_int, error_message) のタプル
        エラーがない場合、error_messageはNone
    """
    page_int = None
    page_end_int = None
    
    if page:
        try:
            page_int = int(page)
            if page_int < MIN_PAGE or page_int > MAX_PAGE:
                return None, None, f'ページは{MIN_PAGE}から{MAX_PAGE}の範囲で入力してください。'
        except ValueError:
            return None, None, f'ページには数値を入力してください: {page}'
    
    if page_end:
        try:
            page_end_int = int(page_end)
            if page_end_int < MIN_PAGE or page_end_int > MAX_PAGE:
                return None, None, f'ページ終了は{MIN_PAGE}から{MAX_PAGE}の範囲で入力してください。'
            if page_int and page_end_int < page_int:
                return None, None, 'ページ終了は開始ページ以上である必要があります。'
        except ValueError:
            return None, None, f'ページ終了には数値を入力してください: {page_end}'
    
    return page_int, page_end_int, None
