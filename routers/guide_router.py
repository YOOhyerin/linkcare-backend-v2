from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from services.guide_service import MedicalRefineOrchestrator

router = APIRouter(prefix="/stt", tags=["stt"])


@router.post("/format")
async def refine_medical_text(
    text: str | None = Form(None),
    audio: UploadFile | None = File(None),
):
    """
    STT(옵션) → LLM(의료 구조화) 처리 엔드포인트.

    입력:
    - text: STT 결과 텍스트 (Form)
    - audio: 오디오 파일 (multipart). 제공 시 STT를 수행하여 text를 대체/생성.

    출력:
    - {
        "summary": "...",
        "diagnosis": "...",
        "prescription": "...",
        "cautions": "...",
        "next_schedule": "..."
      }
    각 필드는 없으면 "" (LLMRefineService가 보장)
    """
    if (text is None or not text.strip()) and audio is None:
        raise HTTPException(status_code=400, detail="Either text or audio must be provided")

    audio_bytes = None
    if audio is not None:
        audio_bytes = await audio.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty audio file")

    try:
        orchestrator = MedicalRefineOrchestrator()
        result = orchestrator.process(
            text=text,
            audio_bytes=audio_bytes,
            audio_filename=audio.filename if audio else None,
            audio_content_type=audio.content_type if audio else None,
        )
        # API 스펙상 summary~next_schedule만 반환
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        # OpenAI 실패 등 서비스 레벨 에러
        raise HTTPException(status_code=502, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}") from e
