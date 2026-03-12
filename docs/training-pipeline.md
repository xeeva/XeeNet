---
layout: default
title: Training Pipeline - XeeNet
---

<div class="page-header">
  <h1>Real ML Training Pipeline</h1>
  <p class="lead">
    From hyperparameter search space to real val_bpb metrics: how XeeNet runs
    actual PyTorch training across distributed workers.
  </p>
</div>

<div class="section">
  <h2>The Autoresearch Contract</h2>
  <p>
    XeeNet's training pipeline follows the <strong>autoresearch pattern</strong> pioneered
    by Andrej Karpathy: every experiment is a self-contained script that runs for a fixed
    compute budget and reports a single comparable metric.
  </p>

  <div class="card-grid">
    <div class="card">
      <h3>Fixed Compute Budget</h3>
      <p>
        Each task has a <code>time_budget_seconds</code>. The script exits
        gracefully at 90% of the budget. The worker enforces a hard kill
        at budget + 15 seconds. Tasks always terminate.
      </p>
    </div>
    <div class="card">
      <h3>Self-Contained Script</h3>
      <p>
        The training script (<code>train_char_lm.py</code>) uses only stdlib + PyTorch.
        No XeeNet imports, no framework dependencies. It downloads its own dataset
        on first run. Move it to any machine and it works.
      </p>
    </div>
    <div class="card">
      <h3>Single Comparable Metric</h3>
      <p>
        Every task reports <code>val_bpb</code> (validation bits-per-byte), a
        normalised measure of model quality. Lower is better. Different architectures
        and hyperparameters are directly comparable on this metric.
      </p>
    </div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Hyperparameter Search Space</h2>
  <p>
    The <code>CharLMConfigGenerator</code> defines the search space for character-level
    language model experiments. Each task samples a unique configuration from this space
    using a deterministic seed.
  </p>

  <table>
    <thead>
      <tr>
        <th>Parameter</th>
        <th>Range / Choices</th>
        <th>Sampling</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>lr</code></td>
        <td>[1e-4, 1e-2]</td>
        <td>Log-uniform</td>
      </tr>
      <tr>
        <td><code>lr_schedule</code></td>
        <td>cosine, linear, step_decay</td>
        <td>Uniform choice</td>
      </tr>
      <tr>
        <td><code>n_layers</code></td>
        <td>2, 4, 6</td>
        <td>Uniform choice</td>
      </tr>
      <tr>
        <td><code>n_heads</code></td>
        <td>2, 4</td>
        <td>Uniform choice</td>
      </tr>
      <tr>
        <td><code>d_model</code></td>
        <td>64, 128, 256</td>
        <td>Uniform choice (divisible by n_heads)</td>
      </tr>
      <tr>
        <td><code>d_ff</code></td>
        <td>256, 512</td>
        <td>Uniform choice</td>
      </tr>
      <tr>
        <td><code>batch_size</code></td>
        <td>32, 64, 128</td>
        <td>Uniform choice</td>
      </tr>
      <tr>
        <td><code>context_length</code></td>
        <td>128, 256</td>
        <td>Uniform choice</td>
      </tr>
    </tbody>
  </table>

  <div class="callout">
    <div class="callout-title">Reproducibility</div>
    <p>
      The generator uses <code>random.Random(seed)</code> for deterministic sampling.
      Given the same seed, the same config is produced every time, on every platform.
      The training script also seeds PyTorch and Python's random module.
    </p>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>The Training Script</h2>
  <p>
    <code>experiments/train_char_lm.py</code> is a ~250-line self-contained training script.
    It implements a character-level GPT: a pre-norm decoder-only transformer with causal masking.
  </p>

  <h3>Architecture</h3>
  <ul>
    <li><strong>Tokenisation:</strong> Character-level (~65 vocabulary tokens from TinyShakespeare)</li>
    <li><strong>Model:</strong> Pre-norm decoder-only transformer with causal attention masking</li>
    <li><strong>Layers:</strong> Configurable depth (2-6 layers), width (64-256 d_model), and heads (2-4)</li>
    <li><strong>Parameters:</strong> ~50K to ~2M depending on configuration</li>
    <li><strong>Dataset:</strong> TinyShakespeare (~1MB, auto-downloaded and cached)</li>
  </ul>

  <h3>Interface</h3>
  <pre><code>python train_char_lm.py --config-file config.json</code></pre>
  <p>
    The config file is a flat JSON object with all hyperparameters. The script reads it,
    trains the model, evaluates periodically, and outputs a single JSON line to stdout
    on completion:
  </p>
  <pre><code>{
  "val_bpb": 3.5906,
  "train_loss": 2.1847,
  "steps_completed": 1531,
  "wall_time_seconds": 9.02,
  "device_used": "cpu",
  "model_params": 198721
}</code></pre>
  <p>
    All other logging goes to stderr. This separation is critical: the worker parses
    stdout for the result JSON, while stderr is available for debugging.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Dual Deadline Pattern</h2>
  <p>
    Training tasks use a two-layer timeout system to guarantee termination:
  </p>

  <div class="mermaid">
  flowchart LR
    T1["Training Loop<br/>0s - 54s"] --> T2["Final Eval + JSON<br/>54s - 60s"]
    T2 --> T3["Grace Period<br/>60s - 75s"]
    T3 --> KILL["Hard Kill"]

    M1(["Soft Deadline<br/>90% = 54s"])
    M2(["Budget Ends<br/>60s"])
    M3(["Hard Kill<br/>75s"])

    T1 -.- M1
    T2 -.- M2
    T3 -.- M3

    style T1 fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
    style T2 fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#fff
    style T3 fill:#6b21a8,stroke:#a855f7,stroke-width:2px,color:#fff
    style KILL fill:#dc2626,stroke:#f87171,stroke-width:2px,color:#fff
    style M1 fill:#0d1117,stroke:#60a5fa,stroke-width:2px,color:#60a5fa
    style M2 fill:#0d1117,stroke:#facc15,stroke-width:2px,color:#facc15
    style M3 fill:#0d1117,stroke:#f87171,stroke-width:2px,color:#f87171
  </div>

  <ol>
    <li><strong>Soft deadline (in-script):</strong> The training loop checks elapsed time
    each step. At 90% of the time budget, it stops training, runs a final evaluation,
    and exits cleanly with metrics.</li>
    <li><strong>Hard deadline (worker-side):</strong> The worker sets a kill timer at
    <code>time_budget + 15 seconds</code>. If the script hasn't exited by then,
    the process is terminated. This catches hangs, infinite loops, and GPU driver issues.</li>
  </ol>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Config-via-Temp-File Pattern</h2>
  <p>
    Hyperparameter configs are passed to the training script via temporary JSON files,
    not command-line arguments. This is a deliberate design choice:
  </p>
  <ul>
    <li><strong>No shell escaping issues:</strong> Windows cmd.exe and PowerShell
    handle quotes differently. JSON in a file avoids all quoting problems.</li>
    <li><strong>Arbitrary complexity:</strong> Nested configs, arrays, and special characters
    work without serialisation concerns.</li>
    <li><strong>Clean process interface:</strong> The script has a single argument
    (<code>--config-file</code>) regardless of how many hyperparameters exist.</li>
    <li><strong>Auditability:</strong> The temp file can be preserved for debugging
    if a task fails.</li>
  </ul>

  <pre><code># Worker writes config to temp file
