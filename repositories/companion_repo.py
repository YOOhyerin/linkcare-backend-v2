from __future__ import annotations

import threading
from typing import List

from models.domain import Companion, GeoPoint


class InMemoryCompanionRepository:
    """
    DB 없이 테스트용 동행사 풀을 메모리에 유지.
    MVP: 서버 시작 시 샘플 데이터 로드.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._companions: List[Companion] = []

        # ✅ 샘플 데이터(원하면 너 데이터로 교체)
        self._companions.extend(
            [
                Companion(
                    id="cp_001",
                    name="김복지",
                    phone="010-9876-5432",
                    location=GeoPoint(lat=37.565, lng=126.936),
                    rating=4.8,
                    vehicle=True,
                    completed_count=45,
                    profile_image=None,
                ),
                Companion(
                    id="cp_002",
                    name="이봉사",
                    phone="010-9876-5432",
                    location=GeoPoint(lat=37.552, lng=126.952),
                    rating=4.6,
                    vehicle=True,
                    completed_count=32,
                    profile_image=None,
                ),
                Companion(
                    id="cp_003",
                    name="박동행",
                    phone="010-9876-5432",
                    location=GeoPoint(lat=37.590, lng=126.910),
                    rating=4.2,
                    vehicle=False,
                    completed_count=18,
                    profile_image=None,
                ),
            ]
        )

    def list_all(self) -> List[Companion]:
        with self._lock:
            return list(self._companions)
        
    def get(self, companion_id: str):
        with self._lock:
            for c in self._companions:
                if c.id == companion_id:
                    return c
            return None

