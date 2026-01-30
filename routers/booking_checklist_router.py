from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_checklist_service
from models.schemas import ChecklistCreateOut, VisitInfoOut, ChecklistCategoryOut, ChecklistItemOut
from services.checklist_service import ChecklistService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("/{booking_id}/checklist", response_model=ChecklistCreateOut, status_code=201)
def create_booking_checklist(
    booking_id: str,
    service: ChecklistService = Depends(get_checklist_service),
) -> ChecklistCreateOut:
    try:
        created = service.create_checklist(booking_id)
    except ValueError as e:
        code = str(e)
        if code == "BOOKING_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Booking not found")
        if code == "REQUEST_NOT_FOUND_FOR_BOOKING":
            raise HTTPException(status_code=500, detail="Booking data is inconsistent")
        raise

    return ChecklistCreateOut(
        checklist_id=created.checklist_id,
        booking_id=created.booking_id,
        visit_info=VisitInfoOut(
            hospital=created.visit_info.hospital,
            department=created.visit_info.department,
            visit_date=created.visit_info.visit_date,
        ),
        checklist=[
            ChecklistCategoryOut(
                category=c.category,
                items=[
                    ChecklistItemOut(item=i.item, required=i.required, reason=i.reason)
                    for i in c.items
                ],
            )
            for c in created.checklist
        ],
        special_notes=created.special_notes,
        created_at=created.created_at,
    )
