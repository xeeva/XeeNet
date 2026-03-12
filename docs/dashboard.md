---
layout: default
title: Dashboard — XeeNet
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
  <p>
    The dashboard runs as part of the FastAPI backend — no separate frontend build step,
    no JavaScript framework, no npm. Just server-rendered HTML with HTMX for interactivity.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Dashboard Features</h2>

  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#128209;</span>
      <h3>Brief Management</h3>
      <p>
        Create, view, and manage research briefs. Each brief defines an experiment campaign
        with a title, description, number of tasks, and time budget per task. The orchestrator
        automatically decomposes briefs into concrete tasks.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128202;</span>
      <h3>Campaign Results</h3>
      <p>
        View aggregated results for each campaign: best val_bpb, mean/std metrics,
        completion rate, and per-task breakdowns. The best-performing hyperparameter
        configuration is highlighted with its full parameter set.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#9881;</span>
      <h3>Worker Monitoring</h3>
      <p>
        Track registered workers, their hardware profiles (CPU, RAM, GPU), current
        status (idle/working/offline), and historical contribution metrics. Credits
        earned per worker are displayed.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128200;</span>
      <h3>Auto-Refreshing Stats</h3>
      <p>
        Platform statistics update automatically via HTMX polling — no manual refresh
        needed. Active tasks, completed experiments, connected workers, and credit
        circulation are all live.
      </p>
    </div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Brief → Results Flow</h2>
  <p>
    The dashboard reflects the full lifecycle of an experiment campaign:
  </p>

  <h3>1. Create a Brief</h3>
  <p>
    Researchers fill in a brief form specifying the research goal. The orchestrator
    processes it and generates a family of tasks — each with a unique hyperparameter
    configuration sampled from the search space.
  </p>

  <h3>2. Monitor Progress</h3>
  <p>
    The brief detail page shows:
  </p>
  <ul>
    <li><strong>Overall completion:</strong> X/Y tasks completed</li>
    <li><strong>Task list:</strong> each task with its status, assigned worker, and result metrics</li>
    <li><strong>Live updates:</strong> tasks transition from queued → assigned → completed as workers report in</li>
  </ul>

  <h3>3. Analyse Results</h3>
  <p>
    Once tasks complete, the dashboard displays:
  </p>
  <ul>
    <li><strong>Best configuration:</strong> the hyperparameter set that achieved the lowest val_bpb</li>
    <li><strong>Statistical summary:</strong> mean, standard deviation, min/max across all tasks</li>
    <li><strong>Per-task detail:</strong> individual metrics for each config, enabling comparison</li>
  </ul>

  <div class="callout">
    <div class="callout-title">Real Results Example</div>
    <p>
      A 10-task campaign on TinyShakespeare produced val_bpb values ranging from 3.57 to 4.89
      with a standard deviation of 0.56. The best configuration used a 4-layer transformer with
      cosine learning rate schedule at lr=0.003, demonstrating meaningful variation across the
      hyperparameter search space.
    </p>
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
        <td><code>brief_form.html</code></td>
        <td>Create/edit brief form</td>
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

  <h3>API Integration</h3>
  <p>
    Dashboard views call the same REST API that workers and external clients use.
    The dashboard router (<code>services/api/dashboard/</code>) renders HTML responses
    while the API routers (<code>services/api/routers/</code>) return JSON. This means
    any dashboard feature can also be accessed programmatically.
  </p>

  <h3>No Build Step</h3>
  <p>
    The dashboard is pure server-side rendering. Static CSS and minimal JavaScript
    live in <code>static/</code>. HTMX handles dynamic updates via HTML-over-the-wire.
    This eliminates the entire frontend build pipeline — no webpack, no bundler,
    no node_modules. Run <code>uvicorn services.api.main:app</code> and the dashboard
    is ready.
  </p>
</div>
