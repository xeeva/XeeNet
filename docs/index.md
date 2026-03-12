---
layout: default
title: XeeNet — Distributed AI Research at Scale
---

<div class="hero">
  <h1>XeeNet</h1>
  <p class="subtitle">
    A distributed platform for autonomous machine learning research.
    Donate your spare compute — CPU, GPU, or NPU — to run real ML experiments
    at global scale. Inspired by SETI@home and Karpathy's autoresearch.
  </p>
  <div class="hero-stats">
    <div class="hero-stat">
      <span class="number">~8,000</span>
      <span class="label">Lines of Code</span>
    </div>
    <div class="hero-stat">
      <span class="number">4</span>
      <span class="label">Agent Families</span>
    </div>
    <div class="hero-stat">
      <span class="number">110</span>
      <span class="label">Passing Tests</span>
    </div>
    <div class="hero-stat">
      <span class="number">0</span>
      <span class="label">External Dependencies*</span>
    </div>
  </div>
</div>

<div class="section">
  <p style="text-align: center; font-size: 0.85rem; color: var(--colour-text-muted);">
    *The desktop worker auto-downloads Python + PyTorch on first run. Users need nothing pre-installed.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>The Problem</h2>
  <p>
    Andrej Karpathy's <strong>autoresearch</strong> showed that ML experiments can be fully autonomous —
    a script runs a training loop for a fixed compute budget, reports a single comparable metric
    (<code>val_bpb</code>), and an agent decides what to try next. The bottleneck is compute:
    one machine can only run so many experiments.
  </p>
  <p>
    XeeNet removes that bottleneck. Instead of one machine, experiments run across a global
    grid of volunteer devices — like SETI@home, but for ML research. Researchers submit
    experiment campaigns, and the platform distributes bounded training tasks to workers worldwide.
  </p>
</div>

<div class="divider"></div>

<div class="section section-wide">
  <h2>How It Works</h2>
  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#128209;</span>
      <h3>Researchers Submit Briefs</h3>
      <p>
        A research brief describes the experiment campaign — the hypothesis, search space,
        and compute budget. The orchestrator decomposes it into bounded tasks with specific
        hyperparameter configurations.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#9881;</span>
      <h3>Orchestrator Generates Tasks</h3>
      <p>
        Each task is a self-contained training run: a Python script, a JSON config
        (learning rate, architecture, schedule), a time budget, and a seed for
        reproducibility. Tasks are queued and matched to available workers.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128187;</span>
      <h3>Workers Run Real Training</h3>
      <p>
        Desktop workers (Windows/Mac/Linux) poll for tasks and execute them in isolated
        subprocesses. The worker auto-downloads Python and PyTorch on first run — no
        setup required from the user.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128200;</span>
      <h3>Results Flow to the Dashboard</h3>
      <p>
        Each completed task reports metrics (val_bpb, train_loss, steps, wall time)
        via a single JSON line. The dashboard aggregates results across the campaign,
        identifying the best configurations.
      </p>
    </div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>End-to-End Pipeline</h2>
  <div class="pipeline-flow">
    <div class="pipeline-step">Research Brief</div>
    <span class="pipeline-arrow">&#10132;</span>
    <div class="pipeline-step">Orchestrator</div>
    <span class="pipeline-arrow">&#10132;</span>
    <div class="pipeline-step">Task Queue</div>
    <span class="pipeline-arrow">&#10132;</span>
    <div class="pipeline-step">Worker Nodes</div>
    <span class="pipeline-arrow">&#10132;</span>
    <div class="pipeline-step">Training Subprocess</div>
    <span class="pipeline-arrow">&#10132;</span>
    <div class="pipeline-step">Metrics JSON</div>
    <span class="pipeline-arrow">&#10132;</span>
    <div class="pipeline-step">Dashboard</div>
  </div>

  <div class="callout">
    <div class="callout-title">Autoresearch Pattern</div>
    <p>
      Every training task follows the autoresearch contract: fixed time budget, self-contained
      script, single comparable metric. The script exits gracefully at 90% of its budget,
      and the worker enforces a hard kill at budget + 15 seconds. This dual-deadline pattern
      ensures tasks always terminate and always produce results.
    </p>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Real Training, Not Simulation</h2>
  <p>
    XeeNet runs <strong>actual PyTorch training</strong> — not simulated metrics. The default
    experiment is a character-level transformer trained on TinyShakespeare, producing a
    real <code>val_bpb</code> (validation bits-per-byte) metric that measures genuine model quality.
  </p>

  <h3>Sample Results from a 10-Task Campaign</h3>
  <table>
    <thead>
      <tr>
        <th>Metric</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Tasks completed</td>
        <td><span class="metric-highlight">10 / 10</span></td>
      </tr>
      <tr>
        <td>Best val_bpb</td>
        <td><span class="metric-highlight">3.5705</span></td>
      </tr>
      <tr>
        <td>Standard deviation</td>
        <td>0.5622</td>
      </tr>
      <tr>
        <td>Hyperparameter configs</td>
        <td>10 distinct (varied lr, schedule, architecture)</td>
      </tr>
      <tr>
        <td>Training steps (best run)</td>
        <td>~1,500</td>
      </tr>
      <tr>
        <td>Wall time per task</td>
        <td>~9 seconds (CPU)</td>
      </tr>
    </tbody>
  </table>
  <p>
    Different hyperparameter configurations produce meaningfully different results — confirming
    the pipeline is capturing real signal, not noise.
  </p>
