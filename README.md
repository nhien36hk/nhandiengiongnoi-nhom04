# Ứng Dụng Trợ Lý Ảo


## Giới Thiệu

Ứng dụng Trợ lý Ảo này được xây dựng bằng Python và Flask cho backend, cùng với Flutter cho frontend, cho phép người dùng tương tác thông qua giọng nói và văn bản. Ứng dụng hỗ trợ đăng ký, đăng nhập, lưu lịch sử truy vấn và nhiều tính năng khác.

## Sơ Đồ Hệ Thống
### DESKTOP
![Untitled diagram-2024-11-28-114820](https://github.com/user-attachments/assets/3778306b-dbe9-4042-a00c-413b8f3c8c1c)
### MOBILE
![mermaid-diagram-2024-11-28-114853](https://github.com/user-attachments/assets/5ad6afa6-695b-4463-bcfc-1139399e575c)


## Tính Năng

- **Đăng Ký và Đăng Nhập**: Người dùng có thể tạo tài khoản và đăng nhập để sử dụng ứng dụng.
- **Trợ Lý Ảo**: Giao tiếp với trợ lý ảo thông qua giọng nói hoặc văn bản.
- **Lưu Lịch Sử Truy Vấn**: Lưu lại các câu hỏi và câu trả lời để tham khảo sau này.
- **Xác Thực Email**: Gửi email xác thực cho người dùng sau khi đăng ký.
- **Giao Diện Người Dùng**: Giao diện thân thiện và dễ sử dụng với Tkinter cho backend và Flutter cho frontend.

## Mô Hình AI

Ứng dụng Trợ lý Ảo sử dụng **Ollama Model gemma2:9b** để xử lý các phản hồi từ trợ lý ảo. Mô hình này giúp cải thiện độ chính xác và sự tự nhiên của các câu trả lời cho người dùng.

## Công Nghệ Sử Dụng

### Backend
- **Python**: Ngôn ngữ lập trình chính.
- **Flask**: Framework web cho Python.
- **Firebase**: Cơ sở dữ liệu và xác thực người dùng.
- **OpenAI API**: Sử dụng để tạo phản hồi từ trợ lý ảo.

### Frontend
- **Flutter**: Framework phát triển ứng dụng di động.
- **Dart**: Ngôn ngữ lập trình chính cho Flutter.
- **Speech to Text**: Thư viện để chuyển đổi giọng nói thành văn bản.
- **Text to Speech**: Thư viện để chuyển đổi văn bản thành giọng nói.

## Giao Diện Người Dùng

### Trang Đăng Nhập
![5](https://github.com/user-attachments/assets/7f20c280-5be3-4c3d-99e5-5e769d432775)
![Screenshot_1732790582](https://github.com/user-attachments/assets/6895aa81-d032-409c-b023-768b5fe76bcd)
![Screenshot_1732790336](https://github.com/user-attachments/assets/37415094-f312-47c4-bb95-d5b8e75d0e33)

### Trang Đăng Ký
![6](https://github.com/user-attachments/assets/86689a46-adaf-4f9b-b4e4-1d6ba869f15b)
![Screenshot_1732790573](https://github.com/user-attachments/assets/f43ef3c6-2201-4c8e-b294-22cf6d1366a6)

### Trang Trò Chuyện
![4](https://github.com/user-attachments/assets/9d9a983a-3ef2-4077-8f79-1dfa4865b116)
![Screenshot_1732790461](https://github.com/user-attachments/assets/5bd1b5e9-38bc-4c09-a29f-8d9dd63106e1)

### Trang Lịch Sử
![4](https://github.com/user-attachments/assets/c8779e81-abf9-47e1-a0fa-63248ffdb484)
![Screenshot_1732790421](https://github.com/user-attachments/assets/4c2608e4-7bf6-4d5c-bb5a-77aa7df4bb57)

### Trang Cá Nhân
![Screenshot_1732790416](https://github.com/user-attachments/assets/3bd4833e-1c27-47be-8d00-c2b1f492045f)


## Cài Đặt

### Yêu Cầu

- Python 3.x
- pip (trình quản lý gói Python)
- Flutter SDK

### Cài Đặt Các Gói Cần Thiết

#### Backend
1. Cài đặt các gói cần thiết cho Flask:
   ```bash
   pip install Flask firebase-admin requests
   ```

#### Frontend
1. Cài đặt Flutter và các gói cần thiết:
   ```bash
   flutter pub get
   ```

## Hướng Dẫn Sử Dụng

1. **Chạy Backend**:
   - Di chuyển đến thư mục chứa mã nguồn backend và chạy:
     ```bash
     python app.py
     ```

2. **Chạy Frontend**:
   - Di chuyển đến thư mục chứa mã nguồn Flutter và chạy:
     ```bash
     flutter run
     ```

## Liên Hệ

Nếu bạn có bất kỳ câu hỏi nào, vui lòng liên hệ với chúng tôi qua email: [your_email@example.com](mailto:your_email@example.com).

## Giấy Phép

Ứng dụng này được phát hành dưới Giấy phép MIT. Vui lòng tham khảo tệp LICENSE để biết thêm chi tiết.
