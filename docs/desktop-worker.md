---
layout: default
title: Desktop Worker — XeeNet
---

<div class="page-header">
  <h1>Desktop Worker Application</h1>
  <p class="lead">
    A self-contained Electron app that turns any Windows PC into a distributed
    ML training node — no Python, no PyTorch, no setup required.
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
    <li>Installs PyTorch — CUDA-enabled (~2.5 GB) if GPU detected, CPU-only (~160 MB) otherwise</li>
    <li>Writes a completion marker and starts accepting tasks</li>
  </ol>
  <p>
    The entire ML environment lives inside the app's data directory. It doesn't touch the
    system Python, doesn't modify PATH, and can be cleanly uninstalled by deleting the folder.
  </p>

  <div class="callout">
    <div class="callout-title">GPU Auto-Detection</div>
    <p>
      The setup process queries <code>nvidia-smi --query-gpu=name --format=csv,noheader</code>.
      If an NVIDIA GPU responds, the app installs PyTorch with CUDA 12.4 support from
      <code>download.pytorch.org/whl/cu124</code>. If no GPU is found (or if the user has
      disabled GPU in settings), it installs the lightweight CPU-only build. The user's
      GPU preference in the settings panel is respected — even with an NVIDIA GPU present,
      the user can opt for CPU-only training.
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

  <h3>Process Model</h3>
  <div class="diagram">
  ┌─────────────────────────────────────────────────────────┐
  │                    Main Process                          │
  │                                                         │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
  │  │ Worker       │  │ Python       │  │ Hardware     │  │
  │  │ Service      │  │ Resolver     │  │ Detection    │  │
  │  │              │  │              │  │              │  │
  │  │ • Poll loop  │  │ • Find Python│  │ • CPU cores  │  │
  │  │ • Subprocess │  │ • Check torch│  │ • RAM        │  │
  │  │ • Timeouts   │  │ • Auto-setup │  │ • GPU/VRAM   │  │
  │  └──────────────┘  └──────────────┘  └──────────────┘  │
  │                                                         │
  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
  │  │ IPC          │  │ Store        │  │ System Tray  │  │
  │  │ Handlers     │  │ (electron-   │  │              │  │
  │  │              │  │  store)      │  │ • Status icon│  │
  │  │ 10 channels  │  │              │  │ • Quick menu │  │
  │  └──────────────┘  └──────────────┘  └──────────────┘  │
  │                          │                              │
  │  ┌──────────────┐        │  ┌───────────────────────┐   │
  │  │ Python       │        │  │ File Logger           │   │
  │  │ Setup        │        │  │                       │   │
  │  │              │        │  │ • Rotating log files  │   │
  │  │ • Download   │        │  │ • %APPDATA%/logs/     │   │
  │  │ • Extract    │        │  └───────────────────────┘   │
  │  │ • Install    │        │                              │
  │  └──────────────┘        │                              │
  └──────────────────────────┼──────────────────────────────┘
                             │ contextBridge (IPC)
  ┌──────────────────────────┼──────────────────────────────┐
  │              Renderer Process                           │
  │                          │                              │
  │  window.xeenet = {       │                              │
  │    worker.start()        │     ┌────────────────────┐   │
  │    worker.stop()         │     │    Dark Theme UI   │   │
  │    worker.onStateUpdate()│────▶│                    │   │
  │    config.get/set()      │     │  • Server URL      │   │
  │    hardware.detect()     │     │  • Resource sliders│   │
  │    python.check()        │     │  • Log panel       │   │
  │    python.setup()        │     │  • Status badges   │   │
  │    connection.test()     │     └────────────────────┘   │
  │  }                                                      │
  └─────────────────────────────────────────────────────────┘
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
        <td>Renderer → Main</td>
        <td>Start the worker loop with a server URL</td>
      </tr>
      <tr>
        <td><code>worker:stop</code></td>
        <td>Renderer → Main</td>
        <td>Gracefully stop the worker</td>
      </tr>
      <tr>
        <td><code>worker:state-update</code></td>
        <td>Main → Renderer</td>
        <td>Full application state broadcast</td>
      </tr>
      <tr>
        <td><code>worker:log</code></td>
        <td>Main → Renderer</td>
        <td>Log entry for the UI log panel</td>
      </tr>
      <tr>
        <td><code>config:get</code> / <code>config:set</code></td>
        <td>Renderer → Main</td>
        <td>Read/write persistent configuration</td>
      </tr>
      <tr>
        <td><code>hardware:detect</code></td>
        <td>Renderer → Main</td>
        <td>Trigger hardware profiling</td>
      </tr>
      <tr>
        <td><code>python:check</code></td>
        <td>Renderer → Main</td>
        <td>Check Python + PyTorch availability</td>
      </tr>
      <tr>
        <td><code>python:setup</code></td>
        <td>Renderer → Main</td>
        <td>Trigger ML environment auto-setup</td>
      </tr>
      <tr>
        <td><code>python:setup-progress</code></td>
        <td>Main → Renderer</td>
        <td>Setup progress updates (phase, detail, percent)</td>
      </tr>
      <tr>
        <td><code>app:quit</code> / <code>app:minimise-to-tray</code></td>
        <td>Renderer → Main</td>
        <td>Application lifecycle control</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Task Execution</h2>
  <p>
    When a task arrives, the worker service follows this flow:
  </p>

  <h3>1. Python Resolution</h3>
  <p>
    The <code>python-resolver</code> module searches for a usable Python installation
    in priority order:
  </p>
  <ol>
    <li><strong>Embedded Python</strong> — the auto-downloaded distribution in <code>%APPDATA%/xeenet-worker/python/</code></li>
    <li><strong>User-configured path</strong> — from the <code>pythonPath</code> setting</li>
    <li><strong><code>python3</code> on PATH</strong></li>
    <li><strong><code>python</code> on PATH</strong></li>
    <li><strong>Common Windows locations</strong> — <code>%LOCALAPPDATA%\Programs\Python\...</code>, <code>C:\Python3*\...</code></li>
  </ol>
  <p>
    Once found, the resolver runs a quick probe (<code>python -c "import torch; ..."</code>)
    to determine PyTorch availability and CUDA support. The result is cached for the session.
  </p>

  <h3>2. Script Resolution</h3>
  <p>
    The training script is bundled inside the portable exe via electron-builder's
    <code>extraResources</code>. At runtime, <code>resolveScript()</code> checks:
  </p>
  <ol>
    <li><code>process.resourcesPath/experiments/</code> — packaged app</li>
    <li><code>process.cwd()/experiments/</code> — development mode</li>
    <li><code>__dirname/../../experiments/</code> — development mode fallback</li>
  </ol>

  <h3>3. Subprocess Execution</h3>
  <p>
    The worker spawns a child process with the embedded Python, passing the config
    via a temporary JSON file. Stdout is collected for the metrics JSON; stderr is
    logged for debugging. A hard timeout kills the process if the script doesn't
    exit within the grace period.
  </p>

  <h3>4. Execution Mode Indicator</h3>
  <p>
    The UI displays an execution mode badge:
  </p>
  <ul>
    <li><span class="badge badge-green">Real ML Training</span> — PyTorch available, running actual training</li>
    <li><span class="badge badge-amber">Simulated</span> — PyTorch unavailable, using seeded PRNG metrics</li>
  </ul>
