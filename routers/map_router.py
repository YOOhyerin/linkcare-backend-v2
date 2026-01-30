from fastapi import APIRouter
from models.map_model import MapCreateRequest, MapCreateResponse
from services.map_service import MapService
from services.providers.kakao_provider import KakaoMapProvider
from services.kakao_local_client import KakaoLocalClient

router = APIRouter(tags=["map"])

# 간단 MVP: 싱글톤 서비스 구성
_service = MapService(
    provider=KakaoMapProvider(),
    kakao_local=KakaoLocalClient(),
)

@router.post("/map", response_model=MapCreateResponse)
async def create_map(req: MapCreateRequest):
    return await _service.create_map(req)