</div>

<div class="divider"></div>

<div class="section section-wide">
  <h2>Key Design Principles</h2>
  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#128274;</span>
      <h3>Zero-Setup Workers</h3>
      <p>
        The Electron desktop app auto-downloads an embedded Python 3.12 distribution and
        installs PyTorch on first run. Users just install the app and click "Start".
        GPU detection is automatic — NVIDIA GPUs get CUDA-enabled PyTorch.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128256;</span>
      <h3>Reproducible by Default</h3>
      <p>
        Every task carries a seed. The config generator uses <code>random.Random(seed)</code>
        for deterministic sampling. Training scripts set PyTorch seeds. Identical configs
        on identical hardware produce matching results.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128736;</span>
      <h3>Graceful Degradation</h3>
      <p>
        If PyTorch is unavailable, workers fall back to simulated metrics with a clear
        UI indicator. The platform never blocks on missing dependencies — it adapts
        and reports honestly.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128176;</span>
      <h3>Credits Economy</h3>
      <p>
        Workers earn credits for completed tasks. Researchers spend credits to submit
        campaigns. The economics agent handles metering, accounting, and fraud detection
        — keeping the marketplace fair.
      </p>
    </div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Technology Stack</h2>
  <table>
    <thead>
      <tr>
        <th>Layer</th>
        <th>Technology</th>
        <th>Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Backend API</td>
        <td>FastAPI + async SQLAlchemy + SQLite</td>
        <td>REST API, task orchestration, data persistence</td>
      </tr>
      <tr>
        <td>Dashboard</td>
        <td>HTMX + Jinja2 + Pico CSS</td>
        <td>Real-time web UI with auto-refreshing stats</td>
      </tr>
      <tr>
        <td>Desktop Worker</td>
        <td>Electron 28 + TypeScript</td>
        <td>Cross-platform worker with system tray integration</td>
      </tr>
      <tr>
        <td>Training Runtime</td>
        <td>PyTorch (CPU or CUDA)</td>
        <td>Real neural network training</td>
      </tr>
      <tr>
        <td>Agent Framework</td>
        <td>Python (custom BaseAgent ABC)</td>
        <td>Orchestrator, Worker, Portal, Economics agents</td>
      </tr>
      <tr>
        <td>Hardware Detection</td>
        <td>systeminformation (Node.js)</td>
        <td>CPU, RAM, GPU profiling on worker devices</td>
      </tr>
      <tr>
        <td>Config</td>
        <td>Pydantic Settings + YAML</td>
        <td>Type-safe configuration with validation</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Get Involved</h2>
  <p>
    XeeNet is in active development. The core pipeline — from research brief to real training
    results — is fully functional. We're looking for contributors, early testers, and researchers
    who want to run distributed ML experiments.
  </p>
  <p>
    <a href="https://github.com/xeeva/XeeNet">View the source on GitHub</a> or read the
    <a href="{{ '/architecture' | relative_url }}">architecture deep-dive</a> to understand
    how the system fits together.
  </p>
</div>
