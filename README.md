# Quận 1 Audio Guide — Ứng dụng thuyết minh du lịch Quận 1

Đồ án môn **Công nghệ Phần mềm** — Trường Đại học Sài Gòn (SGU).

Ứng dụng thuyết minh du lịch đa ngôn ngữ (Việt / Anh / Pháp / Nhật) cho **Quận 1, TP. Hồ Chí Minh**. Người dùng xem địa điểm trên bản đồ, lập hành trình đi bộ tối ưu từ vị trí GPS và nghe thuyết minh thủ công hoặc tự động khi đến gần từng điểm. Quản trị viên quản lý địa điểm, bài thuyết minh, ảnh, hành trình và tài khoản.

## Thành viên nhóm

| MSSV       | Họ tên             | Phụ trách                                                                                   |
| ---------- | ------------------ | ------------------------------------------------------------------------------------------- |
| 3124411077 | Bùi Nhật Hào       | Backend, cơ sở dữ liệu, bản đồ/GPS, hành trình, thuyết minh, tích hợp                       |
| 3124411146 | Trần Quốc Kiệt     | Giao diện đăng nhập/đăng ký, tài khoản, khám phá, chi tiết địa điểm, yêu thích, lịch sử     |
| 3124411153 | Tô Nguyễn Minh Long | Kiểm thử chức năng, ghi nhận lỗi, tài liệu cài đặt và kịch bản demo                         |

## Tính năng chính

**Người dùng**

- Đăng ký, đăng nhập (JWT access + refresh token, có quản lý phiên và giới hạn đăng nhập sai).
- Khám phá 15 địa điểm tiêu biểu của Quận 1: Dinh Độc Lập, Nhà thờ Đức Bà, Bưu điện Trung tâm, Chợ Bến Thành, Nhà hát TP, Phố đi bộ Nguyễn Huệ, Bitexco, Thảo Cầm Viên, Chùa Ngọc Hoàng…
- Bản đồ luôn hiển thị ranh giới Quận 1 (OpenStreetMap), vị trí GPS và các điểm dừng.
- **Hành trình tối ưu**: chọn số điểm muốn đi, app tính thứ tự đi bộ ngắn nhất bằng quy hoạch động Held–Karp (≤16 điểm), ước tính quãng đường/thời gian và mở chỉ đường trên Google Maps.
- **Thuyết minh tự động theo hành trình**: lời giới thiệu, xác nhận đã đến từng điểm, lời dẫn sang điểm kế tiếp và lời kết — bằng 4 ngôn ngữ, đọc bằng giọng TTS trên thiết bị.
- **AutoGuide theo GPS**: tự phát thuyết minh khi đến gần điểm (GPS mới ≤60 s, sai số ≤50 m).
- Ảnh kể chuyện (3 ảnh Wikimedia Commons / địa điểm, có ghi tác giả và giấy phép).
- Yêu thích, lịch sử nghe, đánh giá; hiển thị đánh giá Google Maps (khi có API key).

**Quản trị viên**

- Quản lý địa điểm (nháp / xuất bản / lưu trữ), bài thuyết minh theo ngôn ngữ, ảnh và nguồn ảnh.
- Quản lý hành trình, tài khoản và vai trò, xem thống kê phát, nhật ký thao tác và cấu hình hệ thống.
- Nhập dữ liệu từ OpenStreetMap / danh mục địa điểm TP.HCM.

## Công nghệ

| Thành phần | Công nghệ                                                                                 |
| ---------- | ----------------------------------------------------------------------------------------- |
| Frontend   | Expo SDK 58, React Native 0.88, React 19, TypeScript, Expo Router, Leaflet / react-native-maps, expo-speech, expo-location |
| Backend    | Python 3.13, FastAPI, SQLAlchemy 2, Alembic, PyJWT, pwdlib (Argon2)                        |
| CSDL       | PostgreSQL (SQLite cho kiểm thử E2E)                                                       |
| Kiểm thử   | pytest, Node test runner, Playwright                                                       |
| Triển khai | Docker, Render (API), Cloudflare Workers (Expo Web), Cloudflare R2 (ảnh)                  |

## Cấu trúc thư mục

```text
.
├── backend/                  API FastAPI
│   ├── app/
│   │   ├── models/           Mô hình SQLAlchemy (user, place, review, history, …)
│   │   ├── routers/          API: auth, users, places, journeys, favorites, history,
│   │   │                     reviews, guide-content, audio-sessions, osm, admin, media
│   │   ├── schemas/          Pydantic schema
│   │   ├── services/         Nghiệp vụ
│   │   └── data/             Ranh giới & danh mục Quận 1, ảnh đóng gói sẵn
│   ├── alembic/versions/     Migration 0001 → 0008
│   ├── scripts/              Công cụ dựng dữ liệu demo, kiểm tra, khởi động server
│   ├── tests/                Kiểm thử pytest
│   ├── DEPLOYMENT.md         Hướng dẫn triển khai
│   └── Dockerfile
├── multilingual-guide/       Ứng dụng Expo (Web / Android / iOS)
│   ├── app/                  Màn hình (Expo Router): tabs, login, register, place/[id],
│   │                         journeys, history, account, admin
│   ├── src/                  components, services, context, hooks, admin, theme, data
│   └── tests/                Unit test (node --test) và E2E (Playwright)
├── scripts/                  prepare_handoff.py, check_docs.py
├── render.yaml               Mẫu cấu hình Render cho backend
└── start-app.cmd             Chạy nhanh backend + frontend trên Windows
```

