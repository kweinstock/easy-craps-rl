# Cabinet (backend + frontend)

The live, playable Easy Craps table: [`backend/`](backend) (FastAPI
HTTP/WebSocket server over the [`easycraps`](../easycraps) library) and
[`frontend/`](frontend) (the React UI). See
[`../docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md) for how these two fit
into the rest of the project.

## First-time setup

```bash
pip install -r backend/requirements.txt   # also installs easycraps (editable)
npm install --prefix frontend
```

## Run both together

```bash
python run.py
```

This starts the backend on `http://localhost:8000` and the frontend dev
server, streams both logs (prefixed `[backend]` / `[frontend]`), and prints
the frontend URL to open once it's up. Ctrl+C stops both.

To run them separately instead (e.g. in two terminals), see
[`backend/README.md`](backend/README.md) and use `npm run dev --prefix
frontend` (or `cd frontend && npm run dev`).
