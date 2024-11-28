import tkinter as tk
from tkinter import messagebox
import requests  # Thêm thư viện requests để thực hiện các yêu cầu HTTP
from db import save_query_to_history
from PIL import Image, ImageTk
from virtual_assistant import (speak, get_text, get_response, set_text_widget)  # Import các hàm cần thiết từ virtual_assistant
import threading
from datetime import datetime
import sys
import os

# Add at the top with other global variables
root = None
current_user_id = None
FLASK_API_URL = "http://127.0.0.1:5000"
global entry_email, entry_password, entry_full_name, login_frame, button_frame

# Global variable for entry_full_name
entry_full_name = None  # Initialize it

# Add this at the top with other global variables
text_widget = None

# Thêm biến global ở đầu file
is_listening = False

# Thêm biến toàn cục cho nút mic
mic_btn = None

# Add at the top with other global variables
mic_image = None
mic_active_image = None

def on_closing():
    """Hàm xử lý khi đóng cửa sổ"""
    if messagebox.askokcancel("Thoát", "Bạn có muốn thoát chương trình?"):
        # Đóng cửa sổ Tkinter
        root.destroy()
        # Tắt toàn bộ chương trình
        os._exit(0)  # Hoặc sys.exit(0)


def register():
    global entry_full_name  # Đảm bảo biến này được khai báo là toàn cục
    username = entry_email.get()  # Lấy gi trị từ trường email
    password = entry_password.get()  # Lấy giá trị từ trường password
    full_name = entry_full_name.get()  # Lấy giá trị từ trường full_name

    # Ghi log để kiểm tra giá trị nhận được
    print(f"Username: {username}, Password: {password}, Full Name: {full_name}")

    if username and password and full_name:
        try:
            response = requests.post(f"{FLASK_API_URL}/register", json={
                "email": username,
                "password": password,
                "full_name": full_name
            })
            if response.status_code == 201:
                messagebox.showinfo("Đăng ký thành công", response.json()["message"])
                entry_email.delete(0, tk.END)
                entry_password.delete(0, tk.END)
                entry_full_name.delete(0, tk.END)  # Xóa trường full_name
            else:
                messagebox.showerror("Lỗi", response.json().get("error", "Có lỗi xảy ra!"))
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    else:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập, mật khẩu và họ tên.")

def login():
    global current_user_id
    username = entry_email.get()  # Lấy giá trị từ trường email
    password = entry_password.get()  # Lấy giá trị từ trường password

    # Ghi log để kiểm tra giá trị nhận được
    print(f"Debug - Username: {username}, Password: {password}")

    if not username or not password:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập email và mật khẩu.")
        return

    try:
        response = requests.post(f"{FLASK_API_URL}/login", json={"email": username, "password": password})
        response_data = response.json()  # Thử chuyển đổi phản hồi thành JSON

        if response.status_code == 200:
            current_user_id = response_data["user_id"]
            messagebox.showinfo("Đăng nhập thành công", response_data["message"])
            entry_email.delete(0, tk.END)
            entry_password.delete(0, tk.END)

            # Ẩn toàn bộ khung đăng nhập và minh họa
            main_container.pack_forget()

            # Hiển thị giao diện trợ lý ảo
            show_assistant_interface()
        else:
            messagebox.showerror("Lỗi", response_data.get("error", "Có lỗi xảy ra!"))
    except requests.exceptions.JSONDecodeError:
        messagebox.showerror("Lỗi", "Phản hồi không hợp lệ từ server.")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


        
def fetch_query_history():
    url = f"{FLASK_API_URL}/api/get_query_history/{current_user_id}"  # URL để lấy lịch sử truy vấn
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Giả s API trả về danh sách các truy vấn
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
        'created_at': datetime.now().isoformat()  # Lưu thời gian hiện tại theo định dng ISO
    }

    response = requests.post(url, json=payload)

    if response.status_code == 201:
        print('Query saved successfully!')
    else:
        print(f'Failed to save query: {response.text}')
            

