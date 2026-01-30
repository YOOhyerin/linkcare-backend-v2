from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated

class LatLng(BaseModel):
    lat: Annotated[float, Field(ge=-90, le=90)]
    lng: Annotated[float, Field(ge=-180, le=180)]

class MapCreateRequest(BaseModel):
    location: LatLng
    label: Annotated[str, Field(default="내 위치", max_length=40)]
    include_address: bool = True

class KakaoLinks(BaseModel):
    map: str
    roadview: str

class KakaoAddress(BaseModel):
    address_name: Optional[str] = None
    road_address_name: Optional[str] = None

class MapCreateResponse(BaseModel):
    provider: str = "kakao"
    location: LatLng
    links: KakaoLinks
    address: Optional[KakaoAddress] = None
