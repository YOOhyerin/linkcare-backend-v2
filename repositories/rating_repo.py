from __future__ import annotations

import threading
from typing import Dict, Optional, Tuple

from models.domain import Rating


class InMemoryRatingRepository:
    """
    key를 booking_id로 잡아서 '예약당 1회 평가' 제약을 강제하기 쉬움.
    """
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._by_booking: Dict[str, Rating] = {}

    def get_by_booking_id(self, booking_id: str) -> Optional[Rating]:
        with self._lock:
            return self._by_booking.get(booking_id)

    def save(self, rating: Rating) -> Rating:
        with self._lock:
            self._by_booking[rating.booking_id] = rating
            return rating

    # ✅ 추가: companion_id 기준으로 (sum, count) 반환
    def sum_and_count_by_companion(self, companion_id: str) -> Tuple[int, int]:
        with self._lock:
            total = 0
            count = 0
            for r in self._by_booking.values():
                if r.companion_id == companion_id:
                    total += r.stars
                    count += 1
            return total, count
