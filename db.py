import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Kết nối với Firebase
cred = credentials.Certificate('study2024-6f1d0-firebase-adminsdk-dodle-6a27d5e27f.json')  # Thay 'path/to/your-firebase-adminsdk.json' bằng đường dẫn thực tế
firebase_admin.initialize_app(cred)

# Tạo đối tượng kết nối Firestore
db = firestore.client()

# Hàm đăng ký người dùng
def register_user(username, password):
    user_ref = db.collection('users').document(username)
    user_ref.set({
        'username': username,
        'password': password
    })
    print("User registered successfully.")

# Hàm xác thực người dùng
def authenticate_user(username, password):
    user_ref = db.collection('users').document(username).get()  # Lấy document dựa trên username
    if user_ref.exists:
        user_data = user_ref.to_dict()  # Lấy dữ liệu của người dùng
        if user_data['password'] == password:  # Kiểm tra mật khẩu
            return {
                "user_id": username,  # Dùng username làm user_id (ID người dùng)
                "username": username  # Trả lại username như thông tin người dùng
            }
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
