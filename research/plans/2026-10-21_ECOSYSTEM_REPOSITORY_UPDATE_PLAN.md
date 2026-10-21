# Ecosystem Repository Update Plan

_Prepared: 2026-10-21 (Asia/Katmandu)_
_Purpose: Coordinate the next substantial update cycle across the locally available repositories._

## Evidence labels

- **VERIFIED LOCAL:** directly observed in a local checkout on 2026-10-21. This does not establish live GitHub state.
- **HISTORICAL CONTEXT:** prior memory or repository documents; refresh before acting.
- **PROPOSED:** sequencing, scope, or acceptance criteria for future work.
- **UNKNOWN:** not inspected or not established by current evidence.

This is a planning artifact. No implementation, test suite, branch switch, issue/PR operation, commit, or push is authorized by this document.

## 1. Executive sequence

1. **Protect and classify existing local work.** Resolve the dirty-state and branch-divergence items in §2 before broad updates.
2. **Refresh active project state from primary evidence.** Reconcile BiasAperture issues/PRs and statistical acceptance; confirm SPARK hardware, ethics, and report evidence gates; review the active Agent-Customization-Sync feature branch.
3. **Deliver the next bounded project milestones.** BiasAperture and SPARK have concrete research acceptance gates and should lead substantive work. Keep each repository's release and verification workflow independent.
4. **Synthesize verified changes into the portfolio.** Retain the existing portfolio roadmap edit, then update content only from source commits and artifacts that can be checked.
5. **Run a repository-by-repository ecosystem health pass.** Refresh status, contracts, and checks for the remaining local repositories. Do not bulk synchronize branches or apply a sweeping feature set.

## 2. Local state inventory and constraints

The following snapshot came from local Git metadata. `main...origin/main` means the local branch reports tracking that remote ref; it does not prove the remote server is current. Clean status also does not establish product correctness.

| Repository | Local branch / HEAD on 2026-10-21 | Work constraint or immediate action |
| :--- | :--- | :--- |
| `brainstorm` | `main`, `5721b74`, clean and tracking | Use this document as the coordination plan. Update the knowledge graph when architecture/specification sources change, not for every routine note. |
| `Fleet-Orchestrator` | `main`, `9aeb8a7`; three modified `orchestrator-state` files | Preserve `azmuth_burst_history.jsonl`, `azmuth_ingestion_feed.jsonl`, and `azmuth_run.json`. Classify runtime state and back it up before any branch or sync operation. |
| `Agent-Customization-Sync` | `feat/codex-memory-mirror-#1`, `2c013ca`, clean | Review issue/PR, intended acceptance, and branch delta before deciding whether to continue, revise, or integrate. Do not assume this feature branch is disposable. |
| `BiasAperture` | `main`, `c8ff9f7`, clean and tracking | Refresh live issues, PR heads/reviews, and exact code/artifact state before implementation. Existing Phase 2 plan is dated 2026-10-13 and explicitly requires a live refresh. |
| `SPARK` | `main`, `e9ba53d`, clean and tracking | Follow the existing preparation → procurement → logger validation → approval → cohort → integrated evaluation dependency gates. Preserve separation of the 100 Hz model convention and planned 200 Hz logger. |
| `AaradhyaDT.github.io` | `main`, `8d0377b`; `dev-logs/EVOLUTION_AREAS.md` modified | Preserve and review this existing roadmap edit. Verifier passed all 26 categories on the previously inspected baseline; rerun after any portfolio edits. |
| Organization portfolio mirror `Aaradhya-Dev-Tamrakar.github.io` | `main`, `cf44908`; `assets/css/style.css` modified; tracking state `ahead 1, behind 37` | Preserve the CSS edit. Compare local/remote histories and inspect the CSS diff before any reconciliation. No reset, pull, or push until provenance and desired target are clear. |
| Profile mirror `AaradhyaDT` | `main`, `ad2aa1d`, tracking | Local log is dated 2026-10-03; assess whether this repo is in scope for the update cycle and compare with its authoritative source before syncing. |
| Personal portfolio profile repo `AaradhyaDT.github.io` (under ecosystem root) | `main`, `e2db02d`; `ahead 1, behind 37` | This is distinct from the canonical website checkout at `F:\AaradhyaDT\AaradhyaDT.github.io`. Establish remote identity and intended mirror relationship before reconciling. |
| `makerspace` | `main`, `902be16`; `ahead 1, behind 21` | Inspect local commit and remote history before deciding if sync is appropriate. |
| `Claude-Desktop` | `main`, `49d340f`; one modified skill path | Preserve and inspect `Claude Skills + MCP/chat-archiver.skill`; determine whether it is generated, user-authored, or sync output before touching. |
| `Competitive-Programming` | `main`, `4c6d51a`; modified `runtimes/global_references/INDEX.md` | Preserve and review the index edit. This checkout was outside the original primary scope and needs explicit inclusion in a later wave. |
| `FuseAIF2026` | `main`, `32c9a1b`, clean and tracking | Recent commit reports Week 18 module and report. Refresh course milestones and evidence before portfolio claims. |
| `super-nlm` | `main`, `b74f077`, clean and tracking | Last local commit 2026-10-15; do a focused process-lifecycle and NotebookLM workflow health check if selected for this cycle. |
| `google-classroom-mcp` | `main`, `b53c2c8`, clean and tracking | Last local commit 2026-10-14; inspect current API scopes, token handling, and documented copy semantics if selected. |
| `system-optimizer` | `main`, `6a6397c`, clean and tracking | Recent Windows 10 compatibility/release change; confirm artifact and compatibility evidence before cross-linking. |
| `freecad-mcp` | `main`, `78bf023`, clean and tracking | Run a targeted status check only if included in this release cycle; do not infer integration readiness from repository presence. |
| `github-pilot` | Local repository exists in workspace roots; current status not captured in the inventory command | Inspect separately before scheduling work. |
| `md2pdf-desktop` | Local repository exists in workspace roots; current status not captured in the inventory command | Inspect separately before scheduling work. |
| Other registered/local repos | Registry includes additional modules and templates; not all were inspected | Treat each as **UNKNOWN** until a fresh Git and project-specific verification pass is recorded. |

