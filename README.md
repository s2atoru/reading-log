# Reading Log App

読書記録を管理するためのWebアプリケーション（Flask製）

## Features
- **記録機能**: 日付、タイトル、著者、位置情報（ページ/章/節）、コメントを記録
- **日本語完全対応**: ブラウザのネイティブ入力フォームで日本語IMEの問題を解決
- **検索機能**: タイトルまたは著者名で絞り込み
- **バリデーション**: 必須フィールドのチェック
- **データ永続化**: `~/Library/Mobile Documents/com~apple~CloudDocs/reading-logs/log.json` に保存

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
- **保存**: 「保存」ボタンをクリック
- **検索**: 右パネルの検索バーでタイトルまたは著者名を入力して「検索」ボタンをクリック

