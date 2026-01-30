from __future__ import annotations

import threading
from typing import Dict, Optional

from models.domain import ChecklistResult


class InMemoryChecklistRepository:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._store: Dict[str, ChecklistResult] = {}

    def save(self, chk: ChecklistResult) -> ChecklistResult:
        with self._lock:
            self._store[chk.checklist_id] = chk
            return chk

    def get(self, checklist_id: str) -> Optional[ChecklistResult]:
        with self._lock:
            return self._store.get(checklist_id)
