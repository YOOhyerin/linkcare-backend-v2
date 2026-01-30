import httpx
from typing import Optional
from core.config import settings
from core.errors import MisconfiguredError, ExternalServiceError
from models.map_model import LatLng, KakaoAddress

class KakaoLocalClient:
    """
    Kakao Local API (coord2address) 호출 클라이언트.
    - GET https://dapi.kakao.com/v2/local/geo/coord2address.json?x={lng}&y={lat}
    - Header: Authorization: KakaoAK {REST_API_KEY}
    """
    def __init__(self):
        if not settings.KAKAO_REST_API_KEY:
            raise MisconfiguredError("KAKAO_REST_API_KEY is missing in environment variables.")
        self._base = settings.KAKAO_LOCAL_BASE_URL
        self._headers = {"Authorization": f"KakaoAK {settings.KAKAO_REST_API_KEY}"}
        self._timeout = settings.HTTP_TIMEOUT_SEC

    async def coord_to_address(self, location: LatLng) -> Optional[KakaoAddress]:
        url = f"{self._base}/v2/local/geo/coord2address.json"
        params = {"x": str(location.lng), "y": str(location.lat)}  # x=경도, y=위도

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                r = await client.get(url, headers=self._headers, params=params)
                if r.status_code != 200:
                    raise ExternalServiceError(f"Kakao Local API failed: HTTP {r.status_code}")
                data = r.json()

            docs = data.get("documents") or []
            if not docs:
                return KakaoAddress()

            doc0 = docs[0]
            address = doc0.get("address") or {}
            road = doc0.get("road_address") or {}

            return KakaoAddress(
                address_name=address.get("address_name"),
                road_address_name=road.get("address_name"),
            )

        except httpx.TimeoutException:
            raise ExternalServiceError("Kakao Local API timeout")
        except httpx.HTTPError as e:
            raise ExternalServiceError(f"Kakao Local API http error: {e}")
