import tkinter as tk
from tkinter import messagebox
from db import register_user, authenticate_user, save_query_to_history
from virtual_assistant import (speak, get_text, get_response, assistant, 
                                current_weather, send_email, play_song, 
                                hello, get_time, set_text_widget)  # Import các hàm từ virtual_assistant
import threading

current_user_id = None  # Biến toàn cục để lưu ID người dùng hiện tại

def register():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        try:
            register_user(username, password)
            messagebox.showinfo("Đăng ký thành công", "Bạn đã đăng ký thành công!")
            entry_username.delete(0, tk.END)
            entry_password.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu.")

def login():
    global current_user_id  # Để có thể truy cập biến toàn cục này
    username = entry_username.get()
    password = entry_password.get()
    user = authenticate_user(username, password)
    if user:
        current_user_id = user[0]  # Giả sử ID người dùng là trường đầu tiên trong bảng
        messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {username}!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        start_assistant()  # Bắt đầu trợ lý ảo
    else:
        messagebox.showerror("Lỗi", "Tài khoản hoặc mật khẩu không chính xác!")

def start_assistant():
    # Tạo cửa sổ mới cho cuộc trò chuyện
    conversation_window = tk.Toplevel()
    conversation_window.title("Cuộc trò chuyện")
    speak("Xin chào, bạn tên là gì nhỉ?")

    text_widget = tk.Text(conversation_window, wrap='word')
    text_widget.pack(expand=True, fill='both')
    
    text_widget.insert(tk.END, f"Xin chào bạn muốn giúp gì ạ\n")
    text_widget.see(tk.END)  # Tự động cuộn xuống cuối
    
    set_text_widget(text_widget)

    def send_message(user_message):
        if user_message:
            # Hiển thị tin nhắn của người dùng lên giao diện
            text_widget.insert(tk.END, f"Bạn: {user_message}\n")
            text_widget.see(tk.END)  # Tự động cuộn xuống cuối

            # Lấy phản hồi từ trợ lý ảo
            response = get_response(user_message)

            if response:  # Kiểm tra xem bot có phản hồi không
                # Hiển thị phản hồi của bot lên giao diện
                text_widget.insert(tk.END, f"Đã lưu dữ liệu")
                text_widget.see(tk.END)  # Tự động cuộn xuống cuối
                # Lưu phản hồi của bot vào cơ sở dữ liệu
                save_query_to_history(current_user_id, user_message, response)
            else:
                speak("Bot không thể trả lời câu hỏi này")
                text_widget.insert(tk.END, "Bot không thể trả lời câu hỏi này.\n")
                text_widget.see(tk.END)


    def listen_to_user():
        while True:
            user_speech = get_text()  # Nhận diện giọng nói
            if user_speech:
                # Hiển thị văn bản nhận diện từ giọng nói lên giao diện
                text_widget.insert(tk.END, f"Bạn (qua giọng nói): {user_speech}\n")
                text_widget.see(tk.END)  # Tự động cuộn xuống cuối

                # Gọi hàm xử lý lệnh từ giọng nói
                send_message(user_speech)


    # Chạy việc lắng nghe người dùng trong một luồng khác
    threading.Thread(target=listen_to_user, daemon=True).start()  # Đặt daemon=True để kết thúc luồng khi chương trình chính đóng

def create_gui():
    global entry_username, entry_password
    root = tk.Tk()
    root.title("Trợ Lý Ảo")

    tk.Label(root, text="Tên đăng nhập").pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    tk.Label(root, text="Mật khẩu").pack()
    entry_password = tk.Entry(root, show='*')
    entry_password.pack()

    tk.Button(root, text="Đăng ký", command=register).pack()
    tk.Button(root, text="Đăng nhập", command=login).pack()

    root.mainloop()

if __name__ == "__main__":
    create_gui()