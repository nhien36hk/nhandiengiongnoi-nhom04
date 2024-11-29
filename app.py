# app.py
from flask import Flask, request, jsonify, Response, stream_with_context
import re
from db import register_user, save_query_to_history, get_query_history, authenticate_user, create_or_update_google_user
import threading
from gui import create_gui
from virtual_assistant import get_response
import json
import tkinter as tk
from openai import OpenAI
from datetime import datetime
import time
import pytz

app = Flask(__name__)

conversation_history = []
client = OpenAI(
    base_url="https://384b-2402-800-63b6-c3d0-e8b3-5f68-9684-b9de.ngrok-free.app/v1",
    api_key="ollama"
)

def is_valid_email(email):
    # Kiểm tra định dạng email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    
    # Kiểm tra nếu email, password hoặc full_name là None hoặc rỗng
    if not email or not password or not full_name:
        return jsonify({"error": "Email, mật khẩu và họ tên không được để trống!"}), 400
    
    if not is_valid_email(email):
        return jsonify({"error": "Email không hợp lệ!"}), 400
    
    try:
        register_user(email, password, full_name)
        return jsonify({"message": "Đăng ký thành công! Vui lòng xác nhận email của bạn."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = authenticate_user(email, password)
    if user and "error" not in user:
        return jsonify({"user_id": user["user_id"], "message": f"Chào mừng {email}!"}), 200
    elif user and "error" in user:
        return jsonify({"error": user["error"]}), 401
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
    
@app.route('/api/get_response', methods=['POST'])
def api_get_response():
    data = request.json
    user_message = data.get('user_message')
    
    print(user_message)
    
    if user_message:
        # Gọi hàm get_response để lấy phản hồi từ trợ lý ảo
        response = get_response(user_message)
        if response:
            return jsonify({"response": response}), 200
        else:
            return jsonify({"error": "Không thể xử lý yêu cầu."}), 500
    return jsonify({"error": "Thiếu tin nhắn từ người dùng."}), 400

@app.route('/')
def home():
    return "Welcome to the Flask app!"

def run_flask():
    # Cập nhật dòng này để Flask lắng nghe tất cả các kết nối từ ngoài localhost
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)

@app.route('/api/stream_response', methods=['POST'])
def stream_response():
    data = request.json
    text = data.get('text', '')
    user_id = data.get('user_id')

    def generate():
        try:
            global conversation_history
            conversation_history.append({"role": "user", "content": text})

            # Gọi API trả về dữ liệu stream
            response_stream = client.chat.completions.create(
                model="gemma2:9b",  # Chọn mô hình AI
                messages=conversation_history,  # Lịch sử cuộc trò chuyện
                temperature=0.7,  # Điều chỉnh tính ngẫu nhiên của phản hồi
                max_tokens=2048,  # Giới hạn số token tối đa trong phản hồi
                stream=True  # Bật chế độ streaming
            )

            full_response = ""
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    # Gửi từng ký tự một
                    for char in content:
                        full_response += char
                        yield f"data: {json.dumps({'content': char})}\n\n"
                        time.sleep(0.001)  # Giảm tốc độ stream nếu cần thiết

            conversation_history.append({"role": "assistant", "content": full_response})

            if len(conversation_history) > 10:
                conversation_history = conversation_history[-10:]

            # Lưu vào cơ sở dữ liệu nếu có user_id
            if user_id:
                try:
                    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
                    created_at = datetime.now(vietnam_tz).strftime('%Y-%m-%d %H:%M:%S') # Hour, minutes, seconds
                    save_query_to_history(user_id, text, full_response, created_at)
                except Exception as e:
                    print(f"Error saving to database: {e}")

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    # Tạo Response, tắt buffering bằng cách thêm header 'X-Accel-Buffering'
    response = Response(generate())
    response.headers['X-Accel-Buffering'] = 'no'  # Tắt buffering
    return response

@app.route('/google_sign_in', methods=['POST'])
def google_sign_in():
    try:
        data = request.json
        email = data.get('email')
        name = data.get('name')
        uid = data.get('uid')
        
        success, error = create_or_update_google_user(email, name, uid)
        if success:
            return jsonify({"message": "Success"}), 200
        else:
            return jsonify({"error": error}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Khởi động Flask trong một luồng riêng
    flask_thread = threading.Thread(target=run_flask, daemon=True)  # Thêm daemon=True
    flask_thread.start()
    
    # Khởi động GUI Tkinter
    create_gui()
