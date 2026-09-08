"""
Unit test cho Translation Service.
Lưu ý: mock GoogleTranslator để test không phụ thuộc internet
(quan trọng vì GitHub Actions runner có thể không gọi được API dịch thật
mỗi lần chạy CI).
"""

from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_translate_empty_text_returns_400():
    response = client.post(
        "/translate", json={"text": "   ", "target_lang": "en"}
    )
    assert response.status_code == 400


@patch("main.GoogleTranslator.translate")
def test_translate_success(mock_translate):
    mock_translate.return_value = "Hello"
    response = client.post(
        "/translate",
        json={"text": "Xin chào", "target_lang": "en", "source_lang": "vi"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["translated_text"] == "Hello"
    assert data["target_lang"] == "en"
