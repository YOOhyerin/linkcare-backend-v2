from __future__ import annotations

import threading
from typing import Dict, Optional

from models.domain import CompanionRequest


class InMemoryRequestRepository:
    """
    DB 대신 메모리에 저장.
    - 서버 재시작 시 초기화됨
    - 단순 MVP 용도
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._store: Dict[str, CompanionRequest] = {}

    def save(self, req: CompanionRequest) -> CompanionRequest:
        with self._lock:
            self._store[req.id] = req
            return req

    def get(self, request_id: str) -> Optional[CompanionRequest]:
        with self._lock:
            return self._store.get(request_id)