def show_assistant_interface():
    global text_widget, mic_btn, mic_image, mic_active_image
    # Kiểm tra nếu giao diện trợ lý ảo đã được hiển thị
    if assistant_frame.winfo_ismapped():
        return  # Không làm gì nếu giao diện đã hiển thị

    # Định nghĩa màu sắc và tạo khung giao diện trợ lý ảo
    colors = {
        'bg': '#ffffff',
        'text': '#333333',
        'title': '#1a73e8',
        'ask_btn': '#1a73e8',
        'send_btn': '#34a853',
        'clear_btn': '#ea4335',
        'history_btn': '#fbbc05'
    }

    # Hiển thị giao diện trợ lý ảo
    assistant_frame.pack(fill=tk.BOTH, expand=True)
    assistant_frame.configure(bg=colors['bg'])

    # Title "Virtual Assistant"
    title_frame = tk.Frame(assistant_frame, bg=colors['bg'])
    title_frame.pack(fill=tk.X, padx=20, pady=10)
    
    title_label = tk.Label(
        title_frame,
        text="Virtual Assistant",
        font=("Helvetica", 16, "bold"),
        bg=colors['bg'],
        fg=colors['title']
    )
    title_label.pack(side=tk.LEFT)

    # Main content area
    content_frame = tk.Frame(assistant_frame, bg=colors['bg'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20)

    # Left sidebar for avatar
    sidebar_frame = tk.Frame(content_frame, bg=colors['bg'], width=150)
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
    sidebar_frame.pack_propagate(False)

    try:
        # Load avatar
        image_path = "image/assitant.png"
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        avatar_label = tk.Label(sidebar_frame, image=photo, bg=colors['bg'])
        avatar_label.image = photo
        avatar_label.pack(pady=10)

        # AI Assistant label
        assistant_label = tk.Label(
            sidebar_frame,
            text="AI Assistant",
            font=("Helvetica", 12, "bold"),
            bg=colors['bg'],
            fg=colors['title']
        )
        assistant_label.pack()

    except Exception as e:
        print(f"Error loading avatar: {e}")

    # Chat area
    chat_frame = tk.Frame(content_frame, bg=colors['bg'])
    chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Text display area
    text_widget = tk.Text(
        chat_frame,
        font=('Helvetica', 10),
        bg=colors['bg'],
        fg=colors['text'],
        relief="flat",
        wrap=tk.WORD
    )
    text_widget.pack(fill=tk.BOTH, expand=True)
    
    # Add scrollbar
    scrollbar = tk.Scrollbar(text_widget)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_widget.configure(yscrollcommand=scrollbar.set)
    scrollbar.configure(command=text_widget.yview)

    # Input area frame
    input_frame = tk.Frame(chat_frame, bg=colors['bg'])
    input_frame.pack(fill=tk.X, pady=10)

    # Text entry for chat
    entry_chat = tk.Entry(
        input_frame, 
        font=('Helvetica', 11), 
        bg='#f8f9fa', 
        relief="flat"
    )
    entry_chat.pack(fill=tk.X, pady=(0, 10), ipady=8)

    # Buttons frame
    button_frame = tk.Frame(input_frame, bg=colors['bg'])
    button_frame.pack(fill=tk.X)

    # Button style
    button_style = {
        'font': ('Helvetica', 10, 'bold'),
        'relief': 'flat',
        'pady': 8,
        'padx': 20,
        'cursor': 'hand2'
    }

    # Microphone button
    mic_image = Image.open("mic.png").resize((30, 30), Image.Resampling.LANCZOS)  # Thay đổi kích thước
    mic_image = ImageTk.PhotoImage(mic_image)

    mic_active_image = Image.open("mic_active.png").resize((30, 30), Image.Resampling.LANCZOS)  # Thay đổi kích thước
    mic_active_image = ImageTk.PhotoImage(mic_active_image)

    mic_btn = tk.Button(
        button_frame,
        image=mic_image,
        command=toggle_listening,
        relief="flat"
    )
    mic_btn.pack(side=tk.LEFT, padx=5)

    # Clear button
    clear_btn = tk.Button(
        button_frame,
        text="Clear",
        bg=colors['clear_btn'],
        fg='white',
        command=lambda: delete_text(text_widget),
        **button_style
    )
    clear_btn.pack(side=tk.LEFT, padx=5)

    # History button
    history_btn = tk.Button(
        button_frame,
        text="History",
        bg=colors['history_btn'],
        fg='white',
        command=lambda: show_query_history(text_widget, button_frame),
        **button_style
    )
    history_btn.pack(side=tk.LEFT, padx=5)

    # Initial message
    text_widget.tag_configure("greeting", font=("Helvetica", 11))
    text_widget.insert(tk.END, "Xin chào! Tôi có thể giúp gì cho bạn?\n", "greeting")
    text_widget.see(tk.END)

    # Configure text widget for virtual assistant
    set_text_widget(text_widget)

    # Bind Enter key to send message
    entry_chat.bind("<Return>", lambda e: send_message_in_thread(entry_chat.get(), text_widget))
    
def send_message_in_thread(user_message, text_widget):
    threading.Thread(target=send_message, args=(user_message, text_widget), daemon=True).start()

def send_message(user_message, text_widget):
    if user_message:
        # Enable text widget nếu đang disable
        text_widget.config(state='normal')
        
        # Hiển thị văn bản nhận diện từ giọng nói lên giao diện
        text_widget.insert(tk.END, f"Bạn: {user_message}\n")
        text_widget.see(tk.END)
        
        # Lấy phản hồi từ trợ lý ảo
        response = get_response(user_message)

        if response:
            # Hiển thị phản hồi của bot lên giao diện
            text_widget.insert(tk.END, f"Bot: {response}\n")
            text_widget.see(tk.END)
            # Lưu phản hồi của bot vào cơ sở dữ liệu
            if current_user_id:  # Chỉ lưu khi đã đăng nhập
                save_query(current_user_id, user_message, response)
        else:
            speak("Bot không thể trả lời câu hỏi này.")
            text_widget.insert(tk.END, "Bot không thể trả lời câu hỏi này.\n")
            text_widget.see(tk.END)
            
        # Xa nội dung trong entry sau khi gửi
        entry_email.delete(0, tk.END)
            
def ask(text_widget):
    global is_listening
    try:
        user_speech = get_text()  # Nhận diện giọng nói
        if user_speech:
            send_message(user_speech, text_widget)
    finally:
        is_listening = False  # Đảm bảo reset trạng thái khi kết thúc
    
def delete_text(text_widget):
    # Xóa toàn bộ nội dung trong text_widget
    text_widget.delete("1.0", tk.END)
    # Thêm lại tin nhắn chào mừng
    text_widget.insert(tk.END, "Xin chào! Tôi có thể giúp gì cho bạn?\n", "greeting")
    text_widget.see(tk.END)

def toggle_listening():
    """Hàm để bật/tắt chế độ lắng nghe giọng nói"""
    global is_listening, text_widget, mic_btn
    
    if not is_listening:
        is_listening = True
        mic_btn.config(image=mic_active_image)  # Thay đổi hình ảnh khi mic hoạt động
        threading.Thread(target=lambda: listen_to_user(text_widget), daemon=True).start()
    else:
        is_listening = False
        mic_btn.config(image=mic_image)  # Thay đổi hình ảnh khi mic không hoạt động

def listen_to_user(text_widget):
    global is_listening
    while is_listening:  # Kiểm tra trạng thái lắng nghe
        user_speech = get_text()  # Nhận diện giọng nói
        if user_speech:
            send_message(user_speech, text_widget)
            break  # Thoát vòng lặp sau khi gửi tin nhắn
    is_listening = False  # Đảm bảo reset trạng thái khi kết thúc
    mic_btn.config(image=mic_image)  # Reset hình ảnh mic

def show_query_history(text_widget, button_frame):
    # Xóa nội dung hiện tại trong text_widget
    text_widget.delete("1.0", tk.END)
    
    # Kiểm tra xem người dùng đã đăng nhập chưa
    if not current_user_id:
        text_widget.insert(tk.END, "Vui lòng đăng nhập để xem lịch sử!\n")
        return
        
    # Xóa nút Back cũ nếu có
    for widget in button_frame.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget('text') == 'Back':
            widget.destroy()
        
    history = fetch_query_history()
    
    if history:
        text_widget.insert(tk.END, "=== LỊCH SỬ CHAT ===\n\n")
        reversed_history = history[::-1]  # Đảo ngược list để hiển thị mới nhất trước
        for query in reversed_history:
            text_widget.insert(tk.END, f"Thời gian: {query['created_at']}\n")
            text_widget.insert(tk.END, f"Câu hỏi: {query['question']}\n")
            text_widget.insert(tk.END, f"Trả lời: {query['answer']}\n")
            text_widget.insert(tk.END, "------------------------\n")
    else:
        text_widget.insert(tk.END, "Không có lịch sử truy vấn.\n")
    
    # Thêm nút Back mới
    back_btn = tk.Button(
        button_frame,
        text="Back",
        bg="#4CAF50",
        fg='white',
        command=lambda: restore_chat(text_widget, back_btn),
        font=('Helvetica', 10, 'bold'),
        relief='flat',
        pady=8,
        padx=20,
        cursor='hand2'
    )
    back_btn.pack(side=tk.LEFT, padx=5)
    
    text_widget.see(tk.END)

def restore_chat(text_widget, back_btn):
    # Xóa nội dung hiện tại
    text_widget.delete("1.0", tk.END)
    
    # Thêm lại tin nhắn chào mừng
    text_widget.insert(tk.END, "Xin chào! Tôi có thể giúp gì cho bạn?\n", "greeting")
    
    # Xóa nút Back
    back_btn.destroy()
    
    # Enable lại các chức năng chat
    entry_email.config(state='normal')
    text_widget.config(state='normal')

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

# Thêm các biến global mới
def show_register_form():
    # Clear the current login frame
    login_frame.destroy()
    
    # Create a new register frame
    login_frame = tk.Frame(right_frame, bg="white")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    sign_up_label = tk.Label(
        login_frame,
        text="Sign up",
        font=("Helvetica", 24, "bold"),
        bg="white",
        fg="#1a73e8"
    )
    sign_up_label.pack(anchor="w", pady=(0, 20))
    
    # Full Name field
    full_name_label = tk.Label(
        login_frame, 
        text="Full Name", 
        font=("Helvetica", 10), 
        bg="white", 
        fg="#666"
    )
    full_name_label.pack(anchor="w")
    
    entry_full_name = tk.Entry(
        login_frame,
        font=("Helvetica", 12),
        bg="white",
        fg="#333",
        relief="solid",
        bd=1
    )
    entry_full_name.pack(fill="x", pady=(5, 15))
    entry_full_name.configure(highlightthickness=1, highlightcolor="#1a73e8")

    
    # Username field
    username_label = tk.Label(
        login_frame, 
        text="Email", 
        font=("Helvetica", 10), 
        bg="white", 
        fg="#666"
    )
    username_label.pack(anchor="w")
    
    entry_email = tk.Entry(
        login_frame,
        font=("Helvetica", 12),
        bg="white",
        fg="#333",
        relief="solid",
        bd=1
    )
    entry_email.pack(fill="x", pady=(5, 15))
    entry_email.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
    # Password field
    password_label = tk.Label(
        login_frame,
        text="Password",
        font=("Helvetica", 10),
        bg="white",
        fg="#666"
    )
    password_label.pack(anchor="w")
    
    entry_password = tk.Entry(
        login_frame,
        font=("Helvetica", 12),
        bg="white",
        fg="#333",
        relief="solid",
        bd=1,
        show="•"
    )
    entry_password.pack(fill="x", pady=(5, 15))
    entry_password.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
    # Confirm Password field
    confirm_password_label = tk.Label(
        login_frame,
        text="Confirm Password",
        font=("Helvetica", 10),
        bg="white",
        fg="#666"
    )
    confirm_password_label.pack(anchor="w")
    
    entry_confirm = tk.Entry(
        login_frame,
        font=("Helvetica", 12),
        bg="white",
        fg="#333",
        relief="solid",
        bd=1,
        show="•"
    )
    entry_confirm.pack(fill="x", pady=(5, 20))
    entry_confirm.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
    # Register button
    register_btn = tk.Button(
        login_frame,
        text="Sign up",
        command=lambda: register_user(
            entry_email,        # Truyền đối tượng Entry
            entry_password,     # Truyền đối tượng Entry
            entry_confirm,      # Truyền đối tượng Entry
            entry_full_name     # Truyền đối tượng Entry
        ),
        bg="#1a73e8",
        fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        padx=20,
        pady=8,
        width=20
    )
    register_btn.pack(pady=(10, 0))
    
    # Login link
    login_link_frame = tk.Frame(login_frame, bg="white")
    login_link_frame.pack(pady=(5, 0))
    
    login_label = tk.Label(
        login_link_frame,
        text="Already have an account?",
        font=("Helvetica", 10),
        bg="white",
        fg="#666"
    )
    login_label.pack(side=tk.LEFT, padx=(0, 5))
    
    login_link = tk.Button(
        login_link_frame,
        text="Sign in",
        command=show_login_form,
        font=("Helvetica", 10, "bold"),
        fg="#1a73e8",
        bg="white",
        bd=0,
        relief="flat",
        cursor="hand2"
    )
    login_link.pack(side=tk.LEFT)
    
    # Hover effects
    def on_enter(e):
        e.widget['background'] = '#1557b0'

    def on_leave(e):
        e.widget['background'] = '#1a73e8'
    
    def on_link_enter(e):
        e.widget['fg'] = '#1557b0'

    def on_link_leave(e):
        e.widget['fg'] = '#1a73e8'

    register_btn.bind("<Enter>", on_enter)
    register_btn.bind("<Leave>", on_leave)
    login_link.bind("<Enter>", on_link_enter)
    login_link.bind("<Leave>", on_link_leave)
    
    entry_email.focus()

def show_login_form():
    global entry_email, entry_password, login_frame
    
    # Xóa register frame hiện tại
    login_frame.destroy()
    
    # Tạo login frame mới
    login_frame = tk.Frame(right_frame, bg="white")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    sign_in_label = tk.Label(
        login_frame,
        text="Sign in",
        font=("Helvetica", 24, "bold"),
        bg="white",
        fg="#1a73e8"
    )
    sign_in_label.pack(anchor="w", pady=(0, 20))
    
    
    entry_email = tk.Entry(login_frame, font=("Helvetica", 12), bg="white", fg="#333", relief="solid", bd=1)
    entry_email.pack(fill="x", pady=(5, 15))
    entry_email.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
    entry_full_name = tk.Entry(login_frame, font=("Helvetica", 12), bg="white", fg="#333", relief="solid", bd=1)
    entry_full_name.pack(fill="x", pady=(5, 15))
    entry_full_name.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
    password_label = tk.Label(login_frame, text="Password", font=("Helvetica", 10), bg="white", fg="#666")
    password_label.pack(anchor="w")
    
    entry_password = tk.Entry(login_frame, font=("Helvetica", 12), bg="white", fg="#333", relief="solid", bd=1, show="•")
    entry_password.pack(fill="x", pady=(5, 20))
    entry_password.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
    login_btn = tk.Button(
        login_frame,
        text="Sign in",
        command=login,
        bg="#1a73e8",
        fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        padx=20,
        pady=8,
        width=20
    )
    login_btn.pack(pady=(0, 10))
    
    register_frame = tk.Frame(login_frame, bg="white")
    register_frame.pack(pady=(5, 0))
    
    register_label = tk.Label(
        register_frame,
        text="Don't have an account?",
        font=("Helvetica", 10),
        bg="white",
        fg="#666"
    )
    register_label.pack(side=tk.LEFT, padx=(0, 5))
    
    register_btn = tk.Button(
        register_frame,
        text="Sign up",
        command=show_register_form,
        font=("Helvetica", 10, "bold"),
        fg="#1a73e8",
        bg="white",
        bd=0,
        relief="flat",
        cursor="hand2"
    )
    register_btn.pack(side=tk.LEFT)
    
    def on_enter(e):
        e.widget['background'] = '#1557b0'

    def on_leave(e):
        e.widget['background'] = '#1a73e8'

    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)
    
    entry_email.focus()

