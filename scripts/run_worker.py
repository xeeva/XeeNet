#!/usr/bin/env python3
"""Run a single XeeNet worker agent.

Connects to the API server, registers with detected hardware profile,
then polls for tasks and executes them until interrupted.

Usage:
    python scripts/run_worker.py
    python scripts/run_worker.py --api-base http://192.168.1.10:8000
"""

from __future__ import annotations

import argparse
import asyncio

from agents.worker.worker_agent import WorkerAgent


async def main(api_base: str) -> None:
    worker = WorkerAgent(api_base=api_base)
    try:
        await worker.run()
    except KeyboardInterrupt:
        pass
    finally:
        await worker.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a XeeNet worker agent.")
    parser.add_argument(
        "--api-base",
        default="http://localhost:8000",
        help="Base URL of the XeeNet API server (default: http://localhost:8000)",
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(args.api_base))
    except KeyboardInterrupt:
        print("\nWorker stopped.")
