import os
import sqlite3
import markdown
import htmlmin

def fetch_common_questions(humor = False, question = None):
    # 連接到 SQLite 資料庫
    conn = sqlite3.connect('chat_api_responses.db')
    cursor = conn.cursor()

    try:
        # SQL 查詢語句
        if humor:
            query = """
            SELECT question, response, keyword
            FROM responses
            WHERE keyword = 'common_question_humorous' AND question = ?
            LIMIT 1
            """
            cursor.execute(query, (question,))
        else:
            query = """
            SELECT question, response, keyword
            FROM responses
            WHERE keyword LIKE 'common_question'
            """
            cursor.execute(query)

        # 獲取所有結果
        results = cursor.fetchall()
        return results
    finally:
        # 關閉連接
        conn.close()

# 調用函數
results = fetch_common_questions()

# Render HTML Index page
with open('template_index.html', 'r', encoding='utf-8') as file:
    template = file.read()

content = '<ol>'
content += ''.join([f'<li class="mb-1"><a class="text-decoration-none" href="{idx+1}.html">{row[0]}</a></li>' for idx, row in enumerate(results)])
content += '</ol>'
content = template.replace('{{insert_block}}', content)
minified_content = htmlmin.minify(content, remove_empty_space=True)
file_name = os.path.join('docs', 'index.html')
with open(file_name, 'w', encoding='utf-8') as file:
    file.write(minified_content)

# Render HTML for each question
id = 1
for row in results:

    with open('template_page.html', 'r', encoding='utf-8') as file:
        template = file.read()
    html_content = markdown.markdown(row[1])

    #humor = fetch_common_questions(True, row[0])[0][1]
    #html_content_humor = markdown.markdown(humor)

    prev_id = max(id - 1, 1)
    next_id = min(id + 1, len(results))

    content = template.replace('{{insert_block}}', f'<h2>{id} - {row[0]}</h2><p>{html_content}</p>')
    content = content.replace('{{id}}', f'{prev_id}')
    content = content.replace('{{prev}}', f'{prev_id}')
    content = content.replace('{{next}}', f'{next_id}')

    minified_content = htmlmin.minify(content, remove_empty_space=True)
    file_name = os.path.join('docs', f'{id}.html')

    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(minified_content)
    
    id += 1