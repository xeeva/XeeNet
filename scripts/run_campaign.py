#!/usr/bin/env python3
"""Create and monitor a XeeNet research campaign.

Creates a research brief, triggers orchestration to generate tasks, and
optionally monitors progress until all tasks complete.

Usage:
    python scripts/run_campaign.py --num-tasks 50 --time-budget 300
    python scripts/run_campaign.py --num-tasks 10 --time-budget 60 --no-monitor
"""

from __future__ import annotations

import argparse
import asyncio
import sys
import time

import httpx


_DEFAULT_API_BASE = "http://localhost:8000"

_GOAL_DESCRIPTION = (
    "Across the full CharLM search space, which hyperparameters have "
    "the biggest impact on val_bpb? Run a comprehensive sweep covering "
    "learning rate, hidden size, number of layers, dropout, learning "
    "rate schedule, batch size, and context length."
)


async def check_server(client: httpx.AsyncClient) -> bool:
    """Return True if the server is reachable."""
    try:
        resp = await client.get("/health")
        return resp.status_code == 200
    except (httpx.ConnectError, httpx.ConnectTimeout):
        return False


async def create_campaign(
    client: httpx.AsyncClient,
    num_tasks: int,
    time_budget: int,
) -> tuple[str, str]:
    """Create a brief and orchestrate it into a campaign.

    Uses the dashboard form endpoint which creates the brief, calls
    orchestrate_brief(), and generates the experiment family + tasks
    in a single transaction.

    Returns (brief_id, family_id).
    """
    # Use the dashboard form endpoint — it creates the brief AND
    # orchestrates in one go (brief + family + tasks).
    form_data = {
        "goal_description": _GOAL_DESCRIPTION,
        "budget_credits": "5000.0",
        "target_hardware": "medium",
        "num_tasks": str(num_tasks),
        "time_budget": str(time_budget),
    }
    resp = await client.post(
        "/dashboard/briefs/create",
        data=form_data,
        follow_redirects=False,
    )
    # Dashboard returns a 303 redirect to /dashboard/briefs/<brief_id>.
    if resp.status_code not in (303, 200, 201):
        print(f"  ERROR: Orchestration returned {resp.status_code}")
        print(f"  {resp.text[:500]}")
        sys.exit(1)

    # Extract brief_id from the redirect Location header.
    brief_id = None
    location = resp.headers.get("location", "")
    if "/briefs/" in location:
        brief_id = location.rsplit("/briefs/", 1)[-1].rstrip("/")

    if brief_id:
        print(f"  Brief created: {brief_id}")

    # Find the experiment family linked to this brief.
    families_resp = await client.get("/api/v1/families")
    families_resp.raise_for_status()
    families = families_resp.json()

    family_id = None
    for fam in families:
        if brief_id and fam.get("brief_id") == brief_id:
            family_id = fam["family_id"]
            break

    if family_id is None and families:
        # Fall back to the most recently created family.
        family_id = families[0]["family_id"]
        if not brief_id:
            brief_id = families[0].get("brief_id", "unknown")

    if family_id is None:
        print("  ERROR: No experiment family found after orchestration.")
        sys.exit(1)

    return brief_id, family_id


async def monitor_progress(
    client: httpx.AsyncClient,
    family_id: str,
    poll_interval: float = 15.0,
) -> None:
    """Poll task statuses and print progress until all tasks complete."""
    print("\n  Monitoring progress (Ctrl+C to stop monitoring)...\n")
    start = time.time()

    while True:
        resp = await client.get("/api/v1/tasks", params={"family_id": family_id})
        resp.raise_for_status()
        tasks = resp.json()

        total = len(tasks)
        if total == 0:
            print("  No tasks found yet, waiting...")
            await asyncio.sleep(poll_interval)
            continue

        by_status: dict[str, int] = {}
        for t in tasks:
            status = t.get("status", "unknown")
            by_status[status] = by_status.get(status, 0) + 1

        completed = by_status.get("completed", 0) + by_status.get("failed", 0)
        pct = completed / total * 100
        elapsed = time.time() - start

        parts = [f"{s}: {c}" for s, c in sorted(by_status.items())]
        print(
            f"  [{elapsed:6.0f}s] {completed}/{total} done ({pct:5.1f}%) | "
            + " | ".join(parts)
        )

        terminal = {"completed", "failed", "cancelled"}
        if all(t.get("status") in terminal for t in tasks):
            print(f"\n  All {total} tasks finished in {elapsed:.0f}s.")
            succeeded = by_status.get("completed", 0)
            failed = by_status.get("failed", 0)
            print(f"  Succeeded: {succeeded}  Failed: {failed}")
            break

        await asyncio.sleep(poll_interval)


async def main(
    num_tasks: int,
    time_budget: int,
    api_base: str,
    monitor: bool,
) -> None:
    async with httpx.AsyncClient(base_url=api_base, timeout=30.0) as client:
        # 1. Check server is running.
        print("Checking server...")
        if not await check_server(client):
            print(f"ERROR: Server not reachable at {api_base}")
            print("Start it with: bash scripts/run_dev_server.sh")
            sys.exit(1)
        print("  Server is running.\n")

        # 2. Create campaign.
        print(f"Creating campaign ({num_tasks} tasks, {time_budget}s budget each)...")
        brief_id, family_id = await create_campaign(client, num_tasks, time_budget)

        # 3. Verify tasks were created.
        resp = await client.get("/api/v1/tasks", params={"family_id": family_id})
        resp.raise_for_status()
        tasks = resp.json()

        print(f"  Family ID: {family_id}")
        print(f"  Tasks created: {len(tasks)}")
        est_minutes = (num_tasks * time_budget) / (4 * 60)
        print(f"  Estimated duration with 4 workers: ~{est_minutes:.0f} min\n")

        print("To run workers:")
        print(f"  python scripts/run_worker.py --api-base {api_base}\n")
        print("To analyse results after completion:")
        print(f"  python scripts/analyse_campaign.py --family-id {family_id}\n")

        # 4. Monitor if requested.
        if monitor:
            try:
                await monitor_progress(client, family_id)
            except KeyboardInterrupt:
                print("\n  Monitoring stopped. Campaign continues in background.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create and monitor a XeeNet research campaign.",
    )
    parser.add_argument(
        "--num-tasks", type=int, default=50,
        help="Number of tasks to generate (default: 50)",
    )
    parser.add_argument(
        "--time-budget", type=int, default=300,
        help="Per-task time budget in seconds (default: 300)",
    )
    parser.add_argument(
        "--api-base", default=_DEFAULT_API_BASE,
        help=f"API server URL (default: {_DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--no-monitor", action="store_true",
        help="Exit after creating the campaign without monitoring progress",
    )
    args = parser.parse_args()

    try:
        asyncio.run(main(
            num_tasks=args.num_tasks,
            time_budget=args.time_budget,
            api_base=args.api_base,
            monitor=not args.no_monitor,
        ))
    except KeyboardInterrupt:
        print("\nCampaign runner stopped.")
