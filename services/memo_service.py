from models.memo_model import MemoCreate, MemoResponse  # ← 변경
from repositories.memo_repository import memo_repository


class MemoService:
    """메모 비즈니스 로직"""
    
    def __init__(self):
        self.repository = memo_repository
    
    def create_memo(self, elder_id: str, memo_data: MemoCreate, companion_id: str) -> MemoResponse:
        """메모 생성"""
        memo = self.repository.create(elder_id, memo_data.content, companion_id)
        return MemoResponse(**memo.to_dict())


# 싱글톤
memo_service = MemoService()