</div>

<div class="divider"></div>

<div class="section">
  <h2>User Interface</h2>
  <p>
    The desktop worker features a dark-themed UI with:
  </p>
  <ul>
    <li><strong>Server URL configuration</strong> with connection testing (latency display)</li>
    <li><strong>Resource allocation sliders</strong> — CPU cores, RAM limit, GPU toggle</li>
    <li><strong>Real-time log panel</strong> with colour-coded severity levels</li>
    <li><strong>Worker state display</strong> — Idle, Polling, Working, Error</li>
    <li><strong>Task information panel</strong> — shows current task ID, hyperparameters, and progress</li>
    <li><strong>Execution mode badge</strong> — Real ML Training vs Simulated</li>
    <li><strong>System tray integration</strong> — minimise to tray, status icon updates</li>
  </ul>

  <h3>Resource Controls</h3>
  <p>
    Users can limit the resources available to training tasks:
  </p>
  <table>
    <thead>
      <tr>
        <th>Control</th>
        <th>Effect</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>CPU Cores Limit</td>
        <td>Caps the number of cores available to training subprocesses</td>
      </tr>
      <tr>
        <td>RAM Limit (GB)</td>
        <td>Maximum memory allocation for the worker</td>
      </tr>
      <tr>
        <td>GPU Enabled</td>
        <td>Toggle GPU usage on/off. When disabled, forces CPU-only PyTorch even if GPU available</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Distribution</h2>
  <p>
    The desktop worker is packaged as a portable Windows executable using electron-builder.
    No installation required — download, run, and contribute compute. The training script
    is bundled inside the exe as an extra resource.
  </p>
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
