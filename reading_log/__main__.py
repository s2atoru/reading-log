#!/usr/bin/env python3
"""
Reading Log Application - Flask Web App

日本語入力に完全対応したWebベースの読書記録アプリケーション
"""

import sys
from pathlib import Path

# Flaskアプリをインポートして実行
from reading_log.app import app, open_browser
from reading_log.config import config
import threading

def main():
    print("=" * 50)
    print("📚 Reading Log Application")
    print("=" * 50)
    print("ブラウザが自動的に開きます...")
    print(f"URL: http://{config.server_host}:{config.server_port}")
    print("終了するには Ctrl+C を押してください")
    print("=" * 50)

    # 設定された遅延後にブラウザを開く
    if config.auto_open_browser:
        threading.Timer(config.browser_delay, open_browser).start()

    # Flaskアプリを起動
    app.run(host=config.server_host, port=config.server_port, debug=config.debug, use_reloader=False)

if __name__ == "__main__":
    main()
