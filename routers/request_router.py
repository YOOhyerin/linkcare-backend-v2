from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from deps import get_request_service, get_candidate_service
from models.schemas import (
    RequestCreateIn, RequestCreateOut, RequestStatus,
    CandidatesOut, CandidateSortBy
)
from services.request_service import RequestService
from services.candidate_service import CandidateService

router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("", response_model=RequestCreateOut, status_code=201)
def create_request(
    body: RequestCreateIn,
    service: RequestService = Depends(get_request_service),
) -> RequestCreateOut:
    created = service.create_request(body)
    return RequestCreateOut(
        id=created.id,
        status=RequestStatus(created.status.value),
        created_at=created.created_at,
    )


@router.get("/{requestId}/candidates", response_model=CandidatesOut)
def get_candidates(
    requestId: str,
    sort_by: CandidateSortBy = Query(default=CandidateSortBy.BEST_MATCH),
    max_distance: float | None = Query(default=None, gt=0),
    vehicle_only: bool | None = Query(default=None),
    request_service: RequestService = Depends(get_request_service),
    candidate_service: CandidateService = Depends(get_candidate_service),
) -> CandidatesOut:
    req = request_service.get_request(requestId)
    if req is None:
        raise HTTPException(status_code=404, detail="Request not found")

    companions = candidate_service.get_candidates(
        req=req,
        sort_by=sort_by,
        max_distance=max_distance,
        vehicle_only=vehicle_only,
    )
    return CandidatesOut(companions=companions)
