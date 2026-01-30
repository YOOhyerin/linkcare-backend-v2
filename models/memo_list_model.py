from datetime import datetime
from pydantic import BaseModel
from typing import List


class MemoItem(BaseModel):
    """메모 목록 항목"""
    memo_id: str
    content: str
    created_at: datetime
    created_by: dict


class MemoListResponse(BaseModel):
    """메모 목록 응답"""
    items: List[MemoItem]
    pagination: dict