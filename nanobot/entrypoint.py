#!/usr/bin/env python3
"""Create the smallest safe Railway config, then run pinned nanobot."""

from __future__ import annotations

import json
import os
from pathlib import Path


def build_config(port: int, access_token: str) -> dict:
    return {
        "channels": {
            "websocket": {
                "enabled": True,
                "host": "0.0.0.0",
                "port": port,
                "path": "/",
                "token": access_token,
                "websocketRequiresToken": True,
                "allowFrom": ["*"],
            }
        },
        "gateway": {"host": "127.0.0.1", "port": 18790},
        "tools": {"restrictToWorkspace": True},
    }


def main() -> None:
    access_token = os.environ.get("NANOBOT_ACCESS_TOKEN", "").strip()
    if len(access_token) < 20:
        raise SystemExit("NANOBOT_ACCESS_TOKEN must contain at least 20 characters")

    try:
        port = int(os.environ.get("PORT", "8765"))
    except ValueError as exc:
        raise SystemExit("PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise SystemExit("PORT must be between 1 and 65535")

    config_path = Path.home() / ".nanobot" / "config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(build_config(port, access_token), indent=2) + "\n")
    config_path.chmod(0o600)

    os.execvp(
        "nanobot",
        [
            "nanobot",
            "gateway",
            "--foreground",
            "--config",
            str(config_path),
            "--workspace",
            str(config_path.parent / "workspace"),
        ],
    )


if __name__ == "__main__":
    main()