### Non-negotiable preservation rules

- Never discard or overwrite the modified Fleet runtime state, portfolio CSS, Claude skill file, Competitive-Programming index, or the portfolio roadmap edit as part of this plan.
- Do not use `sync.ps1 -AllBranches`, `-CrossPull`, or another broad sync until each dirty/diverged checkout has been reconciled individually.
- Do not dispatch Fleet/cloud work during repository planning or reliability review.
- Do not treat tracker prose, CI success, branch tracking, or a clean tree as proof of scientific results, production behavior, or mirror equality.

## 3. Workstreams and gates

### Wave A — Reconciliation and source-of-truth map

**Repositories:** Fleet-Orchestrator, Agent-Customization-Sync, the two portfolio mirrors, makerspace, Claude-Desktop, Competitive-Programming.

**Proposed tasks:**

- Capture exact diffs and classify each dirty file as intentional source, generated output, operational state, or unresolved.
- For each diverged branch, compare merge bases, unique commits, remotes, and file-level changes; document the intended canonical repository and direction of propagation.
- Inspect the Agent-Customization-Sync feature branch's issue/PR and acceptance state.

**Exit gate:** Every dirty/diverged item has an owner, source of truth, preservation location, and explicit next action. No repository history has been rewritten or synchronized merely to make status appear clean.

### Wave B — Evidence-led research milestones

#### BiasAperture

**Proposed first action:** Refresh current live GitHub issues, PR heads, reviews, CI, and local branch ancestry; compare them to `docs/fellowship/PHASE_2_FINAL_STATE_AND_EXECUTION_PLAN_2026-10-13.md`.

**Candidate milestone:** Reconcile the matched-cohort experiment contract and subgroup uncertainty path, then execute only after the statistical acceptance criteria, inputs, and provenance are agreed.

**Acceptance gate:** Same validation IDs and task-compatible model comparison; bootstrap budget is forwarded to subgroup intervals with at least 1,000 draws; interval method and unavailable cases are reported honestly; dataset/cohort counts reconcile; inference outputs link to immutable inputs/checkpoints/code; independent reproduction is distinguished from unit tests and CI.

**Constraints:** Keep `src/bias_aperture/schema.py` locked unless an explicit project decision changes that contract. Do not expand datasets, model count, SHAP, dashboard, or commercial scope before the core comparison is reproducible.

#### SPARK

**Proposed first action:** Reconcile current board, BOM/protocol, report sources, evidence ledgers, logger requirements, and institutional approval status.

**Dependency gate:** Reconcile requirements → procure after the specified holiday window and fresh quotes → assemble and validate the planned 200 Hz logger → obtain approval before any participant recording → collect the approved cohort → perform integrated evaluation.

**Acceptance gate:** Keep the existing 100 Hz / 200 sample / six-channel / two-second model convention distinct from the planned 200 Hz logger. Reconcile threshold conflicts and firmware gaps; do not claim deployment, physical-unit calibration, latency, or cohort performance without direct evidence.

#### Fleet-Orchestrator

**Proposed first action:** Preserve and classify the three modified runtime-state files, then refresh the Azmuth GUI/job-lifecycle review against current code.

**Candidate reliability gate:** Confirm visible success/failure state matches actual job outcome, cancellation/timeout behavior is bounded, telemetry reflects real controls, and failures are recoverable. Use local/fake jobs only for review until separately authorized cloud execution exists.

