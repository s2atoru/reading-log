# 📚 Reading Log App

読書記録を管理するためのWebアプリケーション（Flask製）

## Features
- **記録機能**: 日付、タイトル、著者（複数可）、位置情報（ページ/章/節の範囲指定）、コメントを記録
- **日本語完全対応**: ブラウザのネイティブ入力フォームで日本語IMEの問題を解決
- **オートコンプリート**: タイトルと著者の入力時に既存データから候補を表示
- **検索機能**: タイトル、著者名、またはコメントで絞り込み（クリアボタン付き）
- **編集・削除**: 既存のエントリーを編集・削除可能
- **バリデーション**: 必須フィールドのチェック
- **設定ファイル**: `~/.config/reading-log/config.toml` で各種設定をカスタマイズ可能
- **データ永続化**: デフォルトで `~/Library/Mobile Documents/com~apple~CloudDocs/reading-logs/log.json` に保存（設定変更可能）
  - **注意**: デフォルトのパスはmacOS（iCloud）向けです。Windows/Linuxユーザーは初回起動後に設定ファイルでパスを変更してください（例: `~/Documents/reading-logs/log.json`）

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
min_page = 0
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

## Usage
- **入力フォーム**: 左パネルで読書記録を入力
    - *必須*: 日付、タイトル、位置情報（ページ/章/節のいずれか1つ）
    - *オプション*: 著者（複数可、カンマ区切り）、範囲指定（ページ終了、章終了、節終了）、コメント
- **オートコンプリート**: タイトルと著者の入力時に既存データから候補が表示されます
- **保存**: 「保存」ボタンをクリック
- **編集**: 右パネルのテーブルで「確認」ボタンをクリック
- **削除**: 右パネルのテーブルで「削除」ボタンをクリック
- **検索**: 右パネルの検索バーでタイトル、著者名、またはコメントを入力して「検索」ボタンをクリック（「クリア」ボタンで検索条件をリセット）

## Troubleshooting

### ポート5000が既に使用されている
別のアプリケーションがポート5000を使用している場合、設定ファイル（`~/.config/reading-log/config.toml`）で別のポートを指定してください：
```toml
[server]
port = 5001
```

### ブラウザが自動的に開かない
設定ファイルで `auto_open_browser` が `false` に設定されている場合、手動でブラウザを開いてください：
```
http://127.0.0.1:5000
```
または、設定ファイルを変更してください：
```toml
[ui]
auto_open_browser = true
```

### iCloudフォルダにアクセスできない
Windows/Linuxユーザー、またはiCloudを使用していない場合は、設定ファイルでデータ保存先を変更してください：
```toml
[storage]
path = "~/Documents/reading-logs/log.json"
```

### JSONファイルが壊れた
バックアップがない場合、以下の手順でリセットできます：
1. 既存のJSONファイルを別の場所に移動またはリネーム
2. アプリケーションを再起動すると、新しい空のJSONファイルが作成されます

### データが保存されない
- データファイルのディレクトリに書き込み権限があることを確認してください
- ディスクの空き容量を確認してください
- エラーメッセージを確認してください（ターミナルに表示されます）

### 設定ファイルの場所が分からない
設定ファイルは以下の場所にあります：
- **Unix/Linux/macOS**: `~/.config/reading-log/config.toml`
- **Windows**: `C:\Users\<ユーザー名>\.config\reading-log\config.toml`

