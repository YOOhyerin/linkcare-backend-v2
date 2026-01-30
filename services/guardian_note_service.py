from models.guardian_note_model import GuardianNoteCreate, GuardianNoteResponse
from repositories.guardian_note_repository import guardian_note_repository


class GuardianNoteService:
    """보호자 메모 비즈니스 로직"""
    
    def __init__(self):
        self.repository = guardian_note_repository
    
    def create_note(self, elder_id: str, note_data: GuardianNoteCreate, family_id: str) -> GuardianNoteResponse:
        """보호자 메모 생성"""
        note = self.repository.create(elder_id, note_data.content, family_id)
        return GuardianNoteResponse(**note.to_dict())


# 싱글톤
guardian_note_service = GuardianNoteService()