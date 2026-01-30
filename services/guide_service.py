# services/guide_service.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

from services.stt_service import STTService
from services.llm_refine import LLMRefineService, RefinedResult


@dataclass(frozen=True)
class MedicalStructuredResponse:
    transcription_id: str
    text: str
    summary: str
    diagnosis: str
    prescription: str
    cautions: str
    next_schedule: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "diagnosis": self.diagnosis,
            "prescription": self.prescription,
            "cautions": self.cautions,
            "next_schedule": self.next_schedule,
        }


class MedicalRefineOrchestrator:
    """
    STTService → LLMRefineService 오케스트레이션

    입력:
    - context_text (선택): 이미 STT된 텍스트
    - audio_bytes (선택): 오디오 바이너리(있으면 STT 수행)
    - audio_filename/content_type (선택): STT multipart 전송용

    출력(필드 없으면 빈 문자열 규칙은 LLMRefineService가 보장):
    - summary, diagnosis, prescription, cautions, next_schedule
    """

    def __init__(self) -> None:
        self.stt = STTService()
        self.llm_refine = LLMRefineService()

    def process(
        self,
        *,
        text: Optional[str] = None,
        audio_bytes: Optional[bytes] = None,
        audio_filename: Optional[str] = None,
        audio_content_type: Optional[str] = None,
        transcription_id: Optional[str] = None,
        # STT 옵션(필요시 외부에서 override)
        stt_language: Optional[str] = None,
        stt_prompt: Optional[str] = None,
    ) -> MedicalStructuredResponse:
        # 1) 텍스트 결정: 오디오가 있으면 STT 우선
        final_text = (text or "").strip()

        if audio_bytes:
            stt_result = self.stt.transcribe(
                audio_bytes=audio_bytes,
                filename=audio_filename or "audio.wav",
                content_type=audio_content_type,
                language=stt_language,   # None이면 STTService 내부에서 settings default 사용
                prompt=stt_prompt,
                response_format="json",
            )
            final_text = (stt_result.text or "").strip()

        if not final_text:
            raise ValueError("No input text. Provide either `text` or `audio_bytes`.")

        # 2) LLM 정제(의료 구조화)
        refined: RefinedResult = self.llm_refine.refine_medical_consultation(
            text=final_text,
            transcription_id=transcription_id,
        )

        return MedicalStructuredResponse(
            transcription_id=refined.transcription_id,
            text=refined.text,
            summary=refined.summary,
            diagnosis=refined.diagnosis,
            prescription=refined.prescription,
            cautions=refined.cautions,
            next_schedule=refined.next_schedule,
        )
