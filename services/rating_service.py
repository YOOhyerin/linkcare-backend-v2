from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from models.domain import Rating
from models.schemas import RatingCreateIn
from repositories.rating_repo import InMemoryRatingRepository
from repositories.booking_repo import InMemoryBookingRepository


class RatingService:
    def __init__(
        self,
        rating_repo: InMemoryRatingRepository,
        booking_repo: InMemoryBookingRepository,
    ) -> None:
        self._rating_repo = rating_repo
        self._booking_repo = booking_repo

    def create_rating(self, booking_id: str, payload: RatingCreateIn) -> Rating:
        # 1) booking 존재 확인
        booking = self._booking_repo.get(booking_id)
        if booking is None:
            raise ValueError("BOOKING_NOT_FOUND")

        # 2) 중복 평가 방지
        existing = self._rating_repo.get_by_booking_id(booking_id)
        if existing is not None:
            raise ValueError("RATING_ALREADY_EXISTS")

        # 3) stars는 스키마에서 1~5 검증되지만, 혹시 모를 방어적 체크
        if not (1 <= payload.stars <= 5):
            raise ValueError("INVALID_STARS")

        now = datetime.now(timezone.utc)
        rating_id = f"rt_{uuid4().hex[:12]}"

        rating = Rating(
            id=rating_id,
            booking_id=booking_id,
            companion_id=booking.companion_id,
            stars=payload.stars,
            created_at=now,
        )
        return self._rating_repo.save(rating)
