# FinAlly - Nền tảng Giao dịch AI

## Giới thiệu

FinAlly là một nền tảng giao dịch chứng khoán được hỗ trợ bởi AI, cho phép người dùng chat để thực hiện lệnh mua/bán cổ phiếu một cách tự nhiên bằng tiếng Việt hoặc tiếng Anh.

## Tính năng chính

- 🤖 Chat AI để phân tích và thực hiện lệnh giao dịch
- 📊 Theo dõi danh mục đầu tư và lịch sử giao dịch
- 💰 Tài khoản ảo với $10,000
- 📈 Giao diện chuyên nghiệp
- 🔄 Phân tích lệnh mua/bán tự động

## Yêu cầu hệ thống

- Windows 10/11
- Python 3.8+
- Node.js 16+
- CMake 3.16+
- Git

## Hướng dẫn cài đặt và chạy

### Bước 1: Cài đặt CMake

```powershell
winget install Kitware.CMake
```

### Bước 2: Cài đặt llama.cpp

```powershell
# Tạo thư mục cho llama
mkdir c:\BUU\llama-bin
cd c:\BUU\llama-bin

# Clone và build llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
mkdir build
cd build
cmake .. -DLLAMA_BUILD_SERVER=ON
cmake --build . --config Release
```

### Bước 3: Tải model TinyLlama

```powershell
# Tạo thư mục models
mkdir c:\BUU\models

# Tải model (có thể mất thời gian)
curl -L https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -o c:\BUU\models\tinyllama.gguf
```

### Bước 4: Cài đặt backend

```powershell
# Tạo virtual environment
python -m venv c:\BUU\venv
c:\BUU\venv\Scripts\activate

# Cài đặt dependencies
cd c:\BUU\project4\finally\backend
pip install -r requirements.txt
```

### Bước 5: Cài đặt frontend

```powershell
cd c:\BUU\project4\finally\frontend
npm install
```

### Bước 6: Khởi chạy các server

#### Terminal 1: Llama Server

```powershell
cd c:\BUU\llama-bin\llama.cpp\build\bin\Release
.\llama-server.exe -m c:\BUU\models\tinyllama.gguf --host 0.0.0.0 --port 8080
```

#### Terminal 2: Backend API

```powershell
cd c:\BUU\project4\finally\backend
$env:PYTHONPATH="src"
c:\BUU\venv\Scripts\python.exe -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

#### Terminal 3: Frontend

```powershell
cd c:\BUU\project4\finally\frontend
npm run dev
```

### Bước 7: Truy cập ứng dụng

Mở trình duyệt và truy cập: `http://localhost:3000`

## Cách sử dụng

1. **Chat với AI**: Gửi tin nhắn như "mua 10 AAPL" hoặc "bán 5 MSFT"
2. **Xem danh mục**: Kiểm tra số dư và cổ phiếu đang sở hữu
3. **Lịch sử giao dịch**: Xem các lệnh đã thực hiện

## Ví dụ lệnh giao dịch

- `mua 10 AAPL` - Mua 10 cổ phiếu Apple
- `bán 5 MSFT` - Bán 5 cổ phiếu Microsoft
- `mua cho tôi 20 META` - Mua 20 cổ phiếu Meta
- `bạn bán 15 NVDA` - Bán 15 cổ phiếu Nvidia

## Xử lý sự cố

### Lỗi "Failed to fetch"
- Kiểm tra backend có chạy trên port 8000
- Restart backend server

### Llama server không khởi động
- Kiểm tra đường dẫn model đúng
- Đảm bảo port 8080 không bị chiếm

### Frontend không load
- Kiểm tra npm install đã chạy
- Restart `npm run dev`

## Cấu trúc dự án

```
finally/
├── backend/          # API FastAPI
│   ├── src/
│   │   ├── api/      # Endpoints
│   │   ├── db/       # Database models
│   │   └── main.py   # App entry point
├── frontend/         # React/Next.js UI
│   ├── src/
│   │   ├── app/      # Pages
│   │   └── components/
└── db/               # SQLite database
```

## Phát triển thêm

- Thêm nhiều model AI lớn hơn cho phản hồi tốt hơn
- Tích hợp dữ liệu thị trường thực
- Thêm tính năng phân tích kỹ thuật
- Hỗ trợ nhiều ngôn ngữ

## Giấy phép

Dự án này dành cho mục đích học tập.