from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from models.domain import (
    Booking, BookingStatus,
    TimelineItem, TimelineStage, TimelineStatus,
    RequestStatus,
)
from models.schemas import BookingCreateIn
from repositories.booking_repo import InMemoryBookingRepository
from repositories.request_repo import InMemoryRequestRepository
from repositories.companion_repo import InMemoryCompanionRepository


class BookingService:
    def __init__(
        self,
        booking_repo: InMemoryBookingRepository,
        request_repo: InMemoryRequestRepository,
        companion_repo: InMemoryCompanionRepository,
    ) -> None:
        self._booking_repo = booking_repo
        self._request_repo = request_repo
        self._companion_repo = companion_repo

        self._last_date = None
        self._seq = 0

    def _next_booking_code(self, now_utc: datetime) -> str:
        day = now_utc.strftime("%Y%m%d")
        if self._last_date != day:
            self._last_date = day
            self._seq = 0
        self._seq += 1
        return f"BK{day}{self._seq:03d}"

    def create_booking(self, payload: BookingCreateIn) -> Booking:
        req = self._request_repo.get(payload.request_id)
        if req is None:
            raise ValueError("REQUEST_NOT_FOUND")

        companion = self._companion_repo.get(payload.companion_id)
        if companion is None:
            raise ValueError("COMPANION_NOT_FOUND")

        if req.status == RequestStatus.CONFIRMED:
            raise ValueError("REQUEST_ALREADY_CONFIRMED")

        now = datetime.now(timezone.utc)
        booking_id = f"bk_{uuid4().hex[:12]}"
        booking_code = self._next_booking_code(now)

        # ✅ timeline 초기화(예시: 출발은 visit_date 09:00Z로 가정)
        scheduled_departure = None
        try:
            scheduled_departure = datetime.fromisoformat(req.visit_date + "T09:00:00+00:00")
        except Exception:
            scheduled_departure = None

        timeline = [
            TimelineItem(stage=TimelineStage.DEPARTURE, status=TimelineStatus.PENDING, scheduled_at=scheduled_departure),
            TimelineItem(stage=TimelineStage.HOSPITAL_ARRIVAL, status=TimelineStatus.PENDING, scheduled_at=None),
            TimelineItem(stage=TimelineStage.PHARMACY, status=TimelineStatus.PENDING, scheduled_at=None),
            TimelineItem(stage=TimelineStage.HOME_ARRIVAL, status=TimelineStatus.PENDING, scheduled_at=None),
        ]

        booking = Booking(
            id=booking_id,
            request_id=payload.request_id,
            companion_id=payload.companion_id,
            status=BookingStatus.CONFIRMED,
            booking_code=booking_code,
            timeline=timeline,
            created_at=now,
            updated_at=now,
        )

        self._booking_repo.save(booking)

        updated_req = replace(req, status=RequestStatus.CONFIRMED)
        self._request_repo.save(updated_req)

        return booking

    # ✅ GET용: booking + request + companion을 함께 반환하기 위해
    def get_booking_aggregate(self, booking_id: str):
        booking = self._booking_repo.get(booking_id)
        if booking is None:
            return None

        req = self._request_repo.get(booking.request_id)
        companion = self._companion_repo.get(booking.companion_id)

        # 데이터 일관성 깨진 경우(인메모리에서 가능): None 처리
        if req is None or companion is None:
            return None

        return booking, req, companion
