# routers/stt_router.py
from __future__ import annotations

from fastapi import APIRouter, UploadFile, File, HTTPException, Query

from services.stt_service import STTService
from services.llm_refine import LLMRefineService

router = APIRouter(prefix="/stt", tags=["stt"])


@router.post("/text")
async def create_transcription(
    file: UploadFile = File(...),
    language: str | None = Query(default=None, description="예: ko"),
    prompt: str | None = Query(default=None, description="STT 힌트(선택)"),
    refine: bool = Query(default=True, description="LLM 의료 구조화 수행 여부"),
):
    """
    오디오 업로드 → STT 텍스트 반환 (+ 옵션: 의료 구조화)
    - refine=false: STT 텍스트/raw만 반환
    - refine=true : STT 텍스트 + (summary/diagnosis/prescription/cautions/next_schedule) 반환
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")

    allowed_ext = {"flac", "mp3", "mp4", "mpeg", "mpga", "m4a", "ogg", "wav", "webm"}
    ext = (file.filename.rsplit(".", 1)[-1] or "").lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail=f"Unsupported audio format: .{ext}")

    # 1) STT
    stt = STTService()
    try:
        stt_result = stt.transcribe(
            audio_bytes=audio_bytes,
            filename=file.filename,
            content_type=file.content_type,
            language=language,
            prompt=prompt,
            response_format="json",
        )
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e

    text = (stt_result.text or "").strip()

    # refine=false이면 STT 결과만 반환(디버깅/비용절감)
    if not refine:
        return {"text": text, "raw": stt_result.raw}

    # 2) LLM 정제 (의료 구조화)
    llm = LLMRefineService()
    try:
        refined = llm.refine_medical_consultation(text=text)
    except RuntimeError as e:
        # 부분 성공 권장: STT 텍스트는 주고, 정제 실패만 표시
        return {
            "text": text,
            "summary": "",
            "diagnosis": "",
            "prescription": "",
            "cautions": "",
            "next_schedule": "",
            "llm_status": "FAILED",
            "llm_error": str(e),
        }

    # 3) 최종 응답(요구 양식 + STT text 포함)
    return {
        "text": refined.text,
        "summary": refined.summary,
        "diagnosis": refined.diagnosis,
        "prescription": refined.prescription,
        "cautions": refined.cautions,
        "next_schedule": refined.next_schedule,
    }
