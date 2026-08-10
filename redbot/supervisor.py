#!/usr/bin/env python3
"""Supervise Red and expose truthful process health/readiness over HTTP."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STARTED_AT = time.monotonic()
READY_AFTER_SECONDS = 10
child: subprocess.Popen | None = None


def child_alive() -> bool:
    return child is not None and child.poll() is None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - stdlib API
        alive = child_alive()
        ready = alive and time.monotonic() - STARTED_AT >= READY_AFTER_SECONDS
        if self.path == "/healthz":
            code, payload = (200 if alive else 503), {"alive": alive}
        elif self.path == "/readyz":
            code, payload = (200 if ready else 503), {"ready": ready, "alive": alive}
        else:
            code, payload = 404, {"error": "not found"}
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        return


def terminate(signum: int, _frame: object) -> None:
    if child_alive():
        child.send_signal(signum)


def main() -> int:
    global child
    command = json.loads(os.environ["REDBOT_COMMAND_JSON"])
    if not isinstance(command, list) or not all(isinstance(arg, str) for arg in command):
        raise SystemExit("REDBOT_COMMAND_JSON must be a JSON string array")

    child = subprocess.Popen(command)
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, terminate)

    port = int(os.environ.get("PORT", "8080"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        return child.wait()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())

