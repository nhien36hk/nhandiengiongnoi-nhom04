# Ứng Dụng Trợ Lý Ảo

![Logo](path/to/logo.png) <!-- Thay đổi đường dẫn đến logo của bạn -->

## Giới Thiệu

Ứng dụng Trợ lý Ảo này được xây dựng bằng Python và Flask cho backend, cùng với Flutter cho frontend, cho phép người dùng tương tác thông qua giọng nói và văn bản. Ứng dụng hỗ trợ đăng ký, đăng nhập, lưu lịch sử truy vấn và nhiều tính năng khác.

## Tính Năng

- **Đăng Ký và Đăng Nhập**: Người dùng có thể tạo tài khoản và đăng nhập để sử dụng ứng dụng.
- **Trợ Lý Ảo**: Giao tiếp với trợ lý ảo thông qua giọng nói hoặc văn bản.
- **Lưu Lịch Sử Truy Vấn**: Lưu lại các câu hỏi và câu trả lời để tham khảo sau này.
- **Xác Thực Email**: Gửi email xác thực cho người dùng sau khi đăng ký.
- **Giao Diện Người Dùng**: Giao diện thân thiện và dễ sử dụng với Tkinter cho backend và Flutter cho frontend.

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
