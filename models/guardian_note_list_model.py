from datetime import datetime
from pydantic import BaseModel
from typing import List


class GuardianNoteItem(BaseModel):
    """보호자 메모 목록 항목"""
    note_id: str
    content: str
    created_at: datetime
    created_by: dict


class GuardianNoteListResponse(BaseModel):
    """보호자 메모 목록 응답"""
    items: List[GuardianNoteItem]
    pagination: dict