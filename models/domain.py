from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RequestStatus(str, Enum):
    CREATED = "CREATED"
    MATCHED = "MATCHED"
    CONFIRMED = "CONFIRMED"


@dataclass(frozen=True)
class StartLocation:
    address: str
    lat: float
    lng: float


@dataclass(frozen=True)
class CompanionRequest:
    id: str
    visit_date: str
    hospital: str
    department: str
    start: StartLocation
    vehicle_required: bool
    guardian_phone: str | None
    notes: str | None
    status: RequestStatus
    created_at: datetime


@dataclass(frozen=True)
class GeoPoint:
    lat: float
    lng: float


# ✅ phone 추가
@dataclass(frozen=True)
class Companion:
    id: str
    name: str
    phone: str
    location: GeoPoint
    rating: float
    vehicle: bool
    completed_count: int
    profile_image: str | None = None


# ✅ Booking 확장
class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"


class TimelineStage(str, Enum):
    DEPARTURE = "DEPARTURE"
    HOSPITAL_ARRIVAL = "HOSPITAL_ARRIVAL"
    PHARMACY = "PHARMACY"
    HOME_ARRIVAL = "HOME_ARRIVAL"


class TimelineStatus(str, Enum):
    PENDING = "PENDING"
    DONE = "DONE"
    SKIPPED = "SKIPPED"


@dataclass(frozen=True)
class TimelineItem:
    stage: TimelineStage
    status: TimelineStatus
    scheduled_at: datetime | None = None


@dataclass(frozen=True)
class Booking:
    id: str
    request_id: str
    companion_id: str
    status: BookingStatus
    booking_code: str
    timeline: list[TimelineItem]
    created_at: datetime  # UTC
    updated_at: datetime  # UTC

@dataclass(frozen=True)
class Rating:
    id: str
    booking_id: str
    companion_id: str
    stars: int  # 1~5
    created_at: datetime  # UTC

@dataclass(frozen=True)
class VisitInfo:
    hospital: str
    department: str
    visit_date: str  # "YYYY-MM-DD"


@dataclass(frozen=True)
class ChecklistItem:
    item: str
    required: bool
    reason: str | None = None


@dataclass(frozen=True)
class ChecklistCategory:
    category: str  # "필수 서류" | "의료 기록" | "기타 준비물"
    items: list[ChecklistItem]


@dataclass(frozen=True)
class ChecklistResult:
    checklist_id: str
    booking_id: str
    visit_info: VisitInfo
    checklist: list[ChecklistCategory]
    special_notes: list[str]  # ✅ "기타 사항"에 해당
    created_at: datetime  # UTC
