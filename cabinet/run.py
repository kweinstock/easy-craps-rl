#!/usr/bin/env python3
"""Run the Easy Craps cabinet (backend + frontend) together for local dev.

    python run.py

Starts the FastAPI backend (uvicorn, port 8000) and the Vite frontend dev
server as subprocesses, streams both logs with a prefix so you can tell
them apart, and prints the frontend URL to open once it's ready. Ctrl+C
stops both.

Assumes dependencies are already installed:
    pip install -r backend/requirements.txt
    npm install --prefix frontend
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
URL_RE = re.compile(r"(https?://\S+)")


def stream_output(prefix: str, pipe, on_url=None) -> None:
    for line in iter(pipe.readline, ""):
        print(f"[{prefix}] {line}", end="")
        if on_url and "Local" in line:
            clean_line = ANSI_RE.sub("", line)
            match = URL_RE.search(clean_line)
            if match:
                on_url(match.group(1))
    pipe.close()


def main() -> int:
    npm = shutil.which("npm")
    if npm is None:
        print("npm not found on PATH — install Node.js first.", file=sys.stderr)
        return 1

    print(f"Starting backend  (uvicorn) — http://localhost:8000")
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.api.main:app", "--reload", "--port", "8000"],
        cwd=BACKEND_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )

    print("Starting frontend (vite)...")
    frontend = subprocess.Popen(
        [npm, "run", "dev"],
        cwd=FRONTEND_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )

    frontend_url_found = threading.Event()

    def on_frontend_url(url: str) -> None:
        if not frontend_url_found.is_set():
            frontend_url_found.set()
            print(f"\n  Easy Craps cabinet is ready --> {url}\n")

    threading.Thread(target=stream_output, args=("backend", backend.stdout), daemon=True).start()
    threading.Thread(
        target=stream_output, args=("frontend", frontend.stdout, on_frontend_url), daemon=True
    ).start()

    if not frontend_url_found.wait(timeout=20):
        print("\n  Frontend didn't report a URL yet — check the logs above; "
              "it's likely at http://localhost:5173\n")

    try:
        backend.wait()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nStopping backend and frontend...")
        for proc in (frontend, backend):
            if proc.poll() is None:
                proc.terminate()
        for proc in (frontend, backend):
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
