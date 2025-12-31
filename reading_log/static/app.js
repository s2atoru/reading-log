```javascript
// 今日の日付をデフォルトで設定
document.addEventListener('DOMContentLoaded', function () {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
    loadEntries();
    loadAutocomplete();
});

// オートコンプリートデータを読み込む
async function loadAutocomplete() {
    try {
        const response = await fetch('/api/autocomplete');
        const data = await response.json();
        
        // タイトルの候補を設定
        const titleDatalist = document.getElementById('title-suggestions');
        titleDatalist.innerHTML = '';
        data.titles.forEach(title => {
            const option = document.createElement('option');
            option.value = title;
            titleDatalist.appendChild(option);
        });
        
        // 著者の候補を設定
        const authorDatalist = document.getElementById('author-suggestions');
        authorDatalist.innerHTML = '';
        data.authors.forEach(author => {
            const option = document.createElement('option');
            option.value = author;
            authorDatalist.appendChild(option);
        });
    } catch (error) {
        console.error('オートコンプリートデータの読み込みに失敗しました:', error);
    }
}


// フォーム送信処理
document.getElementById('entryForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const editingId = document.getElementById('editingId').value;
    const isEditing = editingId !== '';

    const formData = {
        title: document.getElementById('title').value,
        author: document.getElementById('author').value,
        date: document.getElementById('date').value,
        page: document.getElementById('page').value,
        page_end: document.getElementById('page_end').value,
        chapter: document.getElementById('chapter').value,
        chapter_end: document.getElementById('chapter_end').value,
        section: document.getElementById('section').value,
        section_end: document.getElementById('section_end').value,
        comment: document.getElementById('comment').value
    };

    try {
        const url = isEditing ? `/ api / update / ${ editingId } ` : '/api/save';
        const method = isEditing ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        const statusDiv = document.getElementById('status');

        if (result.success) {
            statusDiv.textContent = result.message;
            statusDiv.className = 'status-message success';

            // フォームをクリア
            cancelEdit();

            // 一覧を更新
            loadEntries();
            loadAutocomplete(); // オートコンプリートも更新
             // 3秒後にメッセージを消す
            setTimeout(() => {
                statusDiv.textContent = '';
                statusDiv.className = 'status-message';
            }, 3000);
        } else {
            statusDiv.textContent = result.error;
            statusDiv.className = 'status-message error';
        }
    } catch (error) {
        const statusDiv = document.getElementById('status');
        statusDiv.textContent = 'エラーが発生しました: ' + error.message;
        statusDiv.className = 'status-message error';
    }
});

// エントリーを編集モードで読み込む
function editEntry(entry) {
    document.getElementById('editingId').value = entry.id;
    document.getElementById('formTitle').textContent = '編集フォーム';
    document.getElementById('submitBtn').textContent = '更新';
    document.getElementById('cancelBtn').style.display = 'inline-block';

    document.getElementById('title').value = entry.title;
    document.getElementById('author').value = entry.author;
    document.getElementById('date').value = entry.date;
    document.getElementById('page').value = entry.page || '';
    document.getElementById('page_end').value = entry.page_end || '';
    document.getElementById('chapter').value = entry.chapter || '';
    document.getElementById('chapter_end').value = entry.chapter_end || '';
    document.getElementById('section').value = entry.section || '';
    document.getElementById('section_end').value = entry.section_end || '';
    document.getElementById('comment').value = entry.comment || '';

    // フォームまでスクロール
    document.querySelector('.input-panel').scrollIntoView({ behavior: 'smooth' });
}

// 編集をキャンセル
function cancelEdit() {
    document.getElementById('editingId').value = '';
    document.getElementById('formTitle').textContent = '入力フォーム';
    document.getElementById('submitBtn').textContent = '保存';
    document.getElementById('cancelBtn').style.display = 'none';

    document.getElementById('entryForm').reset();
    document.getElementById('date').value = new Date().toISOString().split('T')[0];
}

// エントリーを削除
async function deleteEntry(entryId, title) {
    if (!confirm(`「${ title }」を削除しますか？`)) {
        return;
    }

    try {
        const response = await fetch(`/ api / delete/${entryId}`, {
method: 'DELETE'
        });

const result = await response.json();

if (result.success) {
    loadEntries();

    const statusDiv = document.getElementById('status');
    statusDiv.textContent = result.message;
    statusDiv.className = 'status-message success';

    setTimeout(() => {
        statusDiv.textContent = '';
        statusDiv.className = 'status-message';
    }, 3000);
} else {
    alert('削除に失敗しました: ' + result.error);
}
    } catch (error) {
    alert('エラーが発生しました: ' + error.message);
}
}

// エントリー一覧を読み込む
async function loadEntries() {
    const query = document.getElementById('searchInput').value;
    const url = query ? `/api/entries?q=${encodeURIComponent(query)}` : '/api/entries';

    try {
        const response = await fetch(url);
        const entries = await response.json();

        const tbody = document.getElementById('entriesBody');
        tbody.innerHTML = '';

        entries.forEach(entry => {
            const row = document.createElement('tr');

            // 位置情報をフォーマット
            const positions = [];
            if (entry.page) {
                if (entry.page_end) {
                    positions.push(`p.${entry.page}-${entry.page_end}`);
                } else {
                    positions.push(`p.${entry.page}`);
                }
            }
            if (entry.chapter) {
                if (entry.chapter_end) {
                    positions.push(`ch.${entry.chapter}-${entry.chapter_end}`);
                } else {
                    positions.push(`ch.${entry.chapter}`);
                }
            }
            if (entry.section) {
                if (entry.section_end) {
                    positions.push(`sec.${entry.section}-${entry.section_end}`);
                } else {
                    positions.push(`sec.${entry.section}`);
                }
            }
            const positionStr = positions.join(', ');

            row.innerHTML = `
                <td>${entry.date}</td>
                <td>${escapeHtml(entry.title)}</td>
                <td>${escapeHtml(entry.author)}</td>
                <td>${positionStr}</td>
                <td>
                    <button class="btn-edit" onclick='editEntry(${JSON.stringify(entry)})'>編集</button>
                    <button class="btn-delete" onclick="deleteEntry('${entry.id}', '${escapeHtml(entry.title)}')">削除</button>
                </td>
            `;

            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('エントリーの読み込みに失敗しました:', error);
    }
}

// HTMLエスケープ
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 検索フィールドでEnterキーを押したら検索
document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        loadEntries();
    }
});
