from models.guardian_note_list_model import GuardianNoteListResponse, GuardianNoteItem
from repositories.guardian_note_list_repository import guardian_note_list_repository


class GuardianNoteListService:
    """보호자 메모 목록 조회 전용 서비스"""
    
    def __init__(self):
        self.repository = guardian_note_list_repository
    
    def get_notes(self, elder_id: str, page: int = 1, limit: int = 20) -> GuardianNoteListResponse:
        """보호자 메모 목록 조회"""
        notes, total = self.repository.find_by_elder_id(elder_id, page, limit)
        
        # dict -> GuardianNoteItem 변환
        items = [GuardianNoteItem(**note) for note in notes]
        
        return GuardianNoteListResponse(
            items=items,
            pagination={
                "total": total,
                "page": page,
                "limit": limit
            }
        )


# 싱글톤
guardian_note_list_service = GuardianNoteListService()