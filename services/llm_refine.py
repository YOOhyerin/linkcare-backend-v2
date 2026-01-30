# llm_refine.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
from uuid import uuid4
import json

from openai import OpenAI

from core.config import settings


@dataclass
class RefinedResult:
    transcription_id: str
    text: str
    summary: str
    diagnosis: str
    prescription: str
    cautions: str
    next_schedule: str


class LLMRefineService:
    """
    STT 결과 text를 입력받아 의료 진료/상담 내용을 구조화하는 서비스.

    출력 필드(없으면 빈 문자열):
    - summary: 전체 요약
    - diagnosis: 의심 소견/진단 내용
    - prescription: 처방 및 복약 지도
    - cautions: 주의사항
    - next_schedule: 다음 일정/추적 검사
    """

    def __init__(self) -> None:
        if not settings.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def refine_medical_consultation(
        self,
        *,
        text: str,
        transcription_id: Optional[str] = None,
    ) -> RefinedResult:
        if not text.strip():
            raise ValueError("Empty transcription text")

        tr_id = transcription_id or f"tr_{uuid4().hex[:12]}"

        # JSON Schema: 반드시 이 형태로만 나오도록 강제
        schema = {
            "name": "MedicalConsultationRefinement",
            "schema": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "summary": {"type": "string"},
                    "diagnosis": {"type": "string"},
                    "prescription": {"type": "string"},
                    "cautions": {"type": "string"},
                    "next_schedule": {"type": "string"},
                },
                "required": ["summary", "diagnosis", "prescription", "cautions", "next_schedule"],
            },
            "strict": True,
        }

        system = (
            "You are a backend medical note formatter.\n"
            "Given Korean STT text of a medical visit (doctor-patient conversation or announcement), "
            "extract ONLY clinically relevant information and format it into the given JSON schema.\n\n"
            "Rules:\n"
            "- Output must be valid JSON that matches the schema exactly. No extra keys.\n"
            "- If a field has no relevant content, return an empty string \"\".\n"
            "- Be concise and use Korean.\n"
            "- Remove filler, greetings, repetition, off-topic content.\n"
            "- 'summary': one short sentence summarizing the whole visit.\n"
            "- 'diagnosis': suspected finding / assessment / diagnosis (include key symptoms + impression if present).\n"
            "- 'prescription': medications, dosage, duration, and non-drug treatment instructions if explicitly mentioned.\n"
            "- 'cautions': warnings, precautions, red flags, activity restrictions, side effects mentioned.\n"
            "- 'next_schedule': follow-up appointment date/time, re-visit plan, tests to be done later; "
            "if time is vague, write it as described (e.g., '2주 후 재내원').\n"
        )

        user = (
            "STT text:\n"
            f"{text}\n\n"
            "Return JSON only. Do not include any extra keys."
        )

        try:
            resp = self._client.chat.completions.create(
                model=settings.OPENAI_LLM_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={"type": "json_schema", "json_schema": schema},
            )
        except Exception as e:
            raise RuntimeError(f"LLM refinement failed: {e}") from e

        content = resp.choices[0].message.content
        if not content:
            raise RuntimeError("LLM returned empty content")

        data: Dict[str, Any] = json.loads(content)

        # strict schema라 키는 항상 존재해야 하지만, 방어적으로 .get + 기본값 처리
        return RefinedResult(
            transcription_id=tr_id,
            text=text,
            summary=(data.get("summary") or "").strip(),
            diagnosis=(data.get("diagnosis") or "").strip(),
            prescription=(data.get("prescription") or "").strip(),
            cautions=(data.get("cautions") or "").strip(),
            next_schedule=(data.get("next_schedule") or "").strip(),
        )
