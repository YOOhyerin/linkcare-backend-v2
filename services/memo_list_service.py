from models.memo_list_model import MemoListResponse, MemoItem
from repositories.memo_list_repository import memo_list_repository


class MemoListService:
    """메모 목록 조회 전용 서비스"""
    
    def __init__(self):
        self.repository = memo_list_repository
    
    def get_memos(self, elder_id: str, page: int = 1, limit: int = 20) -> MemoListResponse:
        """메모 목록 조회"""
        memos, total = self.repository.find_by_elder_id(elder_id, page, limit)
        
        items = [MemoItem(**memo) for memo in memos]
        
        return MemoListResponse(
            items=items,
            pagination={
                "total": total,
                "page": page,
                "limit": limit
            }
        )


# 싱글톤
memo_list_service = MemoListService()