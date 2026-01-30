from models.map_model import MapCreateRequest, MapCreateResponse, KakaoLinks
from services.providers.kakao_provider import KakaoMapProvider
from services.kakao_local_client import KakaoLocalClient

class MapService:
    def __init__(self, provider: KakaoMapProvider, kakao_local: KakaoLocalClient):
        self._provider = provider
        self._kakao_local = kakao_local

    async def create_map(self, req: MapCreateRequest) -> MapCreateResponse:
        links = KakaoLinks(
            map=self._provider.build_map_link(req.location, req.label),
            roadview=self._provider.build_roadview_link(req.location),
        )

        address = None
        if req.include_address:
            address = await self._kakao_local.coord_to_address(req.location)

        return MapCreateResponse(
            location=req.location,
            links=links,
            address=address,
        )
