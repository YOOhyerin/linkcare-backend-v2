from __future__ import annotations

import threading
from typing import Dict, Optional, List

from models.domain import Booking


class InMemoryBookingRepository:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._store: Dict[str, Booking] = {}

    def save(self, booking: Booking) -> Booking:
        with self._lock:
            self._store[booking.id] = booking
            return booking

    def get(self, booking_id: str) -> Optional[Booking]:
        with self._lock:
            return self._store.get(booking_id)

    def list_all(self) -> List[Booking]:
        with self._lock:
            return list(self._store.values())
