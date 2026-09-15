from typing import Any

from pydantic import BaseModel


class TriggerRequest(BaseModel):
    trigger: str
    payload: dict[str, Any] = {}


class TriggerResponse(BaseModel):
    ok: bool
    message: str
    state: dict[str, Any]


class NewSessionResponse(BaseModel):
    session_id: str
    state: dict[str, Any]