### Wave C — Tooling and education repositories

After Wave A is resolved, select bounded work in `Agent-Customization-Sync`, `super-nlm`, `google-classroom-mcp`, `FuseAIF2026`, `system-optimizer`, `freecad-mcp`, `github-pilot`, and `md2pdf-desktop` based on demonstrated user need or a reproducible defect.

**Proposed health record per selected repo:** canonical remote/branch, dirty state, last verified commit, project-specific test/verification command and result, known blocker, active issue/PR, and whether the change affects downstream consumers.

**Exit gate:** No feature is scheduled solely because a repo is old or clean. A work item must have an observable outcome and repo-specific acceptance criteria.

### Wave D — Portfolio synthesis and ecosystem records

**Repositories:** Canonical personal site `F:\AaradhyaDT\AaradhyaDT.github.io`, then any explicitly confirmed mirrors; `brainstorm` registry/contracts only where the actual ecosystem relationships changed.

**Proposed tasks:**

- Keep the current `EVOLUTION_AREAS.md` edit as existing work; reconcile it with verified project milestones before adding new claims.
- Update project cards, achievements, or journey items only from source commits, reproducible reports, and reviewable proof assets.
- Use the portfolio's deterministic project onboarding tool for new project cards; verify generated IDs, encrypted links, filters, search index, and assets.
- Update ecosystem registry/contracts only when a module or relationship actually changed, then regenerate Graphify for architecture/specification changes.

**Exit gate:** Every quantitative or status claim maps to a source artifact and commit; proposed, historical, measured, and independently reproduced results remain distinct; the portfolio verifier passes.

## 4. Per-repository execution contract

Before implementation in any repository:

1. Re-read its current `AGENTS.md`, tracker, and workflow script; confirm the active branch and exact clean/dirty state.
2. Refresh live issue/PR/CI state where task status depends on GitHub.
3. Define a bounded change, non-goals, evidence tier, and acceptance checklist. For non-trivial code work, anchor to the repository's issue/PR workflow.
4. Preserve uncommitted user work; use an isolated worktree when changes must coexist.
5. Run only the repository-specific verification relevant to the selected scope; record exact command, commit, and result.
6. Synchronize only that repository through its authoritative wrapper after its gate passes. Never bulk-push the ecosystem as one transaction.

## 5. Suggested milestone board

| ID | Work item | Depends on | State |
| :--- | :--- | :--- | :--- |
| E0 | Preserve and classify dirty/diverged checkout state | None | **PROPOSED — first** |
| E1 | Refresh BiasAperture live PR/issue and experiment baseline | E0 for branch operations | **PROPOSED — high priority** |
| E2 | Reconcile SPARK dependency/evidence gates | None | **PROPOSED — high priority** |
| E3 | Review Agent-Customization-Sync feature branch acceptance | E0 | **PROPOSED** |
| E4 | Re-audit Fleet job lifecycle using local/fake jobs | Preserve runtime state | **PROPOSED** |
| E5 | Focused health pass over remaining local repos | E0 | **PROPOSED** |
| E6 | Portfolio synthesis from accepted, verified milestones | E1–E5 as applicable | **PROPOSED — downstream** |
| E7 | Update registry/contracts/Graphify for actual architecture changes | Accepted architecture changes | **CONDITIONAL** |

## 6. Evidence sources and refresh notes

**VERIFIED LOCAL on 2026-10-21:** Git branch/HEAD/status inventory for repositories under `F:\Aaradhya-Dev-Tamrakar`, the personal portfolio checkout, the brainstorm graph report, the SPARK report index, the BiasAperture Phase 2 plan, and the ecosystem registry.

**Historical context requiring refresh:** SPARK's report/thesis evidence and dependency ordering; Fleet's previous GUI review; BiasAperture's October 13 execution plan. These records guide what to recheck but do not establish today's issue, PR, CI, hardware, approval, or experiment state.

**Not yet verified:** Live GitHub branch/PR state for this plan, remote equality for local tracking refs, test status for repositories not run, current external service readiness, and whether dirty files are intended for publication.

## 7. Completion criteria for the update cycle

- Every active workstream has a current source-of-truth record, owner, bounded acceptance checklist, and evidence tier.
- Dirty/diverged files and branches are either deliberately retained, reconciled with documented provenance, or explicitly deferred; none are silently discarded.
- Research outputs are reproducible from recorded inputs, code/checkpoint revisions, and parameters, or are labeled as unverified.
- Each changed repository passes its own required checks and uses its own synchronization workflow.
- Portfolio and ecosystem claims are updated only after their source repositories meet acceptance; no fabricated release identifiers, results, dates, or commit SHAs are introduced.
