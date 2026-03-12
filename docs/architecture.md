---
layout: default
title: Architecture - XeeNet
---

<div class="page-header">
  <h1>Platform Architecture</h1>
  <p class="lead">
    How XeeNet coordinates distributed ML research across a global grid of volunteer devices.
  </p>
</div>

<div class="section">
  <h2>System Overview</h2>
  <p>
    XeeNet follows a hub-and-spoke model. A central server manages experiment campaigns,
    task queues, and results aggregation. Worker nodes (desktop applications running on
    volunteer machines) poll for tasks, execute training runs, and report metrics back.
  </p>

  <div class="mermaid">
  graph TB
    WEB["fa:fa-globe Web Dashboard<br/>(HTMX + Jinja2)"]

    API["fa:fa-server FastAPI REST API"]
    ORC["fa:fa-brain Orchestrator Agent"]
    ECON["fa:fa-coins Economics Agent"]
    QUEUE["fa:fa-list Task Queue"]
    DB["fa:fa-database SQLite Database"]

    W1["fa:fa-desktop Worker 1<br/>Desktop App"]
    W2["fa:fa-desktop Worker 2<br/>Desktop App"]
    W3["fa:fa-desktop Worker N<br/>Python Agent"]

    WEB -->|"Briefs & Reports"| API
    API --> ORC
    API --> ECON
    ORC -->|"Generate Tasks"| QUEUE
    QUEUE --> DB
    API -->|"Poll / Submit"| W1
    API -->|"Poll / Submit"| W2
    API -->|"Poll / Submit"| W3

    style WEB fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
    style API fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style ORC fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style ECON fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style QUEUE fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#fff
    style DB fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#fff
    style W1 fill:#9333ea,stroke:#c084fc,stroke-width:2px,color:#fff
    style W2 fill:#9333ea,stroke:#c084fc,stroke-width:2px,color:#fff
    style W3 fill:#9333ea,stroke:#c084fc,stroke-width:2px,color:#fff
  </div>
</div>

<div class="section">
  <h2>Directory Structure</h2>
  <pre><code>xeenet/
├── agents/                          # Agent definitions
│   ├── base.py                      # BaseAgent ABC
│   ├── orchestrator/                # Decomposes research goals into tasks
│   │   ├── orchestrator_agent.py    # Runtime implementation
│   │   └── orchestrator_prompt.md   # Agent role/responsibilities
│   ├── worker/                      # Runs tasks on user devices
│   │   └── worker_agent.py          # Subprocess execution + fallback
│   ├── portal/                      # Researcher interface agent
│   └── economics/                   # Credits and metering agent
│
├── skills/                          # Reusable modules called by agents
│   ├── task_generation/             # Experiment templates + config generators
│   │   ├── task_templates.py        # ExperimentTemplate, generate_task_batch()
│   │   └── config_generators.py     # CharLMConfigGenerator (search space)
│   ├── result_analysis/             # Aggregation and interpretation
│   ├── scheduling/                  # Queue management
│   ├── credits/                     # Credit calculations
│   └── infra/                       # Device profiling
│
├── services/
│   ├── api/                         # FastAPI application
│   │   ├── main.py                  # App with lifespan, routers
│   │   ├── routers/                 # orchestrator, worker, portal routes
│   │   ├── dashboard/               # HTMX dashboard views
│   │   └── templates/               # ~15 Jinja2 templates
│   ├── db/                          # Async SQLAlchemy + SQLite
│   ├── schemas.py                   # Pydantic data models
│   └── orchestration.py             # Brief -&gt; campaign -&gt; tasks pipeline
│
├── experiments/
│   └── train_char_lm.py             # Self-contained training script
│
├── desktop/                         # Electron desktop worker
│   └── src/
│       ├── main/                    # Main process (8 TypeScript files)
│       ├── renderer/                # UI (HTML + TypeScript)
│       └── shared/                  # Cross-process types + IPC channels
│
├── config/                          # Settings (Pydantic + YAML)
├── tests/                           # 110 tests across 8 files
└── static/                          # CSS, JS for dashboard</code></pre>
</div>

