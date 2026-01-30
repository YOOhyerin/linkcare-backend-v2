# services/llm_refine.py
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

        # Function tool schema (OpenAI Chat Completions tool calling)
        tool_schema = {
            "name": "MedicalConsultationRefinement",
            "description": "의료 상담/진료 STT 텍스트에서 임상적으로 관련된 정보를 추출하여 구조화합니다.",
            "parameters": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "summary": {"type": "string", "description": "전체 내용 요약"},
                    "diagnosis": {"type": "string", "description": "의심 소견 또는 진단 내용"},
                    "prescription": {"type": "string", "description": "처방된 약물 및 복약 지도"},
                    "cautions": {"type": "string", "description": "환자가 주의해야 할 사항"},
                    "next_schedule": {"type": "string", "description": "다음 예약 일정 또는 추적 검사"},
                },
                "required": ["summary", "diagnosis", "prescription", "cautions", "next_schedule"],
            },
        }

        system = (
            "You are a backend medical note formatter.\n"
            "Given Korean STT text of a medical visit (doctor-patient conversation), "
            "extract ONLY clinically relevant information and call the provided function tool.\n\n"
            "Rules:\n"
            "- Do NOT invent facts not present in the text.\n"
            "- If a field has no relevant content, return an empty string \"\".\n"
            "- Be concise and use Korean.\n"
            "- Remove filler, greetings, repetition, off-topic content.\n"
            "- summary: one short sentence summarizing the whole visit.\n"
            "- diagnosis: suspected finding / assessment / diagnosis (include key symptoms + impression if present).\n"
            "- prescription: medications, dosage, duration, and non-drug treatment instructions if explicitly mentioned.\n"
            "- cautions: warnings, precautions, red flags, activity restrictions, side effects mentioned.\n"
            "- next_schedule: follow-up appointment date/time, re-visit plan, tests to be done later; "
            "if time is vague, write it as described (e.g., '2주 후 재내원').\n"
        )

        user = f"STT text:\n{text}"

        try:
            resp = self._client.chat.completions.create(
                model=settings.OPENAI_LLM_MODEL,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                tools=[{"type": "function", "function": tool_schema}],
                tool_choice={"type": "function", "function": {"name": tool_schema["name"]}},
            )
        except Exception as e:
            raise RuntimeError(f"LLM refinement failed: {e}") from e

        msg = resp.choices[0].message

        # Tool calling 결과 파싱
        tool_calls = getattr(msg, "tool_calls", None)
        if not tool_calls:
            # 모델/설정 문제로 tool call이 안 떨어진 경우 대비
            raise RuntimeError("LLM did not return tool_calls")

        arguments = tool_calls[0].function.arguments
        if not arguments:
            raise RuntimeError("LLM returned empty arguments")

        data: Dict[str, Any] = json.loads(arguments)

        # 스펙: 없는 경우 빈 문자열 (모델이 강제하더라도 방어적으로 처리)
        summary = (data.get("summary") or "").strip()
        diagnosis = (data.get("diagnosis") or "").strip()
        prescription = (data.get("prescription") or "").strip()
        cautions = (data.get("cautions") or "").strip()
        next_schedule = (data.get("next_schedule") or "").strip()

        return RefinedResult(
            transcription_id=tr_id,
            text=text,
            summary=summary,
            diagnosis=diagnosis,
            prescription=prescription,
            cautions=cautions,
            next_schedule=next_schedule,
        )
