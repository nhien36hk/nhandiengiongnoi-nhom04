# db.py
import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='127.0.0.1',      # Địa chỉ máy chủ cơ sở dữ liệu
        user='root',           # Tên người dùng (username)
        password='',           # Mật khẩu (password), thay đổi nếu có
        database='assistant_db'     # Tên cơ sở dữ liệu (database)
    )

def register_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    db.close()

def authenticate_user(username, password):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    db.close()
    return user

def save_query_to_history(user_id, question, answer, created_at=None):
    db = connect_db()
    cursor = db.cursor()
    
    if created_at is None:
        created_at = datetime.now()  # Sử dụng thời gian hiện tại nếu không có
    
    cursor.execute(
        "INSERT INTO query_history (user_id, question, answer, created_at) VALUES (%s, %s, %s, %s)",
        (user_id, question, answer, created_at)
    )
    db.commit()
    db.close()
    
def get_query_history(user_id):
    connection = connect_db()  # Hàm tạo kết nối với cơ sở dữ liệu
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, question, answer, created_at FROM query_history WHERE user_id = %s", (user_id,))
    rows = cursor.fetchall()
    
    history = []
    for row in rows:
        history.append({
            'user_id': row[0],
            'question': row[1],
            'answer': row[2],
            'created_at': row[3].isoformat()  # Đảm bảo rằng thời gian là định dạng ISO
        })
    
    cursor.close()
    connection.close()
    
    return history

