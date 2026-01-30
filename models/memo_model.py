from datetime import datetime
from pydantic import BaseModel


class MemoCreate(BaseModel):
    """메모 생성 요청"""
    content: str


class MemoResponse(BaseModel):
    """메모 응답"""
    memo_id: str
    elder_id: str
    content: str
    created_at: datetime
    created_by: dict


class Memo:
    """메모 엔티티"""
    def __init__(self, memo_id: str, elder_id: str, content: str, companion_id: str):
        self.memo_id = memo_id
        self.elder_id = elder_id
        self.content = content
        self.companion_id = companion_id
        self.created_at = datetime.utcnow()
    
    def to_dict(self):
        return {
            "memo_id": self.memo_id,
            "elder_id": self.elder_id,
            "content": self.content,
            "created_at": self.created_at,
            "created_by": {
                "companion_id": self.companion_id
            }
        }