<div class="section">
  <h2>The Four Agents</h2>
  <p>
    XeeNet uses a multi-agent architecture. Each agent has a defined role, a prompt
    specification, and a Python implementation.
  </p>

  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#127919;</span>
      <h3>Orchestrator Agent</h3>
      <p>
        Decomposes research briefs into task graphs. Uses the <code>CharLMConfigGenerator</code>
        to sample hyperparameter configurations from a defined search space. Each task gets
        a unique seed, a time budget, and a code package reference pointing to the training script.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#9881;</span>
      <h3>Worker Agent</h3>
      <p>
        Executes tasks within resource and schedule constraints. The Python worker resolves
        the training script, writes config to a temp JSON file, spawns a subprocess with
        dual deadlines, and parses the JSON metrics from stdout. Falls back to simulation
        if PyTorch is unavailable.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128172;</span>
      <h3>Portal Assistant</h3>
      <p>
        Conversational interface for researchers. Helps formulate research briefs, explains
        results, and generates reports. Designed for progressive disclosure: high-level
        summaries first, drill-down on request.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128176;</span>
      <h3>Economics Agent</h3>
      <p>
        Manages the credits marketplace. Meters compute contributions from workers,
        calculates costs for researchers, detects fraudulent results, and handles
        budget planning. Workers are semi-trusted and the agent accounts for adversarial behaviour.
      </p>
    </div>
  </div>
</div>

<div class="section">
  <h2>Data Flow</h2>
  <p>
    The platform uses Pydantic schemas as the cross-language contract. The same data
    structures are defined in Python (<code>services/schemas.py</code>) and mirrored in
    TypeScript (<code>desktop/src/shared/types.ts</code>), ensuring consistency across
    the backend API and Electron workers.
  </p>

  <div class="mermaid">
  flowchart LR
    BRIEF["Research Brief"] -->|"decompose"| ORC["Orchestrator"]
    ORC -->|"generate configs"| TASKS["Task Queue"]
    TASKS -->|"poll"| WORKER["Worker Node"]
    WORKER -->|"spawn"| TRAIN["Training Subprocess"]
    TRAIN -->|"JSON stdout"| METRICS["Metrics"]
    METRICS -->|"submit"| API["REST API"]
    API -->|"store"| DB["Database"]
    DB -->|"query"| DASH["Dashboard"]

    style BRIEF fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
    style ORC fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style TASKS fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style WORKER fill:#9333ea,stroke:#c084fc,stroke-width:2px,color:#fff
    style TRAIN fill:#9333ea,stroke:#c084fc,stroke-width:2px,color:#fff
    style METRICS fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#fff
    style API fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style DB fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#fff
    style DASH fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#fff
  </div>

  <h3>Core Schemas</h3>
  <table>
    <thead>
      <tr>
        <th>Schema</th>
        <th>Purpose</th>
        <th>Key Fields</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>ResourceProfile</code></td>
        <td>Hardware capabilities of a worker</td>
        <td>cpu_cores, ram_gb, gpu_name, gpu_vram_gb</td>
      </tr>
      <tr>
        <td><code>TaskSpec</code></td>
        <td>A unit of work to execute</td>
        <td>task_id, config (JSON), code_package_ref, time_budget, seeds</td>
      </tr>
      <tr>
        <td><code>TaskResult</code></td>
        <td>Metrics from a completed task</td>
        <td>val_bpb, train_loss, steps_completed, wall_time_seconds, device_used</td>
      </tr>
      <tr>
        <td><code>BriefSpec</code></td>
        <td>A research campaign definition</td>
        <td>title, description, num_tasks, time_budget_per_task</td>
      </tr>
      <tr>
        <td><code>TrainingCapability</code></td>
        <td>Python/PyTorch availability on a worker</td>
        <td>pythonPath, pythonVersion, hasTorch, hasCuda</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="section">
  <h2>API Layer</h2>
  <p>
    The FastAPI backend exposes a versioned JSON API at <code>/api/v1/</code> with three
    router groups:
  </p>
  <ul>
    <li><strong>Orchestrator routes</strong>: Create briefs, list campaigns, view task status</li>
    <li><strong>Worker routes</strong>: Poll for tasks, submit results, register workers</li>
    <li><strong>Portal routes</strong>: Researcher queries, report generation</li>
  </ul>
  <p>
    The database is async SQLAlchemy with SQLite (via aiosqlite), initialised at app
    startup through FastAPI's lifespan context manager. This keeps the deployment simple:
    no external database server required.
  </p>
</div>