def register_user(email_entry, password_entry, confirm_entry, full_name_entry):
    # In ra để debug
    print(f"Debug - Email Entry: {email_entry}, Value: {email_entry.get()}")
    print(f"Debug - Password Entry: {password_entry}, Value: {password_entry.get()}")
    print(f"Debug - Full Name Entry: {full_name_entry}, Value: {full_name_entry.get()}")
    
    # Lấy giá trị từ các entry
    email = email_entry.get()
    password = password_entry.get()
    confirm = confirm_entry.get()
    full_name = full_name_entry.get()
    
    if not email or not password or not confirm or not full_name:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return
        
    if password != confirm:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
        return
    
    try:
        # Đảm bảo gi đúng format JSON
        data = {
            "email": email, 
            "password": password,
            "full_name": full_name
        }
        print(f"Debug - Sending data: {data}")  # In ra data trước khi gửi
        
        response = requests.post(f"{FLASK_API_URL}/register", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Thành công", "Đăng ký thành công, vui lòng xác nhận email để đăng nhập!")
            show_login_form()  # Chuyển về form đăng nhập
        else:
            messagebox.showerror("Lỗi", response.json().get("error", "Có lỗi xảy ra!"))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def create_gui():
    global root, entry_email, entry_password, login_frame, main_container, assistant_frame, right_frame

    root = tk.Tk()
    root.title("Virtual Assistant Login")
    window_width, window_height = 900, 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.configure(bg="white")
    
    # Main container cho phần đăng nhập
    main_container = tk.Frame(root, bg="white")
    main_container.pack(fill=tk.BOTH, expand=True)

    # Left frame for image
    left_frame = tk.Frame(main_container, bg="#EBF3FE")
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    try:
        image_path = "login.png"
        image = Image.open(image_path)
        target_height = 400
        aspect_ratio = image.width / image.height
        target_width = int(target_height * aspect_ratio)
        image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(left_frame, image=photo, bg="#EBF3FE")
        image_label.image = photo
        image_label.place(relx=0.5, rely=0.5, anchor="center")
        
    except Exception as e:
        error_label = tk.Label(left_frame, text="Illustration not found", bg="#EBF3FE", fg="#666")
        error_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Right frame for forms
    right_frame = tk.Frame(main_container, bg="white", padx=40)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Login frame
    login_frame = tk.Frame(right_frame, bg="white")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")
    
    def show_login_form():
        # Clear current frame
        for widget in login_frame.winfo_children():
            widget.destroy()

        # Sign in text
        sign_in_label = tk.Label(
            login_frame,
            text="Sign in",
            font=("Helvetica", 24, "bold"),
            bg="white",
            fg="#1a73e8"
        )
        sign_in_label.pack(anchor="w", pady=(0, 20))
        
        
        # Email
        email_label = tk.Label(
            login_frame,
            text="Email",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        email_label.pack(anchor="w")
        
        global entry_email
        entry_email = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1
        )
        entry_email.pack(fill="x", pady=(5, 15))
        entry_email.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
        # Password
        password_label = tk.Label(
            login_frame,
            text="Password",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        password_label.pack(anchor="w")
        
        global entry_password
        entry_password = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1,
            show="•"
        )
        entry_password.pack(fill="x", pady=(5, 20))
        entry_password.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
        # Login button
        login_btn = tk.Button(
            login_frame,
            text="Sign in",
            command=login,
            bg="#1a73e8",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            width=20
        )
        login_btn.pack(pady=(0, 10))
        
        # Register section
        register_frame = tk.Frame(login_frame, bg="white")
        register_frame.pack(pady=(5, 0))
        
        register_label = tk.Label(
            register_frame,
            text="Don't have an account?",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        register_label.pack(side=tk.LEFT, padx=(0, 5))
        
        register_btn = tk.Button(
            register_frame,
            text="Sign up",
            command=show_register_form,
            font=("Helvetica", 10, "bold"),
            fg="#1a73e8",
            bg="white",
            bd=0,
            relief="flat",
            cursor="hand2"
        )
        register_btn.pack(side=tk.LEFT)
        
        # Hover effects
        def on_enter(e):
            e.widget['background'] = '#1557b0'

        def on_leave(e):
            e.widget['background'] = '#1a73e8'
            
        def on_register_enter(e):
            e.widget['fg'] = '#1557b0'

        def on_register_leave(e):
            e.widget['fg'] = '#1a73e8'

        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)
        register_btn.bind("<Enter>", on_register_enter)
        register_btn.bind("<Leave>", on_register_leave)
        
        # Focus on username
        entry_email.focus()

    def show_register_form():
        # Clear current frame
        for widget in login_frame.winfo_children():
            widget.destroy()
            
        # Sign up text
        sign_up_label = tk.Label(
            login_frame,
            text="Sign up",
            font=("Helvetica", 24, "bold"),
            bg="white",
            fg="#1a73e8"
        )
        sign_up_label.pack(anchor="w", pady=(0, 20))
        
        # Full Name field
        full_name_label = tk.Label(
            login_frame, 
            text="Full Name", 
            font=("Helvetica", 10), 
            bg="white", 
            fg="#666"
        )
        full_name_label.pack(anchor="w")
        
        entry_full_name = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1
        )
        entry_full_name.pack(fill="x", pady=(5, 15))
        entry_full_name.configure(highlightthickness=1, highlightcolor="#1a73e8")

        # Email field
        email_label = tk.Label(
            login_frame, 
            text="Email", 
            font=("Helvetica", 10), 
            bg="white", 
            fg="#666"
        )
        email_label.pack(anchor="w")
        
        entry_email = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1
        )
        entry_email.pack(fill="x", pady=(5, 15))
        entry_email.configure(highlightthickness=1, highlightcolor="#1a73e8")
        

        
        # Password field
        password_label = tk.Label(
            login_frame,
            text="Password",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        password_label.pack(anchor="w")
        
        entry_password = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1,
            show="•"
        )
        entry_password.pack(fill="x", pady=(5, 15))
        entry_password.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
        # Confirm Password field
        confirm_password_label = tk.Label(
            login_frame,
            text="Confirm Password",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        confirm_password_label.pack(anchor="w")
        
        entry_confirm = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1,
            show="•"
        )
        entry_confirm.pack(fill="x", pady=(5, 20))
        entry_confirm.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
        # Register button
        register_btn = tk.Button(
            login_frame,
            text="Sign up",
            command=lambda: register_user(
                entry_email,        # Truyền đối tượng Entry
                entry_password,     # Truyền đối tượng Entry
                entry_confirm,      # Truyền đối tượng Entry
                entry_full_name     # Truyền đối tượng Entry
            ),
            bg="#1a73e8",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            width=20
        )
        register_btn.pack(pady=(10, 0))
        
        # Login section
        login_frame_link = tk.Frame(login_frame, bg="white")
        login_frame_link.pack(pady=(5, 0))
        
        login_label = tk.Label(
            login_frame_link,
            text="Already have an account?",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        login_label.pack(side=tk.LEFT, padx=(0, 5))
        
        login_btn = tk.Button(
            login_frame_link,
            text="Sign in",
            command=show_login_form,
            font=("Helvetica", 10, "bold"),
            fg="#1a73e8",
            bg="white",
            bd=0,
            relief="flat",
            cursor="hand2"
        )
        login_btn.pack(side=tk.LEFT)
        
        # Hover effects
        def on_enter(e):
            e.widget['background'] = '#1557b0'

        def on_leave(e):
            e.widget['background'] = '#1a73e8'
            
        def on_login_enter(e):
            e.widget['fg'] = '#1557b0'

        def on_login_leave(e):
            e.widget['fg'] = '#1a73e8'

        register_btn.bind("<Enter>", on_enter)
        register_btn.bind("<Leave>", on_leave)
        login_btn.bind("<Enter>", on_login_enter)
        login_btn.bind("<Leave>", on_login_leave)
        
        # Focus on username
        entry_email.focus()
    
    # Assistant frame
    assistant_frame = tk.Frame(root, bg="#e0e0e0")
    
    # Show initial login form
    show_login_form()
    
    # Bind Enter key
    def on_enter_key(event):
        if login_frame.winfo_children()[0]['text'] == "Sign in":
            login()
    
    root.bind('<Return>', on_enter_key)
    
    # Thêm protocol xử lý sự kiện đóng cửa sổ
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()
