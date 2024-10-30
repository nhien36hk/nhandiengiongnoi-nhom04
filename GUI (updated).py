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
    global current_user_id
    username = entry_username.get()
    password = entry_password.get()
    response = requests.post(f"{FLASK_API_URL}/login", json={"username": username, "password": password})
    
    if response.status_code == 200:
        current_user_id = response.json()["user_id"]
        messagebox.showinfo("Đăng nhập thành công", response.json()["message"])
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        
        # Ẩn toàn bộ khung đăng nhập và minh họa
        main_container.pack_forget()
        
        # Hiển thị giao diện trợ lý ảo
        show_assistant_interface()
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

    # Tiếp tục cấu hình các thành phần khác như title, content area, chat area, v.v.


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

    # Text entry
    entry1 = tk.Entry(
        input_frame,
        font=('Helvetica', 11),
        bg='#f8f9fa',
        relief="flat"
    )
    entry1.pack(fill=tk.X, pady=(0, 10), ipady=8)
    
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

    # Biến để theo dõi trạng thái mic
    is_listening = False
    
    # Tạo và cấu hình ảnh cho microphone
    try:
        # Tải ảnh mic (đảm bảo file tồn tại trong thư mục của bạn)
        mic_icon = Image.open("mic.png")  # Mic đang tắt
        mic_active_icon = Image.open("mic_active.png")  # Mic đang bật
        
        # Resize ảnh nếu cần
        icon_size = (30, 30)
        mic_icon = mic_icon.resize(icon_size, Image.Resampling.LANCZOS)
        mic_active_icon = mic_active_icon.resize(icon_size, Image.Resampling.LANCZOS)
        
        # Chuyển đổi sang PhotoImage
        mic_photo = ImageTk.PhotoImage(mic_icon)
        mic_active_photo = ImageTk.PhotoImage(mic_active_icon)
        
    except Exception as e:
        print(f"Error loading microphone icons: {e}")
        # Fallback nếu không tải được ảnh
        mic_photo = None
        mic_active_photo = None

    def toggle_listening():
        nonlocal is_listening
        is_listening = not is_listening
        
        if is_listening:
            # Bắt đầu lắng nghe
            mic_btn.configure(image=mic_active_photo) if mic_active_photo else mic_btn.configure(text="🎤 ON")
            threading.Thread(target=start_listening, args=(text_widget,), daemon=True).start()
        else:
            # Dừng lắng nghe
            mic_btn.configure(image=mic_photo) if mic_photo else mic_btn.configure(text="🎤")

    def start_listening(text_widget):
        while is_listening:
            user_speech = get_text()  # Nhận diện giọng nói
            if user_speech and is_listening:  # Kiểm tra lại trạng thái trước khi xử lý
                send_message(user_speech, text_widget)

    # Tạo nút microphone
    if mic_photo:
        mic_btn = tk.Button(
            button_frame,
            image=mic_photo,
            bg=colors['bg'],
            command=toggle_listening,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        # Lưu reference cho ảnh
        mic_btn.image = mic_photo
        mic_btn.active_image = mic_active_photo
    else:
        # Fallback nếu không có ảnh
        mic_btn = tk.Button(
            button_frame,
            text="🎤",
            bg=colors['bg'],
            command=toggle_listening,
            **button_style
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
        command=lambda: show_query_history(text_widget),
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
    entry1.bind("<Return>", lambda e: send_message_in_thread(entry1.get(), text_widget))
    
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

# Thêm các biến global mới
def show_register_form():
    global entry_username, entry_password, login_frame
    
    # Xóa login frame hiện tại
    login_frame.destroy()
    
    # Tạo register frame mới
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
    
    # Username field
    username_label = tk.Label(
        login_frame, 
        text="Username", 
        font=("Helvetica", 10), 
        bg="white", 
        fg="#666"
    )
    username_label.pack(anchor="w")
    
    entry_username = tk.Entry(
        login_frame,
        font=("Helvetica", 12),
        bg="white",
        fg="#333",
        relief="solid",
        bd=1
    )
    entry_username.pack(fill="x", pady=(5, 15))
    entry_username.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
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
        command=lambda: register_user(entry_username, entry_password, entry_confirm),
        bg="#1a73e8",
        fg="white",
        font=("Helvetica", 11, "bold"),
        relief="flat",
        padx=20,
        pady=8,
        width=20
    )
    register_btn.pack(pady=(0, 10))
    
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
    
    entry_username.focus()

def show_login_form():
    global entry_username, entry_password, login_frame
    
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
    
    username_label = tk.Label(login_frame, text="Username", font=("Helvetica", 10), bg="white", fg="#666")
    username_label.pack(anchor="w")
    
    entry_username = tk.Entry(login_frame, font=("Helvetica", 12), bg="white", fg="#333", relief="solid", bd=1)
    entry_username.pack(fill="x", pady=(5, 15))
    entry_username.configure(highlightthickness=1, highlightcolor="#1a73e8")
    
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
    
    entry_username.focus()

def register_user(username_entry, password_entry, confirm_entry):
    username = username_entry.get()
    password = password_entry.get()
    confirm = confirm_entry.get()
    
    if not username or not password or not confirm:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return
        
    if password != confirm:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
        return
    
    try:
        response = requests.post(f"{FLASK_API_URL}/register", json={"username": username, "password": password})
        if response.status_code == 201:
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            show_login_form()  # Chuyển về form đăng nhập
        else:
            messagebox.showerror("Lỗi", response.json().get("error", "Có lỗi xảy ra!"))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


def create_gui():
    global entry_username, entry_password, login_frame, main_container, assistant_frame, right_frame

    # Tạo cửa sổ chính
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
        
        # Username
        username_label = tk.Label(
            login_frame,
            text="Username",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        username_label.pack(anchor="w")
        
        global entry_username
        entry_username = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1
        )
        entry_username.pack(fill="x", pady=(5, 15))
        entry_username.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
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
        entry_username.focus()

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
        
        # Username
        username_label = tk.Label(
            login_frame,
            text="Username",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        username_label.pack(anchor="w")
        
        global entry_username
        entry_username = tk.Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            relief="solid",
            bd=1
        )
        entry_username.pack(fill="x", pady=(5, 15))
        entry_username.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
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
        entry_password.pack(fill="x", pady=(5, 15))
        entry_password.configure(highlightthickness=1, highlightcolor="#1a73e8")
        
        # Confirm Password
        confirm_label = tk.Label(
            login_frame,
            text="Confirm Password",
            font=("Helvetica", 10),
            bg="white",
            fg="#666"
        )
        confirm_label.pack(anchor="w")
        
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
            command=lambda: register_user(entry_username, entry_password, entry_confirm),
            bg="#1a73e8",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            padx=20,
            pady=8,
            width=20
        )
        register_btn.pack(pady=(0, 10))
        
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
        entry_username.focus()
    
    # Assistant frame
    assistant_frame = tk.Frame(root, bg="#e0e0e0")
    
    # Show initial login form
    show_login_form()
    
    # Bind Enter key
    def on_enter_key(event):
        if login_frame.winfo_children()[0]['text'] == "Sign in":
            login()
    
    root.bind('<Return>', on_enter_key)
    
    root.mainloop()

def register_user(username_entry, password_entry, confirm_entry):
    username = username_entry.get()
    password = password_entry.get()
    confirm = confirm_entry.get()
    
    if not username or not password or not confirm:
        messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
        return
        
    if password != confirm:
        messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
        return
    
    try:
        response = requests.post(f"{FLASK_API_URL}/register", json={"username": username, "password": password})
        if response.status_code == 201:
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            show_login_form()  # Chuyển về form đăng nhập
        else:
            messagebox.showerror("Lỗi", response.json().get("error", "Có lỗi xảy ra!"))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
