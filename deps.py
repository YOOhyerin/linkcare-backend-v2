from repositories.request_repo import InMemoryRequestRepository
from repositories.companion_repo import InMemoryCompanionRepository
from repositories.booking_repo import InMemoryBookingRepository
from repositories.rating_repo import InMemoryRatingRepository
from repositories.checklist_repo import InMemoryChecklistRepository

from services.rating_service import RatingService
from services.request_service import RequestService
from services.candidate_service import CandidateService
from services.booking_service import BookingService
from services.companion_rating_service import CompanionRatingService
from services.checklist_service import ChecklistService

_request_repo = InMemoryRequestRepository()
_companion_repo = InMemoryCompanionRepository()
_booking_repo = InMemoryBookingRepository()
_rating_repo = InMemoryRatingRepository()
_checklist_repo = InMemoryChecklistRepository()

_request_service = RequestService(_request_repo)
_candidate_service = CandidateService(_companion_repo)
_booking_service = BookingService(_booking_repo, _request_repo, _companion_repo)
_rating_service = RatingService(_rating_repo, _booking_repo)
_companion_rating_service = CompanionRatingService(_rating_repo, _companion_repo)
_checklist_service = ChecklistService(_checklist_repo, _booking_repo, _request_repo)

def get_request_service() -> RequestService:
    return _request_service

def get_candidate_service() -> CandidateService:
    return _candidate_service

def get_booking_service() -> BookingService:
    return _booking_service

def get_rating_service() -> RatingService:
    return _rating_service

def get_companion_rating_service() -> CompanionRatingService:
    return _companion_rating_service

def get_checklist_service() -> ChecklistService:
    return _checklist_service
