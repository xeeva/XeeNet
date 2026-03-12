---
layout: default
title: Dashboard - XeeNet
---

<div class="page-header">
  <h1>Research Dashboard</h1>
  <p class="lead">
    A real-time web interface for managing experiment campaigns, monitoring workers,
    and analysing results.
  </p>
</div>

<div class="section">
  <h2>Overview</h2>
  <p>
    The XeeNet dashboard is the control centre for the platform. Researchers use it to
    create experiment briefs, monitor distributed training progress, and analyse results
    across campaigns. Built with HTMX for real-time updates, Jinja2 templates, and Pico CSS
    for a clean, responsive interface.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-overview.png' | relative_url }}" alt="Dashboard overview showing workers, tasks, families, briefs, and total credits">
    <div class="screenshot-caption">Dashboard home: live platform stats showing 2 workers online, 68 total tasks, and 538 credits in circulation</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Research Briefs</h2>
  <p>
    Research briefs are the starting point for every experiment campaign. A brief defines
    the research goal, compute budget, and target hardware profile. The orchestrator
    automatically decomposes each brief into concrete tasks with unique hyperparameter
    configurations.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-briefs.png' | relative_url }}" alt="Research briefs list showing experiment campaigns">
    <div class="screenshot-caption">Briefs list: each brief describes an experiment campaign with goal, budget, and hardware requirements</div>
  </div>

  <h3>Campaign Results</h3>
  <p>
    The brief detail page shows the full lifecycle of a campaign: from the research goal
    through to aggregated results. Key metrics include best val_bpb, mean/standard deviation
    across all runs, and the winning hyperparameter configuration.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-brief-detail.png' | relative_url }}" alt="Brief detail page showing campaign results with best val_bpb, configuration, and task list">
    <div class="screenshot-caption">Campaign results: 10/10 tasks completed, best val_bpb 3.5705 with full hyperparameter config and per-task breakdown</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Experiment Families</h2>
  <p>
    Each brief generates an experiment family (campaign) containing all related tasks.
    Families track the metric being optimised, completion status, and linked brief.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-families.png' | relative_url }}" alt="Experiment families list showing campaign status">
    <div class="screenshot-caption">Families view: campaigns linked to briefs with val_bpb metric tracking and completion status</div>
  </div>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-family-detail.png' | relative_url }}" alt="Family detail showing linked brief, metric, resources, and task list">
    <div class="screenshot-caption">Family detail: linked brief, minimum resource requirements, and all 10 tasks with seed and time budget assignments</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Task Management</h2>
  <p>
    Tasks are the atomic units of work. Each task represents a single training run with
    a specific hyperparameter configuration, time budget, and seed. The tasks view shows
    all tasks across all campaigns with their completion status.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-tasks.png' | relative_url }}" alt="Tasks list showing all training tasks with completion status">
    <div class="screenshot-caption">Tasks list: all training tasks across campaigns, showing type, family, priority, assigned worker, and completion time</div>
  </div>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-task-detail.png' | relative_url }}" alt="Task detail showing hyperparameter config, resource requirements, and training result with val_bpb metric">
    <div class="screenshot-caption">Task detail: hyperparameter config, resource requirements, and real training result (val_bpb: 3.8885, train_loss: 1.7409)</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Worker Monitoring</h2>
  <p>
    The workers page tracks all registered nodes in the network. Each worker reports its
    hardware profile (CPU cores, RAM, GPU model and VRAM), platform, and heartbeat status.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-workers.png' | relative_url }}" alt="Workers list showing two online workers with hardware profiles">
    <div class="screenshot-caption">Connected workers: Intel Arc Pro 140T (16GB) and NVIDIA GeForce RTX 3080, both online on Windows</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Technical Implementation</h2>

  <h3>Template Architecture</h3>
  <p>
    The dashboard uses ~15 Jinja2 templates with a shared base layout. HTMX attributes
    handle dynamic content loading without full page refreshes:
  </p>

  <table>
    <thead>
      <tr>
        <th>Template</th>
        <th>Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><code>_base.html</code></td>
        <td>Base layout with navigation, Pico CSS, HTMX includes</td>
      </tr>
      <tr>
        <td><code>home.html</code></td>
        <td>Platform overview with live statistics</td>
      </tr>
      <tr>
        <td><code>briefs_list.html</code></td>
        <td>All research briefs with status badges</td>
      </tr>
      <tr>
        <td><code>brief_detail.html</code></td>
        <td>Campaign results, best config, task breakdown</td>
      </tr>
      <tr>
        <td><code>workers_list.html</code></td>
        <td>Connected workers and hardware profiles</td>
      </tr>
      <tr>
        <td><code>credits_overview.html</code></td>
        <td>Credit balances and transaction history</td>
      </tr>
      <tr>
        <td><code>_stats_partial.html</code></td>
        <td>HTMX partial for auto-refreshing statistics</td>
      </tr>
    </tbody>
  </table>

  <h3>No Build Step</h3>
  <p>
    The dashboard is pure server-side rendering. Static CSS and minimal JavaScript
    live in <code>static/</code>. HTMX handles dynamic updates via HTML-over-the-wire.
    This eliminates the entire frontend build pipeline: no webpack, no bundler,
    no node_modules. Run <code>uvicorn services.api.main:app</code> and the dashboard
    is ready.
  </p>
</div>
