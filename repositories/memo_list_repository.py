from typing import List, Tuple, Dict


class MemoListRepository:
    """메모 목록 조회 전용 저장소"""
    
    def __init__(self):
        # memo_repository와 데이터 공유를 위해 같은 저장소 참조
        from repositories.memo_repository import memo_repository
        self._memo_repo = memo_repository
    
    def find_by_elder_id(self, elder_id: str, page: int = 1, limit: int = 20) -> Tuple[List[Dict], int]:
        """어르신의 메모 목록 조회"""
        # memo_repository의 데이터에 접근
        all_memos = [
            memo.to_dict() 
            for memo in self._memo_repo._memos.values() 
            if memo.elder_id == elder_id
        ]
        
        # 최신순 정렬
        all_memos.sort(key=lambda x: x['created_at'], reverse=True)
        
        total = len(all_memos)
        
        # 페이지네이션
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_memos = all_memos[start_idx:end_idx]
        
        return page_memos, total


# 싱글톤
memo_list_repository = MemoListRepository()