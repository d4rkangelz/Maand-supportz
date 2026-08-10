#!/usr/bin/env python3
"""Validate deployer input, create the Red instance, and start supervision."""

from __future__ import annotations

import os
import subprocess
import sys


def main() -> None:
    token = os.environ.get("DISCORD_TOKEN", "").strip()
    prefix = os.environ.get("DISCORD_PREFIX", "!").strip()
    if len(token) < 20:
        raise SystemExit("DISCORD_TOKEN is required and appears too short")
    if not prefix or len(prefix) > 20:
        raise SystemExit("DISCORD_PREFIX must contain 1 to 20 characters")

    subprocess.run(
        [
            "redbot-setup",
            "--no-prompt",
            "--instance-name",
            "railway",
            "--data-path",
            "/data",
            "--backend",
            "json",
            "--overwrite-existing-instance",
        ],
        check=True,
    )

    command = [
        "redbot",
        "railway",
        "--no-prompt",
        "--token",
        token,
        "--prefix",
        prefix,
    ]
    os.environ["REDBOT_COMMAND_JSON"] = __import__("json").dumps(command)
    os.execv(sys.executable, [sys.executable, "/usr/local/lib/railway-redbot/supervisor.py"])


if __name__ == "__main__":
    main()

