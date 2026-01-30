from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from uuid import uuid4

from models.domain import CompanionRequest, RequestStatus, StartLocation
from models.schemas import RequestCreateIn
from repositories.request_repo import InMemoryRequestRepository


class RequestService:
    def __init__(self, repo: InMemoryRequestRepository) -> None:
        self._repo = repo

    def create_request(self, payload: RequestCreateIn) -> CompanionRequest:
        request_id = f"req_{uuid4().hex[:12]}"
        created_at = datetime.now(timezone.utc)

        domain = CompanionRequest(
            id=request_id,
            visit_date=payload.visit_date.isoformat(),
            hospital=payload.hospital,
            department=payload.department,
            start=StartLocation(
                address=payload.start.address,
                lat=payload.start.lat,
                lng=payload.start.lng,
            ),
            vehicle_required=payload.vehicle_required,
            guardian_phone=payload.guardian_phone,
            notes=payload.notes,
            status=RequestStatus.CREATED,
            created_at=created_at,
        )

        return self._repo.save(domain)
    
    def get_request(self, request_id: str) -> CompanionRequest | None:
        return self._repo.get(request_id)
