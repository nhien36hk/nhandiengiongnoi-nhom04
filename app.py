# app.py
from flask import Flask, request, jsonify
from db import register_user, save_query_to_history, get_query_history, authenticate_user
import threading
from gui import create_gui

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        try:
            user_id = register_user(username, password)
            return jsonify({"message": "Đăng ký thành công!", "user_id": user_id}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Tên đăng nhập và mật khẩu không được để trống!"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Xác thực người dùng qua Firestore
    user = authenticate_user(username, password)
    if user:
        return jsonify({"user_id": user.get("user_id"), "message": f"Chào mừng {username}!"}), 200
    return jsonify({"error": "Tài khoản hoặc mật khẩu không chính xác!"}), 401

# Thêm route để lưu truy vấn
@app.route('/api/save_query', methods=['POST'])
def save_query():
    data = request.json
    user_id = data.get('user_id')
    question = data.get('question')
    answer = data.get('answer')
    created_at = data.get('created_at')  # Nhận thêm trường created_at

    if user_id and question and answer:
        try:
            save_query_to_history(user_id, question, answer, created_at)  # Gọi hàm với created_at
            return jsonify({"message": "Lưu truy vấn thành công!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Thông tin không đầy đủ!"}), 400

@app.route('/api/get_query_history/<string:user_id>', methods=['GET'])
def get_query_history_api(user_id):
    try:
        history = get_query_history(user_id)  # Gọi hàm lấy lịch sử truy vấn
        return jsonify(history), 200  # Trả về dữ liệu dưới dạng JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/')
def home():
    return "Welcome to the Flask app!"

def run_flask():
    app.run(debug=True, use_reloader=False)  # use_reloader=False để không khởi động lại ứng dụng nhiều lần

if __name__ == '__main__':
    # Khởi động Flask trong một luồng riêng
    threading.Thread(target=run_flask).start()
    
    # Khởi động GUI Tkinter
    create_gui()  # Gọi hàm khởi tạo GUI của bạn
