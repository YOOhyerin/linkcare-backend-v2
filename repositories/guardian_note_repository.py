from datetime import datetime
from models.guardian_note_model import GuardianNote
import uuid


class GuardianNoteRepository:
    """보호자 메모 저장소 (인메모리)"""
    
    def __init__(self):
        self._notes = {}  # note_id -> GuardianNote  ← 주석 수정
    
    def create(self, elder_id: str, content: str, family_id: str) -> GuardianNote:
        """보호자 메모 생성"""
        note_id = f"note_{uuid.uuid4().hex[:8]}"  # ← memo_에서 note_로 수정
        note = GuardianNote(note_id, elder_id, content, family_id)
        self._notes[note_id] = note  # ← 수정
        return note


# 싱글톤
guardian_note_repository = GuardianNoteRepository()