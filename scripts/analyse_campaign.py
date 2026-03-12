#!/usr/bin/env python3
"""Analyse results from a completed XeeNet research campaign.

Fetches results via the API, computes factor analysis across
hyperparameters, identifies top configurations, checks reproducibility,
and exports a JSON report.

Usage:
    python scripts/analyse_campaign.py --family-id <family_id>
    python scripts/analyse_campaign.py --family-id abc123 --export results.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime

import httpx

from services.schemas import TaskResult
from skills.result_analysis.analysis_utils import (
    aggregate_results,
    best_config,
    detect_anomalies,
)


_DEFAULT_API_BASE = "http://localhost:8000"

# Hyperparameters produced by CharLMConfigGenerator.
_HYPERPARAMS = [
    "lr",
    "lr_schedule",
    "n_layers",
    "n_heads",
    "d_model",
    "d_ff",
    "batch_size",
    "context_length",
]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _std(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mu = _mean(values)
    return (sum((v - mu) ** 2 for v in values) / len(values)) ** 0.5


def fetch_results(client: httpx.Client, family_id: str) -> list[TaskResult]:
    """Fetch all results for a campaign family."""
    resp = client.get(
        "/api/v1/results",
        params={"family_id": family_id, "limit": 1000},
    )
    resp.raise_for_status()
    return [TaskResult(**r) for r in resp.json()]


def fetch_family(client: httpx.Client, family_id: str) -> dict:
    """Fetch the experiment family metadata."""
    resp = client.get(f"/api/v1/families/{family_id}")
    resp.raise_for_status()
    return resp.json()


def print_summary(results: list[TaskResult], metric: str) -> dict:
    """Print and return summary statistics."""
    agg = aggregate_results(results, metric)
    successful = [r for r in results if r.success]
    failed = len(results) - len(successful)

    print("=" * 60)
    print("  CAMPAIGN SUMMARY")
    print("=" * 60)
    print(f"  Total results:   {len(results)}")
    print(f"  Successful:      {len(successful)}")
    print(f"  Failed:          {failed}")
    print(f"  Metric:          {metric}")
    print(f"  Mean:            {agg['mean']:.4f}")
    print(f"  Std dev:         {agg['std']:.4f}")
    print(f"  Min (best):      {agg['min']:.4f}")
    print(f"  Max (worst):     {agg['max']:.4f}")
    print()
    return agg


def factor_analysis(results: list[TaskResult], metric: str) -> dict:
    """Group results by each hyperparameter value and compute mean metric.

    Returns a dict of {param_name: {value: {mean, std, count, spread}}}.
    """
    successful = [r for r in results if r.success and metric in r.metrics]

    analysis: dict[str, dict] = {}

    for param in _HYPERPARAMS:
        groups: dict[str, list[float]] = defaultdict(list)
        for r in successful:
            val = r.config.get(param)
            if val is not None:
                groups[str(val)].append(r.metrics[metric])

        if not groups:
            continue

        param_analysis: dict[str, dict] = {}
        means: list[float] = []
        for val_str, metrics_list in sorted(groups.items()):
            m = _mean(metrics_list)
            means.append(m)
            param_analysis[val_str] = {
                "mean": round(m, 4),
                "std": round(_std(metrics_list), 4),
                "count": len(metrics_list),
            }

        spread = max(means) - min(means) if len(means) > 1 else 0.0
        analysis[param] = {
            "values": param_analysis,
            "spread": round(spread, 4),
        }

    return analysis


def print_factor_analysis(analysis: dict) -> None:
    """Print factor analysis sorted by impact (spread)."""
    print("=" * 60)
    print("  FACTOR ANALYSIS (sorted by impact)")
    print("=" * 60)

    ranked = sorted(analysis.items(), key=lambda x: x[1]["spread"], reverse=True)

    for rank, (param, data) in enumerate(ranked, 1):
        spread = data["spread"]
        print(f"\n  #{rank}  {param}  (spread: {spread:.4f} val_bpb)")
        print(f"  {'Value':<20} {'Mean':>8} {'Std':>8} {'Count':>6}")
        print(f"  {'-'*20} {'-'*8} {'-'*8} {'-'*6}")

        # Sort by mean (best first for lower-is-better).
        sorted_vals = sorted(data["values"].items(), key=lambda x: x[1]["mean"])
        for val_str, stats in sorted_vals:
            label = val_str[:20]
            print(
                f"  {label:<20} {stats['mean']:>8.4f} {stats['std']:>8.4f} "
                f"{stats['count']:>6}"
            )

    print()


def print_top_configs(results: list[TaskResult], metric: str, top_n: int = 5) -> list[dict]:
    """Print the top N performing configurations."""
    successful = [r for r in results if r.success and metric in r.metrics]
    ranked = sorted(successful, key=lambda r: r.metrics[metric])

    print("=" * 60)
    print(f"  TOP {top_n} CONFIGURATIONS")
    print("=" * 60)

    top = []
    for i, r in enumerate(ranked[:top_n], 1):
        val_bpb = r.metrics[metric]
        print(f"\n  #{i}  {metric} = {val_bpb:.4f}  (task: {r.task_id})")
        # Print key hyperparameters.
        for param in _HYPERPARAMS:
            val = r.config.get(param)
            if val is not None:
                print(f"       {param}: {val}")
        top.append({
            "rank": i,
            "task_id": r.task_id,
            "metric_value": val_bpb,
            "config": {p: r.config.get(p) for p in _HYPERPARAMS if p in r.config},
            "seeds": r.seeds,
        })

    print()
    return top


def check_reproducibility(results: list[TaskResult], metric: str) -> list[dict]:
    """Check if tasks sharing the same seed produce identical results."""
    by_seed: dict[int, list[TaskResult]] = defaultdict(list)
    for r in results:
        if r.success and metric in r.metrics and r.seeds:
            by_seed[r.seeds[0]].append(r)

    # Only look at seeds that appear more than once.
    duplicates = {s: rs for s, rs in by_seed.items() if len(rs) > 1}

    if not duplicates:
        print("=" * 60)
        print("  REPRODUCIBILITY CHECK")
        print("=" * 60)
        print("  No duplicate seeds found — cannot verify reproducibility.")
        print()
        return []

    print("=" * 60)
    print("  REPRODUCIBILITY CHECK")
    print("=" * 60)

    checks = []
    for seed, rs in sorted(duplicates.items()):
        vals = [r.metrics[metric] for r in rs]
        spread = max(vals) - min(vals)
        reproducible = spread < 0.01  # Tolerance for floating-point differences.
        status = "PASS" if reproducible else "FAIL"
        print(
            f"  Seed {seed}: {len(rs)} runs, {metric} values = "
            f"{[round(v, 4) for v in vals]}, spread = {spread:.4f}  [{status}]"
        )
        checks.append({
            "seed": seed,
            "count": len(rs),
            "values": vals,
            "spread": spread,
            "reproducible": reproducible,
        })

    print()
    return checks


def print_anomalies(results: list[TaskResult], metric: str) -> list[str]:
    """Detect and print anomalous results."""
    anomalies = detect_anomalies(results, metric, z_threshold=2.0)

    if not anomalies:
        return []

    print("=" * 60)
    print(f"  ANOMALOUS RESULTS ({len(anomalies)} flagged)")
    print("=" * 60)
    ids = []
    for r in anomalies:
        val = r.metrics.get(metric, 0.0)
        print(f"  Task {r.task_id}: {metric} = {val:.4f}")
        ids.append(r.task_id)
    print()
    return ids


def export_report(
    family_id: str,
    summary: dict,
    factor_data: dict,
    top_configs: list[dict],
    repro_checks: list[dict],
    anomaly_ids: list[str],
    output_path: str,
) -> None:
    """Export the full analysis report as JSON."""
    report = {
        "family_id": family_id,
        "generated_at": datetime.utcnow().isoformat(),
        "summary": summary,
        "factor_analysis": factor_data,
        "top_configs": top_configs,
        "reproducibility": repro_checks,
        "anomaly_task_ids": anomaly_ids,
    }
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"  Report exported to: {output_path}")


def main(family_id: str, api_base: str, export_path: str | None) -> None:
    with httpx.Client(base_url=api_base, timeout=30.0) as client:
        # Fetch data.
        print(f"Fetching results for family {family_id}...\n")
        results = fetch_results(client, family_id)

        if not results:
            print("ERROR: No results found. Is the campaign complete?")
            sys.exit(1)

        try:
            family = fetch_family(client, family_id)
            metric = family.get("metric_name", "val_bpb")
        except httpx.HTTPStatusError:
            metric = "val_bpb"

        # Analysis.
        summary = print_summary(results, metric)
        factor_data = factor_analysis(results, metric)
        print_factor_analysis(factor_data)
        top_configs = print_top_configs(results, metric)
        repro_checks = check_reproducibility(results, metric)
        anomaly_ids = print_anomalies(results, metric)

        # Best config via existing utility.
        best = best_config(results, metric, lower_is_better=True)
        if best:
            print("=" * 60)
            print("  OVERALL BEST CONFIGURATION")
            print("=" * 60)
            print(f"  Task ID:    {best['task_id']}")
            print(f"  {metric}:   {best['metric_value']:.4f}")
            print(f"  Seeds:      {best['seeds']}")
            for k, v in best["config"].items():
                if k in _HYPERPARAMS:
                    print(f"  {k}: {v}")
            print()

        # Export if requested.
        if export_path:
            export_report(
                family_id, summary, factor_data,
                top_configs, repro_checks, anomaly_ids, export_path,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse results from a XeeNet research campaign.",
    )
    parser.add_argument(
        "--family-id", required=True,
        help="Experiment family ID to analyse",
    )
    parser.add_argument(
        "--api-base", default=_DEFAULT_API_BASE,
        help=f"API server URL (default: {_DEFAULT_API_BASE})",
    )
    parser.add_argument(
        "--export", default=None, metavar="FILE",
        help="Export analysis report to JSON file",
    )
    args = parser.parse_args()

    main(
        family_id=args.family_id,
        api_base=args.api_base,
        export_path=args.export,
    )
