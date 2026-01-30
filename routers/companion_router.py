from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_companion_rating_service
from models.schemas import CompanionRatingSummaryOut
from services.companion_rating_service import CompanionRatingService

router = APIRouter(prefix="/companions", tags=["companions"])


@router.get("/{companionId}/rating/summary", response_model=CompanionRatingSummaryOut)
def get_rating_summary(
    companionId: str,
    service: CompanionRatingService = Depends(get_companion_rating_service),
) -> CompanionRatingSummaryOut:
    try:
        cid, avg, cnt = service.get_summary(companionId)
    except ValueError as e:
        if str(e) == "COMPANION_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Companion not found")
        raise

    return CompanionRatingSummaryOut(
        companion_id=cid,
        average_stars=avg,
        rating_count=cnt,
    )
