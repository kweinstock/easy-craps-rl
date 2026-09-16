"""ActionResult — what every Table method returns."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ActionResult:
    """What every Table method returns."""

    ok: bool
    message: str
    state: dict[str, Any]

    def __bool__(self) -> bool:
        return self.ok
