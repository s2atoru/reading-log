from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
from pathlib import Path
from reading_log.data_handler import DataHandler, ReadingLogEntry

app = Flask(__name__)
data_handler = DataHandler()

@app.route('/')
def index():
    """メインページを表示"""
    return render_template('index.html')

@app.route('/api/entries', methods=['GET'])
def get_entries():
    """エントリー一覧を取得（検索対応）"""
    query = request.args.get('q', '')
    entries = data_handler.search_entries(query)
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'author': e.author,
        'date': e.date,
        'page': e.page,
        'chapter': e.chapter,
        'section': e.section,
        'comment': e.comment,
        'timestamp': e.timestamp
    } for e in entries])

@app.route('/api/save', methods=['POST'])
def save_entry():
    """新しいエントリーを保存"""
    try:
        data = request.json
        
        # ページのバリデーション
        page = None
        page_end = None
        if data.get('page'):
            try:
                page = int(data['page'])
                if page < 1 or page > 1000:
                    return jsonify({'success': False, 'error': 'ページは1から1000の範囲で入力してください。'}), 400
            except ValueError:
                return jsonify({'success': False, 'error': f'ページには数値を入力してください: {data["page"]}'}), 400
        
        if data.get('page_end'):
            try:
                page_end = int(data['page_end'])
                if page_end < 1 or page_end > 1000:
                    return jsonify({'success': False, 'error': 'ページ終了は1から1000の範囲で入力してください。'}), 400
                if page and page_end < page:
                    return jsonify({'success': False, 'error': 'ページ終了は開始ページ以上である必要があります。'}), 400
            except ValueError:
                return jsonify({'success': False, 'error': f'ページ終了には数値を入力してください: {data["page_end"]}'}), 400
        
        entry = ReadingLogEntry(
            title=data.get('title', ''),
            author=data.get('author', ''),
            date=data.get('date', ''),
            page=page,
            page_end=page_end,
            chapter=data.get('chapter') or None,
            chapter_end=data.get('chapter_end') or None,
            section=data.get('section') or None,
            section_end=data.get('section_end') or None,
            comment=data.get('comment', '')
        )
        
        data_handler.save_entry(entry)
        return jsonify({'success': True, 'message': '保存しました！'})
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'予期しないエラー: {e}'}), 500

@app.route('/api/update/<entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """既存のエントリーを更新"""
    try:
        data = request.json
        
        # ページのバリデーション
        page = None
        page_end = None
        if data.get('page'):
            try:
                page = int(data['page'])
                if page < 1 or page > 1000:
                    return jsonify({'success': False, 'error': 'ページは1から1000の範囲で入力してください。'}), 400
            except ValueError:
                return jsonify({'success': False, 'error': f'ページには数値を入力してください: {data["page"]}'}), 400
        
        if data.get('page_end'):
            try:
                page_end = int(data['page_end'])
                if page_end < 1 or page_end > 1000:
                    return jsonify({'success': False, 'error': 'ページ終了は1から1000の範囲で入力してください。'}), 400
                if page and page_end < page:
                    return jsonify({'success': False, 'error': 'ページ終了は開始ページ以上である必要があります。'}), 400
            except ValueError:
                return jsonify({'success': False, 'error': f'ページ終了には数値を入力してください: {data["page_end"]}'}), 400
        
        # 既存のエントリーを読み込み
        entries = data_handler.load_entries()
        
        # 対象のエントリーを検索
        target_entry = None
        for i, entry in enumerate(entries):
            if entry.id == entry_id:
                # エントリーを更新
                entries[i] = ReadingLogEntry(
                    id=entry_id,  # IDは保持
                    title=data.get('title', ''),
                    author=data.get('author', ''),
                    date=data.get('date', ''),
                    page=page,
                    page_end=page_end,
                    chapter=data.get('chapter') or None,
                    chapter_end=data.get('chapter_end') or None,
                    section=data.get('section') or None,
                    section_end=data.get('section_end') or None,
                    comment=data.get('comment', ''),
                    timestamp=entry.timestamp  # 元のタイムスタンプを保持
                )
                target_entry = entries[i]
                break
        
        if not target_entry:
            return jsonify({'success': False, 'error': 'エントリーが見つかりません'}), 404
        
        # バリデーション
        target_entry.validate()
        
        # 保存
        import json
        from dataclasses import asdict
        with open(data_handler.storage_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': '更新しました！'})
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'予期しないエラー: {e}'}), 500

@app.route('/api/delete/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """エントリーを削除"""
    try:
        entries = data_handler.load_entries()
        
        # 対象のエントリーを検索して削除
        original_count = len(entries)
        entries = [e for e in entries if e.id != entry_id]
        
        if len(entries) == original_count:
            return jsonify({'success': False, 'error': 'エントリーが見つかりません'}), 404
        
        # 保存
        import json
        from dataclasses import asdict
        with open(data_handler.storage_path, 'w', encoding='utf-8') as f:
            json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
        
        return jsonify({'success': True, 'message': '削除しました！'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'予期しないエラー: {e}'}), 500

def open_browser():
    """ブラウザを自動で開く"""
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # 1秒後にブラウザを開く
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
