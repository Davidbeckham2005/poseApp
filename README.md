# NIÊN LUẬN: HỆ THỐNG THEO DÕI TẬP LUYỆN THỂ CHẤT THỜI GIAN THỰC (POSEAPP)

Dự án ứng dụng công nghệ Computer Vision để hỗ trợ người dùng theo dõi và đếm số lần thực hiện các bài tập thể hình (Squat, Push-up, Plank) thông qua Webcam.

## 📌 Tổng quan dự án
Ứng dụng được xây dựng trên nền tảng Desktop giúp tối ưu hiệu năng xử lý hình ảnh, kết hợp giao diện hiện đại theo phong cách Gaming/Glassmorphism.

* **Tên dự án:** PoseApp - AI Fitness Tracker
* **Sinh viên thực hiện:** Đinh Hoàng Khâm
* **Mã số sinh viên:** B2303822
* **Giảng viên hướng dẫn:** 

## ✨ Tính năng chính
- [x] **Nhận diện tư thế (Pose Estimation):** Sử dụng MediaPipe để xác định các khớp xương trên cơ thể.
- [x] **Đếm số lần thực hiện (Rep Counter):** Tự động đếm Squats, Push-ups và tính thời gian Plank.
- [x] **Tính toán sức khỏe:** Theo dõi chỉ số BMI, lượng Calo tiêu thụ dựa trên cường độ tập luyện.
- [x] **Real-time Pipeline:** Truyền tải dữ liệu khung hình qua WebSockets để đảm bảo độ trễ thấp nhất.
- [x] **Giao diện hiện đại:** Dashboard thiết kế với Tailwind CSS, hỗ trợ biểu đồ và hiệu ứng kính mờ (Glassmorphism).

## 🛠 Công nghệ sử dụng
### Frontend (Client)
* **Framework:** Vue 3 (Vite, Composition API)
* **State Management:** Pinia
* **Styling:** Tailwind CSS
* **Desktop Shell:** Tauri (Core viết bằng Rust)

### Backend (AI Processing)
* **Language:** Python
* **Framework:** FastAPI
* **AI/CV:** OpenCV, MediaPipe
* **Communication:** WebSockets, Multithreading

## 🚀 Cài đặt và Chạy ứng dụng

### 1. Yêu cầu hệ thống
- **Node.js** (v18 trở lên)
- **Rust toolchain** (Cài đặt qua [rustup.rs](https://rustup.rs/))
- **Python 3.9+** (Dành cho AI Backend)

### 2. Khởi chạy Backend Python
```bash
cd python
pip install -r requirements.txt
python main.py