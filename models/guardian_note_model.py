from datetime import datetime
from pydantic import BaseModel


class GuardianNoteCreate(BaseModel):
    """보호자 메모 생성 요청"""
    content: str


class GuardianNoteResponse(BaseModel):
    """보호자 메모 응답"""
    note_id: str  # ← memo_id에서 수정
    elder_id: str
    content: str
    created_at: datetime
    created_by: dict


class GuardianNote:
    """보호자 메모 엔티티"""
    def __init__(self, note_id: str, elder_id: str, content: str, family_id: str):  # ← 수정
        self.note_id = note_id  # ← 수정
        self.elder_id = elder_id
        self.content = content
        self.family_id = family_id
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "note_id": self.note_id,  # ← 수정
            "elder_id": self.elder_id,
            "content": self.content,
            "created_at": self.created_at,
            "created_by": {
                "family_id": self.family_id
            }
        }