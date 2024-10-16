# db.py
import mysql.connector

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

def save_query_to_history(user_id, question, answer):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO query_history (user_id, question, answer) VALUES (%s, %s, %s)",
                   (user_id, question, answer))
    db.commit()
    db.close()
