#!/usr/bin/env python3
"""
Reading Log Application - Flask Web App

日本語入力に完全対応したWebベースの読書記録アプリケーション
"""

import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Flaskアプリをインポートして実行
from app import app, open_browser
import threading

def main():
    print("=" * 50)
    print("📚 Reading Log Application")
    print("=" * 50)
    print("ブラウザが自動的に開きます...")
    print("URL: http://127.0.0.1:5000")
    print("終了するには Ctrl+C を押してください")
    print("=" * 50)
    
    # 1秒後にブラウザを開く
    threading.Timer(1, open_browser).start()
    
    # Flaskアプリを起動
    app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
