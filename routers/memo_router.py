from fastapi import APIRouter, status
from models.memo_model import MemoCreate, MemoResponse
from services.memo_service import memo_service


router = APIRouter(prefix="/elders", tags=["memos"])


@router.post(
    "/{elder_id}/memos",
    response_model=MemoResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_memo(
    elder_id: str,
    memo_data: MemoCreate,
    companion_id: str = "comp_777"
):
    """메모 생성"""
    return memo_service.create_memo(elder_id, memo_data, companion_id)