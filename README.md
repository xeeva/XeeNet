<p align="center">
  <strong>&#9670; XeeNet</strong>
</p>

<h3 align="center">Distributed AI Research at Scale</h3>

<p align="center">
  An open platform for autonomous machine learning experimentation.<br>
  Donate spare compute. Run real PyTorch training. Advance open science.
</p>

<p align="center">
  <a href="https://xeeva.github.io/XeeNet/">Documentation</a> &middot;
  <a href="https://xeeva.github.io/XeeNet/architecture/">Architecture</a> &middot;
  <a href="https://xeeva.github.io/XeeNet/training-pipeline/">Training Pipeline</a> &middot;
  <a href="https://xeeva.github.io/XeeNet/desktop-worker/">Desktop Worker</a> &middot;
  <a href="https://xeeva.github.io/XeeNet/roadmap/">Roadmap</a>
</p>

---

## What is XeeNet?

XeeNet is a distributed compute platform for ML research, inspired by [SETI@home](https://setiathome.berkeley.edu/) and Andrej Karpathy's [autoresearch](https://github.com/karpathy/autoresearch). Volunteers install a lightweight desktop app, donate idle CPU/GPU time, and the platform runs real neural network training across the global grid.

Researchers submit experiment campaigns. The orchestrator decomposes them into bounded, self-contained training tasks. Workers execute actual PyTorch training (not simulations), report metrics, and the dashboard aggregates results. A credits economy rewards contributors and funds research.

**This is not a concept.** The end-to-end pipeline is functional: research brief to real `val_bpb` metrics from distributed workers.

## Key Features

- **Real ML Training** -- Character-level transformer on TinyShakespeare with genuine `val_bpb` metrics. Not simulated.
- **Zero-Setup Desktop Worker** -- Electron app auto-downloads Python 3.12 + PyTorch on first run. NVIDIA GPU auto-detection installs CUDA-enabled PyTorch. Users click "Start" and contribute compute.
- **Autoresearch Contract** -- Every task is self-contained, has a fixed time budget, and reports a single comparable metric. Dual-deadline pattern (soft at 90%, hard kill at budget + 15s) guarantees termination.
- **Reproducible by Default** -- Seeded config generation, deterministic training. Same seed, same config, same results.
- **Multi-Agent Architecture** -- Orchestrator, Worker, Portal, and Economics agents with defined roles and shared memory.
- **Live Dashboard** -- HTMX + Jinja2 web UI with real-time stats, campaign results, worker monitoring, and credit tracking.
- **Credits Economy** -- Workers earn credits for completed tasks. Researchers spend credits to run campaigns. Anti-fraud verification built in.
- **Graceful Degradation** -- No PyTorch? Workers fall back to simulated metrics with a clear UI indicator. The platform never blocks.

## Screenshots

<table>
  <tr>
    <td><strong>Dashboard Overview</strong></td>
    <td><strong>Campaign Results</strong></td>
  </tr>
  <tr>
    <td>Platform stats with live worker count, task completion, and credits</td>
    <td>10/10 tasks completed, best val_bpb 3.5705, full hyperparameter breakdown</td>
  </tr>
</table>

<table>
  <tr>
    <td><strong>Desktop Worker (Connected)</strong></td>
    <td><strong>Desktop Worker (Training)</strong></td>
  </tr>
  <tr>
    <td>RTX 3080 detected, CUDA PyTorch ready, Real ML Training badge</td>
    <td>Active training: spawning train_char_lm.py with hyperparameter config</td>
  </tr>
</table>

> See the full [documentation site](https://xeeva.github.io/XeeNet/) for detailed screenshots and architecture diagrams.

## Architecture

```
Research Brief --> Orchestrator --> Task Queue --> Workers --> Training --> Metrics --> Dashboard
```

| Component | Technology | Role |
|-----------|-----------|------|
| Backend API | FastAPI + async SQLAlchemy + SQLite | REST API, orchestration, persistence |
| Dashboard | HTMX + Jinja2 + Pico CSS | Real-time web UI, campaign management |
| Desktop Worker | Electron 28 + TypeScript | Cross-platform worker with auto-setup |
| Training | PyTorch (CPU or CUDA) | Real neural network training |
| Agents | Python (BaseAgent ABC) | Orchestrator, Worker, Portal, Economics |
| Config | Pydantic Settings + YAML | Type-safe settings with validation |

## How It Works

1. **Researcher creates a brief** defining the experiment goal, compute budget, and task count
2. **Orchestrator decomposes** the brief into tasks, each with a unique hyperparameter config sampled from a defined search space (learning rate, architecture, schedule)
3. **Workers poll** for tasks and execute them as isolated Python subprocesses with dual deadlines
4. **Training script** runs a character-level transformer on TinyShakespeare, outputs metrics as a single JSON line to stdout
5. **Results aggregate** on the dashboard showing best config, mean/std val_bpb, and per-task breakdown

## Sample Results

From a real 10-task campaign:

| Metric | Value |
|--------|-------|
| Tasks completed | **10 / 10** |
| Best val_bpb | **3.5705** |
| Std deviation | 0.5622 |
| Configs tested | 10 distinct (varied lr, schedule, layers, heads, d_model) |
| Best config | lr=0.001248, step_decay, 2 layers, 4 heads, d_model=64 |
| Wall time per task | ~9s (CPU) |

## Quick Start

### Server

```bash
pip install -e ".[dev]"
uvicorn services.api.main:app --reload
# Dashboard at http://localhost:8000/dashboard
```

### Desktop Worker

```bash
cd desktop
npm install
npm run dev
```

Or download the portable `.exe` from releases. The app auto-downloads Python + PyTorch on first launch.

### Training Script (standalone)

```bash
pip install torch
python experiments/train_char_lm.py --config-file config.json
```

### Tests

```bash
pytest  # 110 tests, all passing
```

## Project Structure

```
agents/              Agent definitions (orchestrator, worker, portal, economics)
skills/              Reusable modules (task generation, result analysis, scheduling, credits)
services/            FastAPI backend, database, schemas, orchestration logic
  api/               REST API routers + HTMX dashboard + Jinja2 templates
  db/                Async SQLAlchemy + SQLite
experiments/         Self-contained training scripts
desktop/             Electron desktop worker (TypeScript)
config/              Pydantic settings + YAML config
tests/               Test suite (110 tests)
static/              Dashboard CSS/JS assets
```

## Contributing

Contributions welcome in any area:

- **New experiment templates** following the autoresearch contract (fixed budget, self-contained, single metric)
- **Platform improvements** to the dashboard, API, or worker capabilities
- **Cross-platform testing** of the desktop worker on diverse hardware
- **Research ideas** for what experiments the grid should run

## License

MIT

## Links

- [Documentation](https://xeeva.github.io/XeeNet/) -- Full platform writeup with architecture diagrams and screenshots
- [Vision & Market](https://xeeva.github.io/XeeNet/vision/) -- Scale economics and the case for distributed autoresearch
- [Roadmap](https://xeeva.github.io/XeeNet/roadmap/) -- Current state and future plans
