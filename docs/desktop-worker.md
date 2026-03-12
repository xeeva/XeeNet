---
layout: default
title: Desktop Worker - XeeNet
---

<div class="page-header">
  <h1>Desktop Worker Application</h1>
  <p class="lead">
    A self-contained Electron app that turns any Windows PC into a distributed
    ML training node. No Python, no PyTorch, no setup required.
  </p>
</div>

<div class="section">
  <h2>Zero-Setup Philosophy</h2>
  <p>
    The biggest barrier to distributed compute is setup friction. BOINC projects require
    users to install runtimes, configure paths, and troubleshoot dependency conflicts.
    XeeNet eliminates all of this.
  </p>
  <p>
    When a user launches the XeeNet Worker for the first time, the app automatically:
  </p>
  <ol>
    <li>Downloads the Python 3.12.8 embeddable distribution (~15 MB)</li>
    <li>Extracts it to <code>%APPDATA%/xeenet-worker/python/</code></li>
    <li>Enables pip (edits the <code>._pth</code> file, runs <code>get-pip.py</code>)</li>
    <li>Detects whether an NVIDIA GPU is present (via <code>nvidia-smi</code>)</li>
    <li>Installs PyTorch: CUDA-enabled (~2.5 GB) if GPU detected, CPU-only (~160 MB) otherwise</li>
    <li>Writes a completion marker and starts accepting tasks</li>
  </ol>
  <p>
    The entire ML environment lives inside the app's data directory. It does not touch the
    system Python, does not modify PATH, and can be cleanly uninstalled by deleting the folder.
  </p>

  <div class="callout">
    <div class="callout-title">GPU Auto-Detection</div>
    <p>
      The setup process queries <code>nvidia-smi --query-gpu=name --format=csv,noheader</code>.
      If an NVIDIA GPU responds, the app installs PyTorch with CUDA 12.4 support.
      If no GPU is found (or if the user has disabled GPU in settings), it installs the lightweight CPU-only build.
    </p>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Application Architecture</h2>
  <p>
    The desktop worker is built with Electron 28 and TypeScript, following Electron's
    security best practices: context isolation, no Node.js in the renderer, and a typed
    IPC bridge.
  </p>

  <div class="mermaid">
  graph TB
    WS["Worker Service<br/>Poll loop, subprocess, timeouts"]
    PR["Python Resolver<br/>Find Python, check PyTorch"]
    PS["Python Setup<br/>Auto-download, install"]
    HD["Hardware Detection<br/>CPU, RAM, GPU profiling"]
    IPC["IPC Handlers<br/>10 typed channels"]
    STORE["Electron Store<br/>Persistent config"]
    TRAY["System Tray<br/>Status icon, quick menu"]
    LOG["File Logger<br/>Rotating log files"]

    API["window.xeenet API<br/>(Context Bridge)"]

    UI["Dark Theme UI<br/>Server URL, resource sliders<br/>Log panel, status badges"]

    WS --> PR
    WS --> PS
    WS --> HD
    IPC --> WS
    IPC --> STORE
    IPC --> API
    API --> UI
    WS --> LOG
    TRAY --> WS

    style WS fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style PR fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style PS fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style HD fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style IPC fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style STORE fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style TRAY fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style LOG fill:#16a34a,stroke:#4ade80,stroke-width:2px,color:#000
    style API fill:#ca8a04,stroke:#facc15,stroke-width:2px,color:#000
    style UI fill:#2563eb,stroke:#60a5fa,stroke-width:2px,color:#000
  </div>

  <h3>IPC Channels</h3>
  <p>
    All communication between main and renderer processes goes through typed IPC channels.
    Channel names are defined once in <code>shared/ipc-channels.ts</code> and used by both
    the handler registration and the preload bridge.
  </p>
  <table>
    <thead>
      <tr>
        <th>Channel</th>
        <th>Direction</th>
        <th>Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>worker:start</code></td>
        <td>Renderer to Main</td>
        <td>Start the worker loop with a server URL</td>
      </tr>
      <tr>
        <td><code>worker:stop</code></td>
        <td>Renderer to Main</td>
        <td>Gracefully stop the worker</td>
      </tr>
      <tr>
        <td><code>worker:state-update</code></td>
        <td>Main to Renderer</td>
        <td>Full application state broadcast</td>
      </tr>
      <tr>
        <td><code>worker:log</code></td>
        <td>Main to Renderer</td>
        <td>Log entry for the UI log panel</td>
      </tr>
      <tr>
        <td><code>config:get / config:set</code></td>
        <td>Renderer to Main</td>
        <td>Read/write persistent configuration</td>
      </tr>
      <tr>
        <td><code>hardware:detect</code></td>
        <td>Renderer to Main</td>
        <td>Trigger hardware profiling</td>
      </tr>
      <tr>
        <td><code>python:check</code></td>
        <td>Renderer to Main</td>
        <td>Check Python + PyTorch availability</td>
      </tr>
      <tr>
        <td><code>python:setup</code></td>
        <td>Renderer to Main</td>
        <td>Trigger ML environment auto-setup</td>
      </tr>
      <tr>
        <td><code>python:setup-progress</code></td>
        <td>Main to Renderer</td>
        <td>Setup progress updates (phase, detail, percent)</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>User Interface</h2>

  <div class="screenshot">
    <img src="{{ '/assets/images/worker-connected.png' | relative_url }}" alt="XeeNet Worker connected and ready, showing Real ML Training badge, hardware detection, and activity log">
    <div class="screenshot-caption">Worker connected to server: Real ML Training badge, NVIDIA RTX 3080 detected, CUDA-enabled PyTorch ready</div>
  </div>

  <p>
    The desktop worker features a dark-themed UI with:
  </p>
  <ul>
    <li><strong>Server URL configuration</strong> with connection testing (latency display)</li>
    <li><strong>Resource allocation sliders</strong> for CPU cores, RAM limit, and GPU toggle</li>
    <li><strong>Real-time log panel</strong> with colour-coded severity levels</li>
    <li><strong>Worker state display:</strong> Idle, Polling, Working, Error</li>
    <li><strong>Task information panel</strong> showing current task ID, hyperparameters, and progress</li>
    <li><strong>Execution mode badge:</strong> Real ML Training vs Simulated</li>
    <li><strong>System tray integration</strong> for minimise-to-tray and status icon updates</li>
  </ul>

  <div class="screenshot">
    <img src="{{ '/assets/images/worker-training.png' | relative_url }}" alt="XeeNet Worker actively running a training task, showing task details and hyperparameter config">
    <div class="screenshot-caption">Worker executing a real training task: hyperparameter config visible, spawning train_char_lm.py subprocess</div>
  </div>

  <div class="screenshot">
    <img src="{{ '/assets/images/worker-settings.png' | relative_url }}" alt="XeeNet Worker settings panel with CPU cores, RAM, and GPU allocation controls">
    <div class="screenshot-caption">Settings panel: users control CPU cores, RAM, and GPU allocation donated to the network</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Task Execution</h2>

  <h3>Python Resolution</h3>
  <p>
    The <code>python-resolver</code> module searches for a usable Python installation
    in priority order:
  </p>
  <ol>
    <li><strong>Embedded Python</strong>: the auto-downloaded distribution in <code>%APPDATA%/xeenet-worker/python/</code></li>
    <li><strong>User-configured path</strong>: from the <code>pythonPath</code> setting</li>
    <li><strong><code>python3</code> on PATH</strong></li>
    <li><strong><code>python</code> on PATH</strong></li>
    <li><strong>Common Windows locations</strong>: <code>%LOCALAPPDATA%\Programs\Python\...</code>, <code>C:\Python3*\...</code></li>
  </ol>
  <p>
    Once found, the resolver runs a quick probe (<code>python -c "import torch; ..."</code>)
    to determine PyTorch availability and CUDA support. The result is cached for the session.
  </p>

  <h3>Script Resolution</h3>
  <p>
    The training script is bundled inside the portable exe via electron-builder's
    <code>extraResources</code>. At runtime, <code>resolveScript()</code> checks:
  </p>
  <ol>
    <li><code>process.resourcesPath/experiments/</code> (packaged app)</li>
    <li><code>process.cwd()/experiments/</code> (development mode)</li>
    <li><code>__dirname/../../experiments/</code> (development mode fallback)</li>
  </ol>

  <h3>Execution Mode Indicator</h3>
  <p>
    The UI displays an execution mode badge:
  </p>
  <ul>
    <li><span class="badge badge-green">Real ML Training</span> PyTorch available, running actual training</li>
    <li><span class="badge badge-amber">Simulated</span> PyTorch unavailable, using seeded PRNG metrics</li>
  </ul>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Distribution</h2>
  <table>
    <thead>
      <tr>
        <th>Aspect</th>
        <th>Detail</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Package format</td>
        <td>Portable <code>.exe</code> (NSIS)</td>
      </tr>
      <tr>
        <td>Electron version</td>
        <td>28+</td>
      </tr>
      <tr>
        <td>Node.js</td>
        <td>Bundled (Electron's built-in)</td>
      </tr>
      <tr>
        <td>Python</td>
        <td>Auto-downloaded embeddable 3.12.8</td>
      </tr>
      <tr>
        <td>PyTorch</td>
        <td>Auto-installed (CPU ~160 MB, CUDA ~2.5 GB)</td>
      </tr>
      <tr>
        <td>Data directory</td>
        <td><code>%APPDATA%/xeenet-worker/</code></td>
      </tr>
    </tbody>
  </table>
</div>
