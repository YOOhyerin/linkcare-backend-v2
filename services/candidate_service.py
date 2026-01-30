from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

from models.domain import CompanionRequest, Companion
from models.schemas import CandidateSortBy, CompanionCandidateOut
from repositories.companion_repo import InMemoryCompanionRepository


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    위경도 2점 사이 거리(km)
    """
    r = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


class CandidateService:
    def __init__(self, companion_repo: InMemoryCompanionRepository) -> None:
        self._companion_repo = companion_repo

    def get_candidates(
        self,
        req: CompanionRequest,
        sort_by: CandidateSortBy,
        max_distance: Optional[float],
        vehicle_only: Optional[bool],
    ) -> List[CompanionCandidateOut]:
        companions = self._companion_repo.list_all()

        out: List[CompanionCandidateOut] = []
        for c in companions:
            dist = haversine_km(req.start.lat, req.start.lng, c.location.lat, c.location.lng)

            # 필터: vehicle_only
            if vehicle_only is True and not c.vehicle:
                continue

            # 필터: max_distance
            if max_distance is not None and dist > max_distance:
                continue

            out.append(
                CompanionCandidateOut(
                    id=c.id,
                    name=c.name,
                    distance=round(dist, 2),
                    rating=c.rating,
                    vehicle=c.vehicle,
                    completed_count=c.completed_count,
                    profile_image=c.profile_image,
                )
            )

        # 정렬
        if sort_by == CandidateSortBy.DISTANCE:
            out.sort(key=lambda x: x.distance)
        elif sort_by == CandidateSortBy.RATING:
            out.sort(key=lambda x: x.rating, reverse=True)
        else:
            # BEST_MATCH (간단한 MVP 스코어링)
            # - 가까울수록, 평점 높을수록, 완료건수 많을수록 점수 증가
            def score(x: CompanionCandidateOut) -> float:
                # distance가 작을수록 좋으니 (1/(1+d)) 형태로 변환
                return (x.rating * 2.0) + (x.completed_count * 0.02) + (1.0 / (1.0 + x.distance)) * 3.0

            out.sort(key=score, reverse=True)

        return out
