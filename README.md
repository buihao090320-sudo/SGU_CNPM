# Translation Service

Service con trong kiến trúc microservices — nhận văn bản, trả về bản dịch sang ngôn ngữ đích.

## Chạy ở local (không cần Docker)

```bash
cd translation-service
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Mở http://localhost:8000/docs để thấy Swagger UI, test thử endpoint `/translate` trực tiếp trên trình duyệt.

## Chạy test

```bash
pytest -v
```

## Chạy bằng Docker

```bash
docker build -t translation-service .
docker run -p 8000:8000 translation-service
```

Sau đó gọi thử:

```bash
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Xin chào", "target_lang": "en", "source_lang": "vi"}'
```

## Cấu trúc

- `main.py` — logic chính (FastAPI app)
- `test_main.py` — unit test (dùng cho CI)
- `Dockerfile` — đóng gói container
- `requirements.txt` — thư viện cần cài

## Việc cần làm tiếp

- [ ] Kết nối RabbitMQ để nhận job dịch dạng bất đồng bộ (thay vì chỉ REST đồng bộ)
- [ ] Thêm logging tập trung (VD: ghi log ra file/ELK)
- [ ] Thêm giới hạn rate limit nếu gọi API dịch bên ngoài nhiều
- [ ] Viết thêm integration test giữa Gateway ↔ Translation Service
