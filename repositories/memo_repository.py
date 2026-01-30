from datetime import datetime
from models.memo_model import Memo  # ← 변경
import uuid


class MemoRepository:
    """메모 저장소 (인메모리)"""
    
    def __init__(self):
        self._memos = {}
    
    def create(self, elder_id: str, content: str, companion_id: str) -> Memo:
        """메모 생성"""
        memo_id = f"memo_{uuid.uuid4().hex[:8]}"
        memo = Memo(memo_id, elder_id, content, companion_id)
        self._memos[memo_id] = memo
        return memo


# 싱글톤
memo_repository = MemoRepository()