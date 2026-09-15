from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_full_session_flow():
    r = client.post("/sessions")
    assert r.status_code == 200
    session_id = r.json()["session_id"]

    r = client.post(
        f"/sessions/{session_id}/trigger",
        json={"trigger": "add_funds", "payload": {"amount": 50}},
    )
    assert r.status_code == 200
    assert r.json()["state"]["credit"] == 50

    r = client.post(
        f"/sessions/{session_id}/trigger",
        json={"trigger": "place_bet", "payload": {"spot": "pass", "amount": 10}},
    )
    assert r.json()["state"]["bets"]["pass"] == 10

    r = client.post(
        f"/sessions/{session_id}/trigger",
        json={"trigger": "roll", "payload": {"d1": 3, "d2": 4}},
    )
    body = r.json()
    assert body["state"]["last_roll"]["total"] == 7

    r = client.get(f"/sessions/{session_id}/state")
    assert r.status_code == 200

    r = client.delete(f"/sessions/{session_id}")
    assert r.json() == {"ok": True}


def test_unknown_trigger_is_400():
    r = client.post("/sessions")
    session_id = r.json()["session_id"]
    r = client.post(
        f"/sessions/{session_id}/trigger",
        json={"trigger": "nope", "payload": {}},
    )
    assert r.status_code == 400


def test_unknown_session_is_404():
    r = client.get("/sessions/does-not-exist/state")
    assert r.status_code == 404
