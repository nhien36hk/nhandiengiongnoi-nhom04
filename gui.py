import tkinter as tk
from tkinter import messagebox
import requests  # Thêm thư viện requests để thực hiện các yêu cầu HTTP
from db import save_query_to_history
from PIL import Image, ImageTk
from virtual_assistant import (speak, get_text, get_response, set_text_widget)  # Import các hàm cần thiết từ virtual_assistant
import threading
from datetime import datetime

current_user_id = None  # Biến toàn cục để lưu ID người dùng hiện tại
FLASK_API_URL = "http://127.0.0.1:5000"  # Địa chỉ API Flask

def register():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        try:
            response = requests.post(f"{FLASK_API_URL}/register", json={"username": username, "password": password})
            if response.status_code == 201:
                messagebox.showinfo("Đăng ký thành công", response.json()["message"])
                entry_username.delete(0, tk.END)
                entry_password.delete(0, tk.END)
            else:
                messagebox.showerror("Lỗi", response.json().get("error", "Có lỗi xảy ra!"))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu.")

def login():
    global current_user_id  # Để có thể truy cập biến toàn cục này
    username = entry_username.get()
    password = entry_password.get()
    response = requests.post(f"{FLASK_API_URL}/login", json={"username": username, "password": password})
    
    if response.status_code == 200:
        current_user_id = response.json()["user_id"]  # Lưu ID người dùng
        messagebox.showinfo("Đăng nhập thành công", response.json()["message"])
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        show_assistant_interface()  # Hiển thị giao diện trợ lý ảo
    else:
        messagebox.showerror("Lỗi", response.json().get("error", "Có lỗi xảy ra!"))
        
def fetch_query_history():
    url = f"{FLASK_API_URL}/api/get_query_history/{current_user_id}"  # URL để lấy lịch sử truy vấn
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Giả sử API trả về danh sách các truy vấn
        else:
            messagebox.showerror("Lỗi", "Không thể lấy lịch sử truy vấn.")
            return []
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
        return []
        
def save_query(user_id, question, answer):
    url = 'http://127.0.0.1:5000/api/save_query'  # Địa chỉ API
    payload = {
        'user_id': user_id,
        'question': question,
        'answer': answer,
        'created_at': datetime.now().isoformat()  # Lưu thời gian hiện tại theo định dạng ISO
    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        print('Query saved successfully!')
    else:
        print(f'Failed to save query: {response.text}')
            

def show_assistant_interface():
    # Ẩn các phần đăng nhập
    login_frame.pack_forget()

    # Hiển thị giao diện trợ lý ảo
    assistant_frame.pack(fill=tk.BOTH, expand=True)

    # Setup Image
    setup_image(assistant_frame)

    # Add a text widget
    text_widget = tk.Text(assistant_frame, font=('Courier 10 bold'), bg="#356696")
    text_widget.pack(expand=True, fill='both', padx=10, pady=10)

    # Add a entry widget
    entry1 = tk.Entry(assistant_frame, justify=tk.CENTER)
    entry1.pack(padx=10, pady=(0, 10), fill=tk.X)

    # Khung chứa nút
    button_frame = tk.Frame(assistant_frame)
    button_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 5))  # Căn chỉnh khung nút

    # Nút ASK
    button1 = tk.Button(button_frame, text="ASK", bg="#356696", pady=10, padx=40, command=lambda: ask(text_widget))
    button1.pack(side=tk.LEFT, padx=(0, 5))  # Căn chỉnh nút sang trái trong khung
    
    # Nút Delete
    button2 = tk.Button(button_frame, text="Send", bg="#356696", pady=10, padx=40, command=lambda: send_message_in_thread(entry1.get(), text_widget))
    button2.pack(side=tk.LEFT, padx=(5, 0))  # Căn chỉnh nút sang trái trong khung

    # Nút Delete
    button3 = tk.Button(button_frame, text="Delete", bg="#356696", pady=10, padx=40, command=lambda: delete_text(text_widget))
    button3.pack(side=tk.LEFT, padx=(5, 0))  # Căn chỉnh nút sang trái trong khung
    
    # Nút Show History
    button_history = tk.Button(button_frame, text="Xem Lịch Sử", bg="#356696", pady=10, padx=40, command=lambda: show_query_history(text_widget))
    button_history.pack(side=tk.LEFT, padx=(5, 0))  # Căn chỉnh nút sang trái trong khung

    # Đặt câu hỏi về cuộc trò chuyện
    text_widget.insert(tk.END, f"Xin chào bạn muốn giúp gì ạ\n")
    text_widget.see(tk.END)  # Tự động cuộn xuống cuối
    set_text_widget(text_widget)
    
