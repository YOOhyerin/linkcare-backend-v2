from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

from openai import OpenAI

from core.config import settings


@dataclass
class STTResult:
    text: str
    raw: Dict[str, Any]


class STTService:
    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def transcribe(
        self,
        *,
        audio_bytes: bytes,
        filename: str,
        content_type: Optional[str] = None,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        response_format: str = "json",
    ) -> STTResult:
        """
        audio/transcriptions 호출.
        - audio_bytes: 업로드된 파일의 bytes
        - filename: 원본 파일명 (multipart file 파라미터에 필요)
        """
        lang = language or settings.OPENAI_STT_LANGUAGE

        # OpenAI Python SDK는 file을 (filename, bytes, content_type) 형태로 전달 가능
        file_tuple = (filename, audio_bytes, content_type or "application/octet-stream")

        try:
            resp = self._client.audio.transcriptions.create(
                model=settings.OPENAI_STT_MODEL,
                file=file_tuple,
                language=lang,
                prompt=prompt,
                response_format="json",
            )
        except Exception as e:
            # 상위(router)에서 HTTPException으로 변환하는 방식도 가능
            raise RuntimeError(f"OpenAI transcription failed: {e}") from e

        # SDK 응답 타입이 dict-like 또는 pydantic일 수 있어 안전하게 처리
        text = getattr(resp, "text", None)
        if text is None:
            # 일부 response_format에서는 resp 자체가 문자열일 수 있음
            text = str(resp)

        raw = resp.model_dump() if hasattr(resp, "model_dump") else {"resp": str(resp)}
        return STTResult(text=text, raw=raw)
