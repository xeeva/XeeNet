---
layout: default
title: Roadmap - XeeNet
---

<div class="page-header">
  <h1>Roadmap</h1>
  <p class="lead">
    XeeNet is a distributed experimentation network that turns idle compute into
    a research fabric for bounded, verifiable ML workloads. This roadmap tracks
    the journey from working prototype to global-scale autoresearch.
  </p>
</div>

<div class="section">
  <h2>Current State <span class="badge badge-green">Phase 1 Complete</span></h2>
  <p>
    The core platform is functional end-to-end as a single-operator research network.
    A researcher creates a brief, the orchestrator decomposes it into a campaign of
    bounded experiments with real hyperparameter configurations, workers execute actual
    PyTorch training, results flow back through the API, and the dashboard displays
    live progress with factor analysis. Credits are calculated and recorded on every
    result submission.
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
        <td>HTMX + Jinja2, brief CRUD, campaign status, results display, auto-refresh</td>
      </tr>
      <tr>
        <td>Orchestrator Agent</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Brief decomposition, config generation, task graph creation</td>
      </tr>
      <tr>
        <td>Python Worker Agent</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Subprocess execution, dual deadlines, simulated fallback, CLI runner</td>
      </tr>
      <tr>
        <td>Electron Desktop Worker</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Zero-setup install, GPU detection, task execution, system tray</td>
      </tr>
      <tr>
        <td>Training Pipeline</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Char-level transformer on TinyShakespeare, real val_bpb, bounded budgets</td>
      </tr>
      <tr>
        <td>Config Generator</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Reproducible search space sampling with deterministic seeds</td>
      </tr>
      <tr>
        <td>Campaign Tooling</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Campaign runner, progress monitor, post-campaign factor analysis with JSON export</td>
      </tr>
      <tr>
        <td>Credits System</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>Calculation on result submission, ledger persistence, dashboard display</td>
      </tr>
      <tr>
        <td>Portal Assistant</td>
        <td><span class="badge badge-blue">Framework</span></td>
        <td>Agent prompt and stub, needs LLM integration</td>
      </tr>
      <tr>
        <td>Test Suite</td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>110 tests across 10 files, all passing</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Growth Phases</h2>
  <p>
    XeeNet grows in four deliberate phases. Each phase proves a specific thesis
    before the next layer of complexity is introduced. The platform is not a
    replacement for datacentres &mdash; it is a new compute substrate for
    high-volume ML experimentation.
  </p>

  <table>
    <thead>
      <tr>
        <th>Phase</th>
        <th>Status</th>
        <th>Thesis to Prove</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>1. Single-Operator Network</strong></td>
        <td><span class="badge badge-green">Complete</span></td>
        <td>A distributed worker network can reliably execute bounded ML experiments and produce useful, verified research insights.</td>
      </tr>
      <tr>
        <td><strong>2. Trusted External Contributors</strong></td>
        <td><span class="badge badge-amber">Next</span></td>
        <td>Strangers can safely contribute compute with verifiable results and earned reputation.</td>
      </tr>
      <tr>
        <td><strong>3. Research Platform</strong></td>
        <td><span class="badge badge-blue">Planned</span></td>
        <td>External researchers get genuine value from submitting briefs to the network.</td>
      </tr>
      <tr>
        <td><strong>4. Economic Layer</strong></td>
        <td><span class="badge badge-blue">Planned</span></td>
        <td>A sustainable incentive model drives long-term participation without regulatory overhead.</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Phase 2: Trusted External Contributors <span class="badge badge-amber">Next</span></h2>
  <p>
    The trust layer is the existential requirement. Without it, adoption stops.
    These priorities harden the platform for external workers before scaling the
    researcher side.
  </p>

  <div class="card-grid">
    <div class="card">
      <span class="card-icon">&#128274;</span>
      <h3>Result Verification</h3>
      <p>
        First-class k-of-n redundancy: randomly re-run a subset of tasks on trusted
        workers, compare metrics within tolerance, and flag anomalies. This is the
        minimum viable trust layer for a semi-trusted worker network.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#128737;</span>
      <h3>Workload Sandboxing</h3>
      <p>
        The autoresearch contract already constrains the attack surface &mdash; workers
        run a pre-approved script with JSON config, not arbitrary code. Harden this with
        containerised or WASM-based execution, no arbitrary filesystem or network access,
        and deterministic runtime constraints.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#11088;</span>
      <h3>Worker Reputation</h3>
      <p>
        Track worker reliability over time: task completion rate, result consistency
        across redundant runs, uptime history. Reputation scores inform task scheduling
        priority and eligibility for higher-value workloads.
      </p>
    </div>
    <div class="card">
      <span class="card-icon">&#127760;</span>
      <h3>Cross-Platform Workers</h3>
      <p>
        Extend the Electron app&rsquo;s auto-setup beyond Windows. Add platform-specific
        Python distribution management for macOS and Linux. Signed binaries, reproducible
        runtimes, and transparent security model in the documentation.
      </p>
    </div>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Phase 3: Research Platform <span class="badge badge-blue">Planned</span></h2>
  <p>
    Once external workers can contribute safely, open the platform to external
    researchers. The goal is to prove that the network produces genuine research
    value &mdash; not just compute, but knowledge.
  </p>

  <h3>Workload Admission and Policy Engine</h3>
  <p>
    External briefs must pass through a policy engine: constrained job formats,
    pre-approved execution templates, resource and time-budget caps. The workload
    model must be strict enough to prevent abuse (cryptomining, data exfiltration,
    fingerprinting) while flexible enough to support diverse research questions.
    Public datasets only in the initial release.
  </p>

  <h3>Bayesian Optimisation</h3>
  <p>
    Replace random search with Bayesian optimisation. Use the accumulated experiment
    history to inform the next batch of hyperparameter configurations. Focus
    exploration on promising regions of the search space rather than sweeping blindly.
  </p>

  <h3>Multiple Experiment Types</h3>
  <p>
    Extend beyond character-level LMs. Add experiment templates for image
    classification (CIFAR-10), reinforcement learning (CartPole), and other
    self-contained benchmarks. Each template follows the same autoresearch
    contract: bounded budget, single comparable metric, deterministic seeds.
  </p>

  <h3>Regional Orchestrator Nodes</h3>
  <p>
    Deploy local orchestrator nodes in each geographic region. Regional nodes
    prioritise low-latency clients, handle worker-to-task matching within their
    zone, and synchronise results with the central server. Reduces cross-region
    data transfer and improves scheduling responsiveness.
  </p>

  <h3>Intelligent Orchestration</h3>
  <p>
    The orchestrator consults the global experiment corpus before designing new
    campaigns. Historical results inform which hyperparameter regions to explore,
    which architectures to prioritise, and how to allocate compute across tasks.
    Each campaign builds on the accumulated knowledge of every previous campaign.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Phase 4: Economic Layer <span class="badge badge-blue">Planned</span></h2>
  <p>
    Introduce only after the research platform proves its value. The economic
    layer must be legally sound and operationally justified before any
    monetisation.
  </p>

  <h3>Credits Marketplace</h3>
  <p>
    Workers earn credits for completed, verified tasks. Researchers spend credits
    to submit campaigns. The economics agent manages pricing based on supply and
    demand, detects fraud, and ensures fair distribution. Credits reflect actual
    compute contributed: GPU time is worth more than CPU time.
  </p>

  <h3>Monetisation</h3>
  <p>
    Large research projects and enterprise labs can purchase worker time for
    high-throughput experimentation. The acquisition thesis is not &ldquo;replace
    datacentres&rdquo; &mdash; it is &ldquo;massively accelerate the experiment
    loop that informs what to train in the datacentres.&rdquo; Every major lab
    runs thousands of small experiments before committing to a large training run.
    That pre-cluster experimentation phase is the sweet spot.
  </p>

  <h3>Central Ledger with Cryptographic Audit</h3>
  <p>
    A centralised append-only ledger with cryptographic task receipts, worker
    attestations, and audit trails. Provides 95% of the trust guarantees of a
    distributed blockchain with a fraction of the complexity. Blockchain becomes
    relevant only if the platform requires trustless settlement between parties
    who do not trust a central operator.
  </p>

  <h3>Federated Research Programmes</h3>
  <p>
    Multiple researchers contribute to shared long-term research goals (e.g.,
    &ldquo;find the optimal small transformer architecture for character-level
    language modelling&rdquo;). Programmes coordinate campaigns across research
    groups and accumulate results into shared knowledge.
  </p>

  <h3>Agent-Driven Code Modification</h3>
  <p>
    Following the autoresearch pattern more deeply: agents propose modifications
    to training scripts based on experiment results. Given a series of outcomes,
    the orchestrator suggests architectural changes, new regularisation techniques,
    or training procedure modifications and generates the code to test them.
  </p>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Long-Term: The Global Experiment Corpus</h2>
  <p>
    The real moat is not the compute network. It is the experiment database.
  </p>
  <p>
    Every completed task produces a verified (seed, config, metric) tuple. Over
    time, that accumulates into a massive structured dataset of &ldquo;what works
    in ML.&rdquo; That corpus cannot be replicated by simply spinning up more
    GPUs &mdash; it represents institutional knowledge at network scale.
  </p>
  <p>
    Imagine a dataset that answers questions like:
  </p>
  <ul>
    <li>Across 40 million experiments, which optimiser schedules consistently outperform others for small transformer models?</li>
    <li>How does context length interact with model depth across dozens of hardware tiers?</li>
    <li>What architectural patterns produce the best token efficiency under strict compute budgets?</li>
  </ul>
  <p>
    Most research knowledge today is fragmented across papers, private lab
    notebooks, and unpublished results. The failures, near-misses, and
    surprising parameter combinations that drive real scientific progress mostly
    vanish into internal systems. XeeNet captures that negative space.
  </p>
  <p>
    The ultimate vision:
  </p>
  <ul>
    <li>Millions of volunteer devices run bounded ML experiments continuously</li>
    <li>Research programmes self-direct based on accumulated results and lessons</li>
    <li>A global experiment corpus captures insights across all experiments &mdash; successes and failures alike</li>
    <li>Researchers launch campaigns that build on the accumulated knowledge of every previous campaign</li>
    <li>A sustainable credits economy incentivises long-term participation</li>
    <li>Results are publicly available, advancing open ML research</li>
  </ul>

  <div class="callout">
    <div class="callout-title">The SETI@home Parallel</div>
    <p>
      SETI@home proved that volunteers will donate compute for science. At its peak,
      it had over 5 million participants providing 27 PetaFLOPS. XeeNet applies the
      same model to ML research: instead of searching for extraterrestrial signals,
      we search for optimal neural network architectures &mdash; using workloads
      that are embarrassingly parallel, naturally bounded, and immediately
      verifiable. The compute requirements are similar; the scientific payoff is
      immediate and measurable.
    </p>
  </div>
