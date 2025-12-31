from flask import Flask, render_template, request, jsonify
import webbrowser
import threading
from reading_log.data_handler import DataHandler, ReadingLogEntry
from reading_log.validators import validate_page_range

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
        'page_end': e.page_end,
        'chapter': e.chapter,
        'chapter_end': e.chapter_end,
        'section': e.section,
        'section_end': e.section_end,
        'comment': e.comment,
        'timestamp': e.timestamp
    } for e in entries])

@app.route('/api/autocomplete', methods=['GET'])
def get_autocomplete():
    """オートコンプリート用のタイトルと著者一覧を取得"""
    entries = data_handler.load_entries()
    
    # 重複を除いたタイトルと著者のリストを作成
    titles = sorted(set(e.title for e in entries if e.title.strip()))
    authors = sorted(set(e.author for e in entries if e.author.strip()))
    
    return jsonify({
        'titles': titles,
        'authors': authors
    })


@app.route('/api/save', methods=['POST'])
def save_entry():
    """新しいエントリーを保存"""
    try:
        data = request.json
        
        # ページのバリデーション
        page, page_end, error = validate_page_range(
            data.get('page'),
            data.get('page_end')
        )
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
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
        page, page_end, error = validate_page_range(
            data.get('page'),
            data.get('page_end')
        )
        if error:
            return jsonify({'success': False, 'error': error}), 400
        
        # 既存のエントリーを取得してタイムスタンプを保持
        entries = data_handler.load_entries()
        original_timestamp = None
        for entry in entries:
            if entry.id == entry_id:
                original_timestamp = entry.timestamp
                break
        
        if not original_timestamp:
            return jsonify({'success': False, 'error': 'エントリーが見つかりません'}), 404
        
        # 更新されたエントリーを作成
        updated_entry = ReadingLogEntry(
            id=entry_id,
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
            timestamp=original_timestamp
        )
        
        # DataHandlerを使用して更新
        if data_handler.update_entry(entry_id, updated_entry):
            return jsonify({'success': True, 'message': '更新しました！'})
        else:
            return jsonify({'success': False, 'error': 'エントリーが見つかりません'}), 404
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'予期しないエラー: {e}'}), 500

@app.route('/api/delete/<entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """エントリーを削除"""
    try:
        if data_handler.delete_entry(entry_id):
            return jsonify({'success': True, 'message': '削除しました！'})
        else:
            return jsonify({'success': False, 'error': 'エントリーが見つかりません'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': f'予期しないエラー: {e}'}), 500

def open_browser():
    """ブラウザを自動で開く"""
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # 1秒後にブラウザを開く
    threading.Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)
