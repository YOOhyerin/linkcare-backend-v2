from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from openai import OpenAI

from core.config import settings
from models.domain import ChecklistResult, VisitInfo, ChecklistCategory, ChecklistItem
from models.schemas import LLMChecklistOutput
from repositories.checklist_repo import InMemoryChecklistRepository
from repositories.booking_repo import InMemoryBookingRepository
from repositories.request_repo import InMemoryRequestRepository


class ChecklistService:
    def __init__(
        self,
        checklist_repo: InMemoryChecklistRepository,
        booking_repo: InMemoryBookingRepository,
        request_repo: InMemoryRequestRepository,
    ) -> None:
        self._checklist_repo = checklist_repo
        self._booking_repo = booking_repo
        self._request_repo = request_repo

        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def create_checklist(self, booking_id: str) -> ChecklistResult:
        booking = self._booking_repo.get(booking_id)
        if booking is None:
            raise ValueError("BOOKING_NOT_FOUND")

        req = self._request_repo.get(booking.request_id)
        if req is None:
            # 인메모리 특성상 데이터 깨짐 방어
            raise ValueError("REQUEST_NOT_FOUND_FOR_BOOKING")

        visit = VisitInfo(
            hospital=req.hospital,
            department=req.department,
            visit_date=req.visit_date,  # "YYYY-MM-DD"
        )

        system_msg = (
            "너는 한국의 병원 진료 전 준비물 체크리스트를 만드는 도우미야.\n"
            "반드시 다음 4개 구성으로만 출력해야 한다:\n"
            "1) checklist[카테고리 3개]: '필수 서류', '의료 기록', '기타 준비물'\n"
            "2) special_notes: '기타 사항'에 해당하는 주의/팁 목록\n"
            "카테고리명은 정확히 위 문자열을 사용하고, 누락하거나 추가 카테고리를 만들지 마.\n"
            "각 item은 짧고 구체적으로 작성하고, required는 꼭 필요한지 여부로 설정해.\n"
            "reason은 필요하면 한 문장으로만."
        )

        user_msg = (
            f"다음 예약의 진료 전 준비물 체크리스트를 만들어줘.\n"
            f"- 병원: {visit.hospital}\n"
            f"- 진료과: {visit.department}\n"
            f"- 방문 예정일: {visit.visit_date}\n"
            f"추가 조건:\n"
            f"- 환자는 '어르신'일 수 있어, 이동/접수/검사 동선에 유용한 준비물도 고려해.\n"
        )

        # Structured Outputs (Pydantic)로 강제
        resp = self._client.responses.parse(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            text_format=LLMChecklistOutput,
        )
        parsed: LLMChecklistOutput = resp.output_parsed

        checklist_id = f"chk_{uuid4().hex[:12]}"
        now = datetime.now(timezone.utc)

        # 도메인 변환
        categories = []
        for c in parsed.checklist:
            categories.append(
                ChecklistCategory(
                    category=c.category.value,
                    items=[
                        ChecklistItem(
                            item=i.item,
                            required=i.required,
                            reason=(i.reason or "").strip() or None,
                        )
                        for i in c.items
                    ],
                )
            )

        result = ChecklistResult(
            checklist_id=checklist_id,
            booking_id=booking_id,
            visit_info=visit,
            checklist=categories,
            special_notes=[s for s in parsed.special_notes if s and s.strip()],
            created_at=now,
        )

        return self._checklist_repo.save(result)