config = {
    "lr": 0.003, "lr_schedule": "cosine",
    "n_layers": 4, "n_heads": 4, "d_model": 128,
    "d_ff": 512, "batch_size": 64, "context_length": 256,
    "seed": 42, "time_budget_seconds": 60
}
with open(tmp_path, "w") as f:
    json.dump(config, f)

# Spawn training subprocess
proc = subprocess.run(
    [python, "train_char_lm.py", "--config-file", tmp_path],
    capture_output=True, timeout=75
)</code></pre>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Worker Execution Flow</h2>

  <div class="mermaid">
  flowchart TD
    START["Task Received"] --> RESOLVE["Resolve Script Path"]
    RESOLVE --> CHECK{"PyTorch<br/>Available?"}
    CHECK -->|"Yes"| WRITE["Write Config to Temp JSON"]
    CHECK -->|"No"| SIM["Simulated Fallback<br/>(Seeded PRNG)"]
    WRITE --> SPAWN["Spawn Python Subprocess"]
    SPAWN --> TIMER["Start Hard Kill Timer<br/>(budget + 15s)"]
    TIMER --> WAIT{"Process<br/>Exited?"}
    WAIT -->|"Yes"| PARSE["Parse JSON from stdout"]
    WAIT -->|"Timeout"| KILL["Kill Process"]
    KILL --> ERROR["Error Result"]
    PARSE --> SUBMIT["Submit Result to Server"]
    SIM --> SUBMIT
    ERROR --> SUBMIT
    SUBMIT --> CLEAN["Clean Up Temp File"]

    style START fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
    style RESOLVE fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style CHECK fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#fff
    style WRITE fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style SPAWN fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style TIMER fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style WAIT fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#fff
    style PARSE fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style KILL fill:#dc2626,stroke:#f87171,stroke-width:2px,color:#fff
    style ERROR fill:#dc2626,stroke:#f87171,stroke-width:2px,color:#fff
    style SIM fill:#9333ea,stroke:#c084fc,stroke-width:2px,color:#fff
    style SUBMIT fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
    style CLEAN fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
  </div>

  <p>
    Both the Python worker agent and the Electron desktop worker follow this same execution
    pattern. The key steps:
  </p>
  <ol>
    <li><strong>Resolve script:</strong> Locate the training script from <code>code_package_ref</code>
    relative to the project root (Python) or <code>process.resourcesPath</code> (Electron).</li>
    <li><strong>Check PyTorch:</strong> Verify <code>torch</code> is importable. If not, fall back
    to simulated metrics with a clear warning.</li>
    <li><strong>Write config:</strong> Serialise the task's config dict (with injected seed and
    time budget) to a temporary JSON file.</li>
    <li><strong>Spawn subprocess:</strong> Execute the training script as a child process
    with stdout/stderr capture.</li>
    <li><strong>Enforce timeout:</strong> Hard kill at <code>time_budget + 15s</code>.</li>
    <li><strong>Parse result:</strong> Read the last line of stdout as JSON metrics.</li>
    <li><strong>Clean up:</strong> Delete the temp config file.</li>
  </ol>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Verified Results</h2>
  <table>
    <thead>
      <tr>
        <th>Validation</th>
        <th>Status</th>
        <th>Detail</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Script produces valid JSON</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>All required metric fields present</td>
      </tr>
      <tr>
        <td>Seed reproducibility</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>val_bpb within 0.05 across runs with same config</td>
      </tr>
      <tr>
        <td>Time budget respected</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>Script exits within budget, never exceeds hard deadline</td>
      </tr>
      <tr>
        <td>Different configs produce different results</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>10-task campaign: val_bpb range 3.57-4.89, std 0.56</td>
      </tr>
      <tr>
        <td>GPU detection (NVIDIA)</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>Auto-installs CUDA PyTorch when GPU detected</td>
      </tr>
      <tr>
        <td>Simulated fallback</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>Clean degradation with UI badge when no PyTorch</td>
      </tr>
      <tr>
        <td>110 automated tests</td>
        <td><span class="badge badge-green">Passed</span></td>
        <td>Config generators, script output, orchestrator, worker, API</td>
      </tr>
    </tbody>
  </table>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-task-detail.png' | relative_url }}" alt="Task detail showing completed training run with real val_bpb metric and hyperparameter config">
    <div class="screenshot-caption">Task detail: completed training run showing real val_bpb metric, hyperparameter config, and resource requirements</div>
  </div>
</div>
