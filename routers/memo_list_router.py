from fastapi import APIRouter, status, Query
from models.memo_list_model import MemoListResponse
from services.memo_list_service import memo_list_service


router = APIRouter(prefix="/elders", tags=["memos"])


@router.get(
    "/{elder_id}/memos",
    response_model=MemoListResponse,
    status_code=status.HTTP_200_OK
)
async def get_memos(
    elder_id: str,
    page: int = Query(1, ge=1, description="페이지 번호 (기본값: 1)"),
    limit: int = Query(20, ge=1, le=100, description="페이지당 항목 수 (기본값: 20)")
):
    """메모 목록 조회"""
    return memo_list_service.get_memos(elder_id, page, limit)