</div>

<div class="divider"></div>

<div class="section">
  <h2>Risks and Constraints</h2>
  <p>
    These are the dragons in the cave. Each must be addressed deliberately as the
    platform grows through the phases above.
  </p>

  <table>
    <thead>
      <tr>
        <th>Risk</th>
        <th>Phase</th>
        <th>Mitigation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Trust and sandboxing</strong></td>
        <td>2</td>
        <td>Constrained job formats, pre-approved templates, containerised execution, no arbitrary filesystem or network access. The autoresearch contract is itself the primary sandbox.</td>
      </tr>
      <tr>
        <td><strong>Result integrity</strong></td>
        <td>2</td>
        <td>k-of-n redundant execution, cross-worker metric comparison within tolerance, anomaly detection. First-class verification, not an afterthought.</td>
      </tr>
      <tr>
        <td><strong>Malicious workloads</strong></td>
        <td>3</td>
        <td>Workload admission policy engine, deterministic runtime constraints, no arbitrary internet access from tasks, pre-approved execution templates only.</td>
      </tr>
      <tr>
        <td><strong>Dataset privacy</strong></td>
        <td>3</td>
        <td>Public datasets only in early phases. Proprietary data support requires differential privacy, secure enclaves, and data governance review.</td>
      </tr>
      <tr>
        <td><strong>Cold start problem</strong></td>
        <td>2&ndash;3</td>
        <td>Do not build a marketplace first. Build a working network: seed worker fleet, own workloads, prove throughput, then invite external workers, then external researchers.</td>
      </tr>
      <tr>
        <td><strong>Consumer trust optics</strong></td>
        <td>2</td>
        <td>Signed binaries, reproducible runtimes, transparent code, public security review, explicit resource controls, hard caps on power / time / bandwidth.</td>
      </tr>
      <tr>
        <td><strong>Regulatory exposure</strong></td>
        <td>4</td>
        <td>If credits become redeemable or cash-equivalent, financial regulation applies. Start with non-cash reputation scoring; add grants, prizes, or sponsorships before direct financial settlement. Professional legal review before any tokenisation.</td>
      </tr>
      <tr>
        <td><strong>Hardware heterogeneity</strong></td>
        <td>2&ndash;3</td>
        <td>Resource profiles as first-class scheduling inputs, task parameterisation by device tier, regional orchestrators for latency-aware matching.</td>
      </tr>
      <tr>
        <td><strong>Network economics</strong></td>
        <td>3</td>
        <td>Bounded experiments minimise data transfer by design. Small configs in, single metric out. Datasets cached locally on workers, not streamed per task.</td>
      </tr>
    </tbody>
  </table>
</div>
