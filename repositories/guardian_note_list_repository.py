from typing import List, Tuple, Dict


class GuardianNoteListRepository:
    """보호자 메모 목록 조회 전용 저장소"""
    
    def __init__(self):
        # guardian_note_repository와 데이터 공유
        from repositories.guardian_note_repository import guardian_note_repository
        self._note_repo = guardian_note_repository
    
    def find_by_elder_id(self, elder_id: str, page: int = 1, limit: int = 20) -> Tuple[List[Dict], int]:
        """어르신의 보호자 메모 목록 조회"""
        # guardian_note_repository의 데이터에 접근
        all_notes = [
            note.to_dict() 
            for note in self._note_repo._notes.values() 
            if note.elder_id == elder_id
        ]
        
        # 최신순 정렬
        all_notes.sort(key=lambda x: x['created_at'], reverse=True)
        
        total = len(all_notes)
        
        # 페이지네이션
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_notes = all_notes[start_idx:end_idx]
        
        return page_notes, total


# 싱글톤
guardian_note_list_repository = GuardianNoteListRepository()