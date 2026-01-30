from fastapi import APIRouter, status, Query
from models.guardian_note_list_model import GuardianNoteListResponse
from services.guardian_note_list_service import guardian_note_list_service


router = APIRouter(prefix="/elders", tags=["guardian-notes"])


@router.get(
    "/{elder_id}/notes",
    response_model=GuardianNoteListResponse,
    status_code=status.HTTP_200_OK
)
async def get_guardian_notes(
    elder_id: str,
    page: int = Query(1, ge=1, description="페이지 번호 (기본값: 1)"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수 (기본값: 20)")
):
    """보호자 메모 목록 조회"""
    return guardian_note_list_service.get_notes(elder_id, page, limit)