def send_message_in_thread(user_message, text_widget):
    threading.Thread(target=send_message, args=(user_message, text_widget), daemon=True).start()

def send_message(user_message, text_widget):
    if user_message:        
        # Hiển thị văn bản nhận diện từ giọng nói lên giao diện
        text_widget.insert(tk.END, f"Bạn: {user_message}\n")
        text_widget.see(tk.END)  # Tự động cuộn xuống cuối
        # Lấy phản hồi từ trợ lý ảo
        response = get_response(user_message)

        if response:  # Kiểm tra xem bot có phản hồi không
            # Hiển thị phản hồi của bot lên giao diện
            text_widget.insert(tk.END, f"Bot: {response}\n")
            text_widget.see(tk.END)  # Tự động cuộn xuống cuối
            # Lưu phản hồi của bot vào cơ sở dữ liệu
            save_query(current_user_id, user_message, response) 
        else:
            speak("Bot không thể trả lời câu hỏi này.")
            text_widget.insert(tk.END, "Bot không thể trả lời câu hỏi này.\n")
            text_widget.see(tk.END)
            
def ask(text_widget):
    # Khởi động việc lắng nghe người dùng
    threading.Thread(target=listen_to_user, args=(text_widget,), daemon=True).start()
    
def delete_text(text_widget):
    text_widget.delete("1.0", "end")

def listen_to_user(text_widget):
    while True:
        user_speech = get_text()  # Nhận diện giọng nói
        if user_speech:
            # Gọi hàm xử lý lệnh từ giọng nói
            send_message(user_speech, text_widget)
            
def show_query_history(text_widget):
    text_widget.delete("1.0", "end")  # Xóa nội dung hiện tại trong text_widget
    history = fetch_query_history()
    
    if history:
        for query in history:
            text_widget.insert(tk.END, f"User ID: {query['user_id']}\n")
            text_widget.insert(tk.END, f"Câu hỏi: {query['question']}\n")
            text_widget.insert(tk.END, f"Trả lời: {query['answer']}\n")
            text_widget.insert(tk.END, f"Thời gian: {query['created_at']}\n")
            text_widget.insert(tk.END, "----------------------------------\n")
    else:
        text_widget.insert(tk.END, "Không có lịch sử truy vấn.\n")
    text_widget.see(tk.END)  # Tự động cuộn xuống cuối

def setup_image(parent_frame):
    try:
        image_path = "image/assitant.png"  # Đường dẫn đến hình ảnh
        image = Image.open(image_path)
        image = image.resize((400, 400))  # Thay đổi kích thước nếu cần
        photo = ImageTk.PhotoImage(image)

        illustration = tk.Label(parent_frame, image=photo, bg="white")
        illustration.image = photo  # Lưu biến để tránh garbage collection
        illustration.pack(pady=20)  # Sử dụng pack để căn chỉnh
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải hình ảnh: {str(e)}")
        # Nếu không thể tải hình ảnh, bạn có thể hiển thị một placeholder
        show_image_placeholder(parent_frame)

def show_image_placeholder(parent_frame):
    placeholder_text = "Image not available"
    placeholder_label = tk.Label(parent_frame, text=placeholder_text, bg="white")
    placeholder_label.pack(pady=20)  # Đảm bảo sử dụng pack cho tính nhất quán

def create_gui():
    global entry_username, entry_password, login_frame, assistant_frame

    # Tạo cửa sổ chính
    root = tk.Tk()
    screen_height = root.winfo_screenheight()
    root.geometry(f"550x{screen_height - 100}")  # Đặt chiều cao bằng chiều cao màn hình trừ đi 20px
    root.title("Trợ Lý Ảo")

    # Khung đăng nhập
    login_frame = tk.Frame(root)
    tk.Label(login_frame, text="Tên đăng nhập").pack()
    entry_username = tk.Entry(login_frame)
    entry_username.pack()

    tk.Label(login_frame, text="Mật khẩu").pack()
    entry_password = tk.Entry(login_frame, show='*')   
    entry_password.pack()

    tk.Button(login_frame, text="Đăng ký", command=register).pack(pady=(10, 5))
    tk.Button(login_frame, text="Đăng nhập", command=login).pack()

    login_frame.pack(fill=tk.BOTH, expand=True)  # Hiển thị khung đăng nhập

    # Khung trợ lý ảo
    assistant_frame = tk.Frame(root)

    root.mainloop()

