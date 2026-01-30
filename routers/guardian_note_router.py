from fastapi import APIRouter, status
from models.guardian_note_model import GuardianNoteCreate, GuardianNoteResponse
from services.guardian_note_service import guardian_note_service


router = APIRouter(prefix="/elders", tags=["guardian-notes"])


@router.post(
    "/{elder_id}/notes",
    response_model=GuardianNoteResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_guardian_note(
    elder_id: str,
    note_data: GuardianNoteCreate,
    family_id: str = "family_777"
):
    """보호자 메모 생성"""
    return guardian_note_service.create_note(elder_id, note_data, family_id)