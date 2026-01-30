from abc import ABC, abstractmethod
from models.map_model import LatLng

class MapProviderBase(ABC):
    @abstractmethod
    def build_map_link(self, location: LatLng, label: str) -> str:
        ...

    @abstractmethod
    def build_roadview_link(self, location: LatLng) -> str:
        ...
