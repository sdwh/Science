import sqlite3

# 連接到資料庫
conn = sqlite3.connect('chat_api_responses.db')
cursor = conn.cursor()

# 執行刪除操作
timestamp_to_delete = '2024-10-02T14:46:35.032758'
cursor.execute("DELETE FROM responses WHERE timestamp = ?", (timestamp_to_delete,))

# 提交更改
conn.commit()

# 關閉連接
conn.close()