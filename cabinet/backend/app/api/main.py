"""HTTP + WebSocket API for Easy Craps.

This is the language-agnostic surface: any RL agent (Python, or otherwise)
can drive a table by POSTing named triggers, exactly like the buttons in the
React frontend. See docs/RULES.md for what each trigger does and
backend/README.md for the endpoint list.
"""
from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from easycraps import Game, TriggerError

from .schemas import NewSessionResponse, TriggerRequest, TriggerResponse

app = FastAPI(title="Easy Craps API", version="1.0.0")

RULES_PATH = Path(__file__).resolve().parents[4] / "docs" / "RULES.md"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_sessions: dict[str, Game] = {}


@app.get("/rules", response_class=Response)
def get_rules() -> Response:
    """The rulebook (docs/RULES.md), served as-is for the frontend Help page."""
    if not RULES_PATH.exists():
        raise HTTPException(status_code=404, detail="Rulebook not found.")
    return Response(content=RULES_PATH.read_text(encoding="utf-8"), media_type="text/markdown")


def _get_game(session_id: str) -> Game:
    game = _sessions.get(session_id)
    if game is None:
        raise HTTPException(status_code=404, detail=f"Unknown session_id: {session_id}")
    return game


@app.post("/sessions", response_model=NewSessionResponse)
def create_session() -> NewSessionResponse:
    session_id = uuid.uuid4().hex
    game = Game()
    _sessions[session_id] = game
    return NewSessionResponse(session_id=session_id, state=game.state.to_dict())


@app.get("/sessions/{session_id}/state")
def get_state(session_id: str) -> dict[str, Any]:
    return _get_game(session_id).state.to_dict()


@app.get("/sessions/{session_id}/triggers")
def list_triggers(session_id: str) -> dict[str, Any]:
    return {"triggers": _get_game(session_id).trigger_names}


@app.post("/sessions/{session_id}/trigger", response_model=TriggerResponse)
def fire_trigger(session_id: str, req: TriggerRequest) -> TriggerResponse:
    game = _get_game(session_id)
    try:
        result = game.apply(req.trigger, req.payload)
    except TriggerError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return TriggerResponse(**result)


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str) -> dict[str, bool]:
    _sessions.pop(session_id, None)
    return {"ok": True}


@app.websocket("/sessions/{session_id}/ws")
async def session_ws(websocket: WebSocket, session_id: str) -> None:
    """Push-based mirror of the REST trigger endpoint, for the live UI.

    Client sends {"trigger": str, "payload": {...}}; server replies with the
    same TriggerResponse shape after every message, so the UI can stay a
    thin renderer of engine state.
    """
    game = _sessions.get(session_id)
    if game is None:
        await websocket.close(code=4404)
        return
    await websocket.accept()
    await websocket.send_json({"ok": True, "message": game.state.message, "state": game.state.to_dict()})
    try:
        while True:
            data = await websocket.receive_json()
            trigger = data.get("trigger")
            payload = data.get("payload") or {}
            try:
                result = game.apply(trigger, payload)
            except TriggerError as exc:
                result = {"ok": False, "message": str(exc), "state": game.state.to_dict()}
            await websocket.send_json(result)
    except WebSocketDisconnect:
        pass
