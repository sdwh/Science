import sqlite3

def fetch_common_questions(humor=False, question=None):
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
