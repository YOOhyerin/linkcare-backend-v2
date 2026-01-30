from __future__ import annotations

from datetime import date, datetime, timezone
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class RequestStatus(str, Enum):
    CREATED = "CREATED"
    MATCHED = "MATCHED"
    CONFIRMED = "CONFIRMED"


class StartIn(BaseModel):
    address: str = Field(..., min_length=1, description="출발지 주소")
    lat: float = Field(..., ge=-90, le=90, description="위도")
    lng: float = Field(..., ge=-180, le=180, description="경도")


class RequestCreateIn(BaseModel):
    visit_date: date = Field(..., description="병원 방문 예정 날짜 (YYYY-MM-DD)")
    hospital: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    start: StartIn
    vehicle_required: bool = Field(default=False, description="차량 동행 필요 여부")
    guardian_phone: Optional[str] = Field(default=None, description="보호자 연락처")
    notes: Optional[str] = Field(default=None, description="특이사항")

    @field_validator("guardian_phone")
    @classmethod
    def normalize_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v if v else None


class RequestCreateOut(BaseModel):
    id: str
    status: RequestStatus
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        # 응답에서는 UTC 타임존을 명확히
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)
    
class CandidateSortBy(str, Enum):
    BEST_MATCH = "BEST_MATCH"
    DISTANCE = "DISTANCE"
    RATING = "RATING"


class CompanionCandidateOut(BaseModel):
    id: str
    name: str
    distance: float = Field(..., ge=0, description="km")
    rating: float = Field(..., ge=0.0, le=5.0)
    vehicle: bool
    completed_count: int = Field(..., ge=0)
    profile_image: Optional[str] = None


class CandidatesOut(BaseModel):
    companions: List[CompanionCandidateOut]


class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


# ---- POST /bookings 기존 ----
class BookingCreateIn(BaseModel):
    request_id: str = Field(..., min_length=1)
    companion_id: str = Field(..., min_length=1)


class BookingCreateOut(BaseModel):
    id: str
    status: BookingStatus
    booking_code: str
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


# ---- GET /bookings/{bookingId} 응답 ----
class StartOut(BaseModel):
    address: str
    lat: float
    lng: float


class RequestSummaryOut(BaseModel):
    visit_date: str
    hospital: str
    department: str
    start: StartOut
    vehicle_required: bool


class CompanionSummaryOut(BaseModel):
    id: str
    name: str
    phone: str
    rating: float


class TimelineStage(str, Enum):
    DEPARTURE = "DEPARTURE"
    HOSPITAL_ARRIVAL = "HOSPITAL_ARRIVAL"
    PHARMACY = "PHARMACY"
    HOME_ARRIVAL = "HOME_ARRIVAL"


class TimelineStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    SKIPPED = "SKIPPED"


class TimelineItemOut(BaseModel):
    stage: TimelineStage
    status: TimelineStatus
    scheduled_at: Optional[datetime] = None

    @field_validator("scheduled_at")
    @classmethod
    def ensure_utc_opt(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is None:
            return None
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class BookingDetailOut(BaseModel):
    id: str
    status: BookingStatus
    request: RequestSummaryOut
    companion: CompanionSummaryOut
    timeline: List[TimelineItemOut]
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class RatingCreateIn(BaseModel):
    stars: int = Field(..., ge=1, le=5, description="별점 (1~5)")


class RatingCreateOut(BaseModel):
    id: str
    booking_id: str
    companion_id: str
    stars: int
    created_at: datetime

    @field_validator("created_at")
    @classmethod
    def ensure_utc(cls, v: datetime) -> datetime:
        if v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)


class CompanionRatingSummaryOut(BaseModel):
    companion_id: str = Field(..., min_length=1)
    average_stars: float = Field(..., ge=0.0, le=5.0)
    rating_count: int = Field(..., ge=0)
