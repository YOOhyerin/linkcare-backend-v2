from __future__ import annotations

from repositories.rating_repo import InMemoryRatingRepository
from repositories.companion_repo import InMemoryCompanionRepository


class CompanionRatingService:
    def __init__(
        self,
        rating_repo: InMemoryRatingRepository,
        companion_repo: InMemoryCompanionRepository,
    ) -> None:
        self._rating_repo = rating_repo
        self._companion_repo = companion_repo

    def get_summary(self, companion_id: str) -> tuple[str, float, int]:
        # companion 존재 확인(요구사항엔 없지만 API 품질상 권장)
        companion = self._companion_repo.get(companion_id)
        if companion is None:
            raise ValueError("COMPANION_NOT_FOUND")

        total, count = self._rating_repo.sum_and_count_by_companion(companion_id)

        if count == 0:
            return companion_id, 0.0, 0

        avg = total / count
        # 소수점 둘째 자리에서 반올림 → 첫째 자리까지
        avg_1dp = round(avg + 1e-12, 1)
        return companion_id, avg_1dp, count
