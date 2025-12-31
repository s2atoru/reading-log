# Reading Log App

読書記録を管理するためのWebアプリケーション（Flask製）

## Features
- **記録機能**: 日付、タイトル、著者（複数可）、位置情報（ページ/章/節の範囲指定）、コメントを記録
- **日本語完全対応**: ブラウザのネイティブ入力フォームで日本語IMEの問題を解決
- **オートコンプリート**: タイトルと著者の入力時に既存データから候補を表示
- **検索機能**: タイトルまたは著者名で絞り込み
- **編集・削除**: 既存のエントリーを編集・削除可能
- **バリデーション**: 必須フィールドのチェック
- **設定ファイル**: `~/.config/reading-log/config.toml` で各種設定をカスタマイズ可能
- **データ永続化**: デフォルトで `~/Library/Mobile Documents/com~apple~CloudDocs/reading-logs/log.json` に保存（設定変更可能）

## Requirements
- Python 3.12+
- `uv` (推奨) または `pip`
- モダンブラウザ (Safari, Chrome, Firefox など)

## Installation

### 方法1: CLIツールとしてインストール（推奨）

最も簡単な方法です。`~/.local/bin`にコマンドをインストールします：

```bash
uv tool install git+https://github.com/s2atoru/reading-log.git
```

**使用方法:**
```bash
reading-log
```

**アンインストール:**
```bash
uv tool uninstall reading-log
```

### 方法2: ローカル開発

リポジトリをクローンして開発モードで実行：

```bash
git clone https://github.com/s2atoru/reading-log.git
cd reading-log
uv sync
uv run python -m reading_log
```

## Configuration

初回起動時に `~/.config/reading-log/config.toml` が自動作成されます。

**設定例:**
```toml
[storage]
# データ保存先のパス
path = "~/Library/Mobile Documents/com~apple~CloudDocs/reading-logs/log.json"

[validation]
# ページ番号の範囲
min_page = 1
max_page = 1000

[server]
# Flaskサーバーの設定
host = "127.0.0.1"
port = 5000
debug = true

[ui]
# ブラウザの自動起動
auto_open_browser = true
browser_delay = 1
```

設定を変更した後、アプリを再起動すると反映されます。

## Setup & Run

1.  **依存関係のインストール**:
    ```bash
    uv sync
    ```

2.  **アプリケーションの起動**:
    ```bash
    uv run python -m reading_log
    ```
    
    ブラウザが自動的に開き、`http://127.0.0.1:5000` にアクセスします。

3.  **終了**:
    ターミナルで `Ctrl+C` を押してください。

## Usage
- **入力フォーム**: 左パネルで読書記録を入力
    - *必須*: 日付、タイトル、位置情報（ページ/章/節のいずれか1つ）
    - *オプション*: 著者（複数可、カンマ区切り）、範囲指定（ページ終了、章終了、節終了）、コメント
- **オートコンプリート**: タイトルと著者の入力時に既存データから候補が表示されます
- **保存**: 「保存」ボタンをクリック
- **編集**: 右パネルのテーブルで「編集」ボタンをクリック
- **削除**: 右パネルのテーブルで「削除」ボタンをクリック
- **検索**: 右パネルの検索バーでタイトルまたは著者名を入力して「検索」ボタンをクリック

