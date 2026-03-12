---
layout: default
title: Roadmap — XeeNet
---

<div class="page-header">
  <h1>Roadmap</h1>
  <p class="lead">
    Where XeeNet is today and where it's headed — from local prototype
    to global-scale distributed autoresearch.
  </p>
</div>

<div class="section">
  <h2>Current State <span class="badge badge-green">Working</span></h2>
  <p>
    The core platform is functional end-to-end. A researcher can create a brief,
    the orchestrator generates tasks with real hyperparameter configurations,
    workers execute actual PyTorch training, and results flow back to the dashboard.
  </p>

  <h3>What's Built</h3>
  <table>
    <thead>
      <tr>
        <th>Component</th>
        <th>Status</th>
        <th>Detail</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>FastAPI Backend</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>REST API, async DB, 3 router groups, lifespan management</td>
      </tr>
      <tr>
        <td>Web Dashboard</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>HTMX + Jinja2, brief CRUD, results display, auto-refresh</td>
      </tr>
      <tr>
        <td>Orchestrator Agent</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Brief decomposition, config generation, task graph creation</td>
      </tr>
      <tr>
        <td>Python Worker Agent</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Subprocess execution, dual deadlines, simulated fallback</td>
      </tr>
      <tr>
        <td>Electron Desktop Worker</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Auto-setup, GPU detection, task execution, system tray</td>
      </tr>
      <tr>
        <td>Training Script</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Char-level transformer on TinyShakespeare, real val_bpb</td>
      </tr>
      <tr>
        <td>Config Generator</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Reproducible search space sampling with seeds</td>
      </tr>
      <tr>
        <td>Credits System</td>
        <td><span class="badge badge-blue">Framework</span></td>
        <td>Agent defined, calculation logic in place, needs integration</td>
      </tr>
      <tr>
        <td>Portal Assistant</td>
        <td><span class="badge badge-blue">Framework</span></td>
        <td>Agent prompt and stub, needs LLM integration</td>
      </tr>
      <tr>
        <td>Test Suite</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>110 tests across 8 files, all passing</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Near-Term Priorities</h2>

  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#128269;</span>
      <h3>Bayesian Optimisation</h3>
      <p>
        Replace random search with Bayesian optimisation. Use completed task results to
        inform the next batch of hyperparameter configurations. The orchestrator should
        focus exploration on promising regions of the search space.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128640;</span>
      <h3>Multiple Experiment Types</h3>
      <p>
        Extend beyond character-level LMs. Add experiment templates for image classification
        (CIFAR-10), reinforcement learning (CartPole), and other self-contained benchmarks.
        Each template follows the same autoresearch contract.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128274;</span>
      <h3>Result Verification</h3>
      <p>
        Workers are semi-trusted. Implement result verification: randomly re-run tasks on
        trusted workers, compare metrics within tolerance, and flag anomalies. Critical for
        the credits economy — no fake results, no free credits.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#127760;</span>
      <h3>macOS and Linux Workers</h3>
      <p>
        The Electron app currently targets Windows for auto-setup. Extend <code>python-setup.ts</code>
        with platform-specific Python distribution downloads and installation paths for
        macOS and Linux workers.
      </p>
    </div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Medium-Term Vision</h2>

  <h3>Intelligent Orchestration</h3>
  <p>
    The orchestrator should learn from the global results database. When a new campaign
    starts, it should consult <code>LessonsLearned.md</code> and historical results to
    make informed decisions about which hyperparameter regions to explore, which
    architectures to prioritise, and how to allocate compute across tasks.
  </p>

  <h3>Federated Research Programmes</h3>
  <p>
    Multiple researchers should be able to contribute to shared research programmes.
    A programme defines a long-term research goal (e.g., "find the optimal small transformer
    architecture for character-level language modelling") and coordinates campaigns across
    research groups.
  </p>

  <h3>Live Credits Marketplace</h3>
  <p>
    Full implementation of the credits economy: workers earn credits for completed tasks,
    researchers spend credits to submit campaigns. The economics agent manages pricing
    based on supply/demand, detects fraud, and ensures fair distribution. Credits should
    reflect actual compute contributed — GPU time is worth more than CPU time.
  </p>

  <h3>Agent-Driven Code Modification</h3>
  <p>
    Following the autoresearch pattern more deeply: agents should be able to propose
    modifications to the training script itself. Given a series of experiment results,
    the orchestrator could suggest architectural changes, new regularisation techniques,
    or training procedure modifications — and generate the code to test them.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Long-Term: Global Autoresearch Grid</h2>
  <p>
    The ultimate vision is a global research grid where:
  </p>
  <ul>
    <li>Thousands of volunteer devices run bounded ML experiments continuously</li>
    <li>Research programmes self-direct based on accumulated results and lessons</li>
    <li>A shared knowledge base captures insights across all experiments</li>
    <li>Researchers can launch campaigns that run across the entire grid</li>
    <li>The credits economy incentivises sustained participation</li>
    <li>Results are publicly available, advancing open ML research</li>
  </ul>
  <p>
    XeeNet is designed with this scale in mind from the start. The autoresearch contract
    (fixed budget, self-contained script, single metric) makes experiments composable
    and distributable. The agent architecture makes orchestration intelligent. The
    zero-setup desktop worker makes participation frictionless.
  </p>

  <div class="callout">
    <div class="callout-title">The SETI@home Parallel</div>
    <p>
      SETI@home proved that volunteers will donate compute for science — at its peak,
      it had over 5 million participants providing 27 PetaFLOPS. XeeNet applies the
      same model to ML research: instead of searching for extraterrestrial signals,
      we're searching for optimal neural network architectures. The compute requirements
      are similar; the scientific payoff is immediate and measurable.
    </p>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Contributing</h2>
  <p>
    XeeNet is open source. We welcome contributions in any area:
  </p>
  <ul>
    <li><strong>New experiment templates</strong> — self-contained training scripts following the autoresearch contract</li>
    <li><strong>Platform improvements</strong> — dashboard features, API enhancements, worker capabilities</li>
    <li><strong>Testing and validation</strong> — running the desktop worker on diverse hardware configurations</li>
    <li><strong>Documentation</strong> — tutorials, guides, and architectural write-ups</li>
    <li><strong>Research ideas</strong> — what experiments should the grid run?</li>
  </ul>
  <p>
    See the <a href="https://github.com/xeeva/XeeNet">GitHub repository</a> to get started.
  </p>
</div>
