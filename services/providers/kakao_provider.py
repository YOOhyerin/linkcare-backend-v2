from urllib.parse import quote
from models.map_model import LatLng
from services.providers.base import MapProviderBase

class KakaoMapProvider(MapProviderBase):
    """
    Kakao 지도 바로가기 URL 패턴 기반 링크 생성.
    - /link/map/{이름},{위도},{경도}
    - /link/roadview/{위도},{경도}
    """
    BASE = "https://map.kakao.com/link"

    def build_map_link(self, location: LatLng, label: str) -> str:
        safe_label = quote(label, safe="")
        return f"{self.BASE}/map/{safe_label},{location.lat},{location.lng}"

    def build_roadview_link(self, location: LatLng) -> str:
        return f"{self.BASE}/roadview/{location.lat},{location.lng}"
