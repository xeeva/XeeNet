---
layout: default
title: Vision & Market - XeeNet
---

<div class="page-header">
  <h1>Vision & Market Opportunity</h1>
  <p class="lead">
    Why distributed autoresearch is the next frontier in ML, and how
    XeeNet positions itself at the intersection of volunteer computing
    and autonomous experimentation.
  </p>
</div>

<div class="section">
  <h2>The Scale Problem in ML Research</h2>
  <p>
    Machine learning research is fundamentally compute-bound. A single hyperparameter sweep
    across architecture choices, learning rates, and training schedules can require hundreds
    or thousands of GPU-hours. Academic labs wait weeks for cluster time. Startups burn through
    cloud budgets. Individual researchers are locked out entirely.
  </p>
  <p>
    Meanwhile, billions of dollars worth of consumer compute sits idle. The average gaming PC
    is active less than 4 hours a day. Enterprise workstations sit powered on but unused
    overnight. Every one of these machines has a CPU capable of training small neural networks,
    and many have GPUs that rival data centre hardware from just a few years ago.
  </p>
  <p>
    XeeNet bridges this gap: researchers get affordable, elastic compute for ML experiments,
    and device owners put their idle hardware to productive use.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>The Autoresearch Revolution</h2>
  <p>
    Andrej Karpathy's autoresearch project demonstrated a powerful insight: ML experiments
    can be fully autonomous. A training script runs for a fixed compute budget, reports a
    single metric, and an agent decides what to try next. No human in the loop during
    execution. No interactive debugging sessions. Just bounded, reproducible experiments
    that produce comparable results.
  </p>
  <p>
    This changes the economics of ML research fundamentally. If every experiment is:
  </p>
  <ul>
    <li><strong>Self-contained</strong> (one script, no external dependencies beyond PyTorch)</li>
    <li><strong>Bounded</strong> (fixed time budget, guaranteed termination)</li>
    <li><strong>Comparable</strong> (single metric like <code>val_bpb</code> across all runs)</li>
    <li><strong>Reproducible</strong> (seeded RNG, deterministic configs)</li>
  </ul>
  <p>
    ...then experiments become perfectly distributable. Any machine, anywhere in the world,
    can run any experiment and produce a valid result. This is the core insight behind XeeNet.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Market Landscape</h2>
  <h3>Volunteer Computing</h3>
  <p>
    SETI@home proved the model at massive scale: 5.2 million participants contributing
    27 PetaFLOPS at peak. Folding@home exceeded an ExaFLOP during COVID-19 protein folding
    efforts, briefly becoming the world's most powerful computing system. BOINC continues
    to power dozens of scientific projects across astrophysics, mathematics, and biology.
  </p>
  <p>
    These projects demonstrate sustained volunteer willingness to donate compute for science.
    But none target ML research, where the compute demand is growing exponentially and the
    workload characteristics (bounded training runs, GPU acceleration) are an excellent fit
    for distributed execution.
  </p>

  <h3>Distributed ML Compute</h3>
  <p>
    Commercial distributed GPU marketplaces (Vast.ai, RunPod, Lambda) focus on renting
    full machines at hourly rates. They target ML engineers who need dedicated instances
    for days or weeks. This leaves a massive gap: researchers who need thousands of short
    experiments (minutes each) rather than a few long ones.
  </p>
  <p>
    XeeNet occupies a different niche entirely. Tasks are short (seconds to minutes),
    self-contained, and fault-tolerant. A worker can disconnect mid-task and the work is
    simply reassigned. This makes volunteer hardware viable in a way that long-running
    training jobs never could be.
  </p>

  <h3>The Opportunity</h3>
  <table>
    <thead>
      <tr>
        <th>Factor</th>
        <th>Existing Solutions</th>
        <th>XeeNet</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Target user</td>
        <td>ML engineers with budgets</td>
        <td>Researchers, academics, independents</td>
      </tr>
      <tr>
        <td>Compute source</td>
        <td>Dedicated GPU clusters / cloud</td>
        <td>Volunteer idle hardware (any device)</td>
      </tr>
      <tr>
        <td>Task duration</td>
        <td>Hours to days</td>
        <td>Seconds to minutes</td>
      </tr>
      <tr>
        <td>Cost model</td>
        <td>Per-hour rental ($0.50-$4/GPU-hr)</td>
        <td>Credits economy (contribute to earn)</td>
      </tr>
      <tr>
        <td>Setup friction</td>
        <td>SSH, Docker, driver config</td>
        <td>Zero: download, click Start</td>
      </tr>
      <tr>
        <td>Fault tolerance</td>
        <td>Checkpointing (complex)</td>
        <td>Inherent: tasks are short and idempotent</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Scale Economics</h2>
  <p>
    The economics of XeeNet improve with scale in ways that centralised compute cannot match:
  </p>

  <h3>Supply-Side Dynamics</h3>
  <p>
    Every new worker that joins the network adds compute capacity at zero marginal cost to
    the platform. Workers bear their own electricity and hardware costs, but since these
    machines are already powered on and idle, the incremental cost is near zero. A gaming PC
    drawing 50W idle versus 150W under load costs the owner roughly $0.01/hour in additional
    electricity to run ML training. That is 10-100x cheaper than cloud GPU pricing.
  </p>

  <h3>Demand-Side Dynamics</h3>
  <p>
    Researchers benefit from elastic scaling that no fixed cluster can provide. A hyperparameter
    sweep of 1,000 configurations can run across 500 workers in parallel, completing in the time
    it takes to run two experiments on a single machine. The autoresearch contract (fixed budget,
    single metric) means results are directly comparable regardless of which worker ran them.
  </p>

  <h3>Network Effects</h3>
  <p>
    More workers attract more researchers (faster results). More researchers attract more
    workers (more credits to earn, more impactful science). This creates a virtuous cycle
    where the platform becomes more valuable to both sides as it grows. Unlike cloud compute,
    where costs scale linearly, XeeNet's distributed model means capacity scales with adoption.
  </p>

  <div class="callout">
    <div class="callout-title">Scale Illustration</div>
    <p>
      A modest network of 10,000 workers, each contributing 2 hours of idle time daily,
      provides 20,000 compute-hours per day. At an average of 6 experiments per hour
      per worker, that is 120,000 experiments per day. A hyperparameter sweep that would
      take a single GPU months can complete in hours.
    </p>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>The Credits Economy</h2>
  <p>
    XeeNet uses an internal credits system to balance supply and demand:
  </p>
  <ul>
    <li><strong>Workers earn credits</strong> by completing tasks. Credit value scales with
    compute contributed: GPU tasks earn more than CPU tasks, longer budgets earn proportionally more.</li>
    <li><strong>Researchers spend credits</strong> to submit experiment campaigns. Pricing reflects
    the actual compute required.</li>
    <li><strong>Bootstrap mechanism:</strong> New users receive starter credits to run their first
    campaign, experiencing the platform before contributing compute.</li>
    <li><strong>Anti-fraud:</strong> The economics agent monitors for fabricated results.
    Random verification re-runs catch workers submitting fake metrics. Repeat offenders
    lose credits and are excluded from the network.</li>
  </ul>
  <p>
    This two-sided market creates sustainable incentives. Contributors are rewarded for honest
    participation. Researchers access compute that scales with the network. The platform
    captures no rent on the underlying compute itself.
  </p>

  <div class="screenshot">
    <img src="{{ '/assets/images/dashboard-overview.png' | relative_url }}" alt="Dashboard overview showing workers, tasks, families, briefs, and total credits">
    <div class="screenshot-caption">Platform dashboard showing active workers, task completion stats, and total credits in circulation</div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Use Cases</h2>
  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#127891;</span>
      <h3>Academic Research</h3>
      <p>
        University labs can run large-scale hyperparameter sweeps without waiting for
        shared cluster allocations. Graduate students get access to distributed compute
        for their thesis experiments.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128161;</span>
      <h3>Architecture Search</h3>
      <p>
        Explore neural network architecture choices (depth, width, attention patterns)
        across thousands of configurations simultaneously. Find optimal designs for
        specific tasks and compute budgets.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128218;</span>
      <h3>Reproducibility Studies</h3>
      <p>
        Re-run published experiments across diverse hardware to verify claims.
        Seeded configs and standardised metrics make large-scale reproducibility
        testing practical for the first time.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#127981;</span>
      <h3>Open Science</h3>
      <p>
        All experiment results flow into a shared database. The global research
        community benefits from every run, building collective knowledge about
        what works and what does not.
      </p>
    </div>
  </div>
</div>
