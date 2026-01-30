from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from deps import get_booking_service, get_rating_service
from models.schemas import (
    BookingCreateIn, BookingCreateOut, BookingStatus,
    BookingDetailOut, RequestSummaryOut, StartOut, CompanionSummaryOut,
    TimelineItemOut, TimelineStage, TimelineStatus,
    RatingCreateIn, RatingCreateOut
)
from services.booking_service import BookingService
from services.rating_service import RatingService

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingCreateOut, status_code=201)
def create_booking(
    body: BookingCreateIn,
    service: BookingService = Depends(get_booking_service),
) -> BookingCreateOut:
    try:
        created = service.create_booking(body)
    except ValueError as e:
        code = str(e)
        if code == "REQUEST_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Request not found")
        if code == "COMPANION_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Companion not found")
        if code == "REQUEST_ALREADY_CONFIRMED":
            raise HTTPException(status_code=409, detail="Request already confirmed")
        raise

    return BookingCreateOut(
        id=created.id,
        status=BookingStatus(created.status.value),
        booking_code=created.booking_code,
        created_at=created.created_at,
    )


@router.get("/{bookingId}", response_model=BookingDetailOut)
def get_booking_detail(
    bookingId: str,
    service: BookingService = Depends(get_booking_service),
) -> BookingDetailOut:
    agg = service.get_booking_aggregate(bookingId)
    if agg is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    booking, req, companion = agg

    return BookingDetailOut(
        id=booking.id,
        status=BookingStatus(booking.status.value),
        request=RequestSummaryOut(
            visit_date=req.visit_date,
            hospital=req.hospital,
            department=req.department,
            start=StartOut(address=req.start.address, lat=req.start.lat, lng=req.start.lng),
            vehicle_required=req.vehicle_required,
        ),
        companion=CompanionSummaryOut(
            id=companion.id,
            name=companion.name,
            phone=companion.phone,
            rating=companion.rating,
        ),
        timeline=[
            TimelineItemOut(
                stage=TimelineStage(t.stage.value),
                status=TimelineStatus(t.status.value),
                scheduled_at=t.scheduled_at,
            )
            for t in booking.timeline
        ],
        created_at=booking.created_at,
        updated_at=booking.updated_at,
    )


@router.post("/{bookingId}/rating", response_model=RatingCreateOut, status_code=201)
def create_booking_rating(
    bookingId: str,
    body: RatingCreateIn,
    service: RatingService = Depends(get_rating_service),
) -> RatingCreateOut:
    try:
        created = service.create_rating(bookingId, body)
    except ValueError as e:
        code = str(e)
        if code == "BOOKING_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Booking not found")
        if code == "RATING_ALREADY_EXISTS":
            raise HTTPException(status_code=409, detail="Rating already exists for this booking")
        if code == "INVALID_STARS":
            raise HTTPException(status_code=422, detail="Stars must be between 1 and 5")
        raise

    return RatingCreateOut(
        id=created.id,
        booking_id=created.booking_id,
        companion_id=created.companion_id,
        stars=created.stars,
        created_at=created.created_at,
    )