## Yêu cầu môi trường

- Python **3.13**
- Node.js **≥ 22.13.1**
- PostgreSQL (tạo một database phát triển riêng)
- Expo Go (SDK 58) nếu chạy trên điện thoại thật

## Cài đặt và chạy

Các lệnh dưới đây dùng PowerShell trên Windows. Trên macOS/Linux thay `npm.cmd` bằng `npm` và `.\.venv\Scripts\python.exe` bằng `.venv/bin/python`.

### 1. Clone

```powershell
git clone https://github.com/buihao090320-sudo/SGU_CNPM.git
cd SGU_CNPM
```

### 2. Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Sửa `backend/.env`:

- `DATABASE_URL` — chuỗi kết nối PostgreSQL
- `SECRET_KEY` — chuỗi ngẫu nhiên ≥ 32 ký tự
- `ALLOWED_ORIGINS` — origin của frontend (ví dụ `http://localhost:8081`)
- `GOOGLE_MAPS_API_KEY` *(tùy chọn)* — để hiện đánh giá Google Maps

Tạo bảng và chạy server:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Tài liệu API (Swagger): <http://127.0.0.1:8000/docs>
- Kiểm tra sẵn sàng: <http://127.0.0.1:8000/health/ready>

### 3. Dữ liệu demo (database mới, trống)

```powershell
.\.venv\Scripts\python.exe -m scripts.bootstrap_reviewed_demo --apply
.\.venv\Scripts\python.exe -m scripts.apply_district1_catalog --apply --backup <file.dump>
```

Lệnh không có `--apply` chỉ xem trước. `apply_district1_catalog` yêu cầu file sao lưu `pg_dump` trước khi ghi. **Không chạy các script dựng dữ liệu trên database thật.**

### 4. Frontend

Mở terminal khác:

```powershell
cd multilingual-guide
npm.cmd ci
Copy-Item .env.example .env
npm.cmd run web
```

Đặt `EXPO_PUBLIC_API_URL` trong `multilingual-guide/.env` theo nền tảng:

| Nền tảng            | `EXPO_PUBLIC_API_URL`             | Lệnh chạy                                               |
| ------------------- | --------------------------------- | ------------------------------------------------------- |
| Web cùng máy        | `http://127.0.0.1:8000`           | `npm.cmd run web`                                       |
| Android emulator    | `http://10.0.2.2:8000`            | `npm.cmd run android`                                   |
| Điện thoại thật     | `http://<IPv4-LAN-máy-tính>:8000` | `npm.cmd run check:device` rồi `npm.cmd run dev:device` |

Điện thoại và máy tính phải cùng mạng Wi‑Fi. GPS trên trình duyệt cần `localhost` hoặc HTTPS; để dùng đầy đủ GPS và giọng đọc trên điện thoại, mở bằng Expo Go.

### Chạy nhanh (Windows)

Khi backend đã có `.venv`, `.env` và PostgreSQL đang chạy, nhấp đúp **`start-app.cmd`**. Script mở hai cửa sổ (FastAPI `:8000`, Expo Web `:8081`) và mở trình duyệt tại <http://localhost:8081>.

## Cấp quyền Admin

1. Đăng ký tài khoản trên app và lấy ID người dùng trong database.
2. Thêm ID vào `ADMIN_USER_IDS` trong `backend/.env`.
3. Khởi động lại backend và đăng nhập lại.

Người dùng không thể tự cấp quyền Admin qua API đăng ký.

## Kiểm thử

```powershell
# Backend
cd backend
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider

# Frontend
cd ..\multilingual-guide
npm.cmd run typecheck
npm.cmd run lint -- --no-cache
npm.cmd test
npm.cmd run test:e2e      # cần Chrome, cổng 8765/8099 trống
```

## Luồng demo

1. Admin tạo / duyệt địa điểm, bài thuyết minh và ảnh, sắp xếp hành trình.
2. Người dùng đăng ký → đăng nhập → **Khám phá** địa điểm Quận 1.
3. Mở **Bản đồ** → chọn số điểm → **Lập hành trình tối ưu**.
4. Bấm **Bắt đầu thuyết minh tự động**, xác nhận khi đến từng điểm để nghe thuyết minh.
5. Lưu địa điểm yêu thích, xem lại lịch sử nghe, gửi đánh giá.

## Quy trình làm việc nhóm

- Mỗi thành viên làm trên nhánh riêng (ví dụ `kiet/hoan-thien-giao-dien`, `long/kiem-thu-tai-lieu`), commit bằng tài khoản GitHub của mình và mở Pull Request vào `main`.
- Chỉ `git add` đúng các tệp đã sửa; mô tả rõ thay đổi, cách kiểm tra và kết quả trong PR.
- **Không** đưa lên GitHub: `.env`, mật khẩu/token, dữ liệu người dùng, bản sao lưu database, `uploads/`, `node_modules/`, `.venv/`.

## Nguồn dữ liệu và giấy phép

- Ranh giới Quận 1: OpenStreetMap relation 2587287 — © OpenStreetMap contributors, giấy phép ODbL.
- Ảnh địa điểm: Wikimedia Commons, ghi tác giả và giấy phép từng ảnh trong dữ liệu.
- Đánh giá Google Maps lấy qua Google Places API chính thức, có ghi nguồn; ứng dụng không cào dữ liệu Google Maps.
