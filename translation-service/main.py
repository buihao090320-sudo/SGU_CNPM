"""
Translation Service
Nhiệm vụ: nhận văn bản + ngôn ngữ đích, trả về bản dịch.
Đây là service con trong kiến trúc microservices, được Gateway gọi qua REST.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deep_translator import GoogleTranslator

app = FastAPI(title="Translation Service", version="0.1.0")


class TranslateRequest(BaseModel):
    text: str
    target_lang: str  # ví dụ: "en", "vi", "ja", "ko"
    source_lang: str = "auto"


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str


@app.get("/health")
def health_check():
    """Dùng để service khác (hoặc CI/CD) kiểm tra service còn sống không."""
    return {"status": "ok", "service": "translation-service"}


@app.post("/translate", response_model=TranslateResponse)
def translate_text(payload: TranslateRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text không được để trống")

    try:
        result = GoogleTranslator(
            source=payload.source_lang,
            target=payload.target_lang,
        ).translate(payload.text)
    except Exception as e:
        # Trong thực tế nên log lỗi này ra hệ thống logging tập trung
        raise HTTPException(status_code=502, detail=f"Lỗi khi gọi engine dịch: {e}")

    return TranslateResponse(
        original_text=payload.text,
        translated_text=result,
        source_lang=payload.source_lang,
        target_lang=payload.target_lang,
    )
