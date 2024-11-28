import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Kết nối với Firebase
cred = credentials.Certificate('study2024-6f1d0-firebase-adminsdk-dodle-f8076572ce.json')
firebase_admin.initialize_app(cred)

# Tạo đối tượng kết nối Firestore
db = firestore.client()

# Hàm đăng ký người dùng
def register_user(email, password, full_name):
    # Tạo tài khoản trong Firebase Auth
    user = auth.create_user(
        email=email,
        password=password
    )
    
    # Lưu thông tin người dùng vào Firestore
    user_ref = db.collection('users').document(user.uid)
    user_ref.set({
        'email': email,
        'name': full_name,
        'password': password
    })
    
    # Gửi email xác thực
    link = auth.generate_email_verification_link(email)
    send_verification_email(email, link)
    
    print("User registered successfully.")
    
def create_or_update_google_user(email, name, uid):
    try:
        user_ref = db.collection('users').document(uid)
        if user_ref.get().exists:  # Check if the user already exists
            return True, None  # User exists, return True
        
        user_ref.set({
            'email': email,
            'name': name,
            'uid': uid,
            'created_at': datetime.now()
        }, merge=True)
        return True, None
    except Exception as e:
        return False, str(e)

def send_verification_email(email, link):
    try:
        # Cấu hình thông tin email
        sender_email = 'kingofpro1410@gmail.com'
        sender_password = 'ypvc gccd fysu cqyp'  # Sử dụng mật khẩu ứng dụng
        subject = "Xác nhận email của bạn"
        body = f"Vui lòng nhấp vào liên kết sau để xác nhận email của bạn: {link}"

        # Tạo email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Kết nối tới server SMTP của Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        
        print(f"Verification email sent to {email}.")
    except Exception as e:
        print(f"Failed to send verification email: {e}")

# Hàm xác thực người dùng
def authenticate_user(email, password):
    if not email or not password:
        return {"error": "Email và mật khẩu không được để trống."}

    try:
        user = auth.get_user_by_email(email)
        if not user.email_verified:
            return {"error": "Email chưa được xác nhận. Vui lòng xác nhận email của bạn."}
        
        # Kiểm tra mật khẩu (giả sử bạn có cách để xác thực mật khẩu)
        user_ref = db.collection('users').document(user.uid).get()
        if user_ref.exists:
            user_data = user_ref.to_dict()
            if user_data['password'] == password:
                return {
                    "user_id": user.uid,
                    "email": email
                }
        return {"error": "Mật khẩu không chính xác."}
    except ValueError as e:
        return {"error": str(e)}
    except firebase_admin.exceptions.FirebaseError as e:
        return {"error": str(e)}
    return None


# Hàm lưu lịch sử truy vấn
def save_query_to_history(user_id, question, answer, created_at=None):
    # Kiểm tra nếu created_at là None, tạo mới datetime.now() nếu không có
    if created_at is None:
        created_at = datetime.now()

    # Nếu created_at là chuỗi (string), chuyển đổi nó thành datetime
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)

    # Lưu dữ liệu vào Firestore
    history_ref = db.collection('query_history').document()  # Tạo document mới với ID tự động
    history_ref.set({
        'user_id': user_id,
        'question': question,
        'answer': answer,
        'created_at': created_at.isoformat()  # Chuyển thời gian sang định dạng ISO
    })

    print("Query saved to history.")

def get_query_history(user_id):
    # Truy vấn lịch sử truy vấn của người dùng
    history_ref = db.collection('query_history').where('user_id', '==', user_id)
    history = []
    
    for doc in history_ref.stream():
        data = doc.to_dict()
        # Chuyển 'created_at' từ chuỗi thành datetime nếu cần
        created_at = datetime.fromisoformat(data['created_at'])  # Chuyển chuỗi ISO thành datetime
        
        history.append({
            'user_id': data['user_id'],
            'question': data['question'],
            'answer': data['answer'],
            'created_at': created_at  # Lưu dưới dạng datetime
        })
    
    return history

def is_valid_email(email):
    # Kiểm tra định dạng email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
