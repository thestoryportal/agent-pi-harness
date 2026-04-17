# Enrichment Proposals — data-analytics — 2026-04-17

## Analytics Engineer
**File:** `~/.claude/roles/data-analytics/analytics-engineer.md`
**JD sources used:** bi-consultant.md, Data Engineer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

### Required Context
**Add:**
- `- [ ] Semantic/metrics layer definition` — *source: Data Engineer.md, reason: role exposes governed marts (LookML/Cube/dbt metrics class); current context lists KPI definitions but not the semantic-layer artifact they live in*

**No edit** (existing 5 items are already concrete: warehouse, dbt project, event schemas, KPI definitions, CI/CD)

### Key Priorities
**Add:**
- `Publish a data-contract pattern for upstream producers so schema breaks surface at the boundary, not in marts` — *source: Data Engineer.md, reason: JD names schema evolution and pipeline quality; current priorities cover staging and testing but not producer-side contracts*

**No edit** (existing 5 priorities are already strong)

### Quality Bar
**Add:**
- `| **Metric parity** | Every KPI in a mart reconciles to the metrics-layer definition |` — *source: Data Engineer.md + bi-consultant.md, reason: role sits between warehouse and semantic layer; adds a falsifiable parity gate absent from current 5 rows; net add — reviewer to retire one existing row (candidate: Review, which is less domain-specific) if 5-row ceiling holds*

**No edit** (existing 5 gates are tight)

---

## Analytics Operations Manager
**File:** `~/.claude/roles/data-analytics/analytics-operations-manager.md`
**JD sources used:** analytics-manager.md, Operations Manager.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] Data governance policy` — *source: analytics-manager.md + Operations Manager.md, reason: JD emphasises governance/compliance (PII handling, retention, access review cadence); current context names RBAC but not the broader governance policy*

**No edit** (existing 5 items cover stack, RBAC, vendors, priorities, open requests)

### Key Priorities
**Add:**
- `Publish quarterly access review so RBAC stays tied to current team composition and role changes` — *source: analytics-manager.md, reason: JD emphasises governance and team management; current priorities cover RBAC setup but not periodic review*

**No edit** (existing 5 priorities cover inventory, RBAC, onboarding, vendors, runbooks)

### Quality Bar
**Add:**
- `| **Access currency** | 100% of active grants reviewed within the last 90 days |` — *source: analytics-manager.md, reason: JD stresses governance discipline; adds a falsifiable SLA absent from the 5 rows; net add — reviewer to retire one existing row (candidate: Access governance, which this replaces with a measurable version) if 5-row ceiling holds*

**No edit** (existing 5 gates are already concrete and falsifiable)

---

## BI Developer
**File:** `~/.claude/roles/data-analytics/bi-developer.md`
**JD sources used:** bi-(business-intelligence)-developer.md
**JD tiers:** STRONG: 1, GOOD: 2 (not read; STRONG covered span), WEAK: 0

### Required Context
**Add:**
- `- [ ] Row-level security policy` — *source: bi-(business-intelligence)-developer.md, reason: JD names security/integrity concerns (row-level and column-level); current context lists workspace credentials but not the access-policy artifact*

**No edit** (existing 5 items are already specific)

### Key Priorities
**Add:**
- `Publish dashboard usage telemetry so stale dashboards get deprecated instead of accumulating` — *source: bi-(business-intelligence)-developer.md, reason: JD names evaluating/improving existing BI systems; current priorities cover deprecation process but not the telemetry that triggers it*

**Edit:**
- OLD: `Ship the executive KPI dashboard first (north-star metrics only)` → NEW: `Ship the executive KPI dashboard first with north-star metrics sourced only from the metrics layer` — *reason: JD Quality Bar already says "naming match metrics layer"; tightens the first-ship priority to match*

### Quality Bar
**Add:**
- `| **Sunset rate** | Dashboards with <5 monthly views archived within one quarter |` — *source: bi-(business-intelligence)-developer.md, reason: JD lists BI system improvement; adds a falsifiable deprecation threshold; net add — reviewer to retire one existing row (candidate: Review, the least falsifiable of the current five) if 5-row ceiling holds*

**No edit** (existing 5 gates are already strong: governed marts, 5s load, WCAG, naming, review)

---

## Data Analyst
**File:** `~/.claude/roles/data-analytics/data-analyst.md`
**JD sources used:** Data Analyst.md
**JD tiers:** STRONG: 1, GOOD: 2 (not read; STRONG covered span), WEAK: 0

### Required Context
**Add:**
- `- [ ] Python/R notebook environment` — *source: Data Analyst.md, reason: JD must-have Python/R plus SQL and cloud warehouse drivers; current context names SQL IDE but not the analytical notebook surface*

**No edit** (existing 6 items are already among the sharpest in the role set)

### Key Priorities
**Add:**
- `Build two or three self-service dashboards for the highest-volume recurring questions to reduce ad-hoc load` — *source: Data Analyst.md, reason: JD emphasises self-service analytics; current priorities cover intake SLA but not the shift-left to dashboards*

**No edit** (existing 5 priorities are strong)

### Quality Bar
**Add:**
- `| **Turnaround** | Standard analysis requests delivered within 3 business days |` — *source: Data Analyst.md, reason: JD lists SLA/responsiveness; current gates cover accuracy/reproducibility but not delivery speed; net add — reviewer to retire one existing row (candidate: Caveats, partly overlapping with Narrative row) if 5-row ceiling holds*

**No edit** (existing 5 gates are strong)

---

## Data Analytics Research Lead
**File:** `~/.claude/roles/data-analytics/data-analytics-research-lead.md`
**JD sources used:** lead-data-scientist.md, Data Scientist.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

### Required Context
**Add:**
- `- [ ] Statistical tooling access` — *source: Data Scientist.md, reason: JD lists statistical methods (Python stats libraries, R, or similar) as must-have; current context omits the statistical-compute surface*

**No edit** (existing 5 items cover priorities, stack, requests, trends, budget)

### Key Priorities
**Add:**
- `Stand up an A/B testing review loop so every experiment has pre-registered hypothesis, power calc, and guardrail metrics` — *source: Data Scientist.md, reason: JD names experimental design as core; current priorities cover flagship projects but not the review loop*

**No edit** (existing 5 priorities cover operating model, library, flagships, evaluation, mentoring)

### Quality Bar
**Add:**
- `| **Experiment hygiene** | Every shipped A/B test has power analysis and guardrail metrics logged |` — *source: Data Scientist.md + lead-data-scientist.md, reason: JD stresses statistical rigor; adds a concrete experiment-hygiene gate; net add — reviewer to retire one existing row (candidate: Statistical correctness, subsumed by this more-specific experiment row) if 5-row ceiling holds*

**No edit** (existing 5 gates cover rigor, reproducibility, stakeholder value, statistical correctness, peer review)

---

## Data Quality Engineer
**File:** `~/.claude/roles/data-analytics/data-quality-engineer.md`
**JD sources used:** quality-engineer.md, Data Engineer.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] Data quality framework access` — *source: Data Engineer.md, reason: JD names automated data quality monitoring (Great Expectations/dbt tests/Soda class); current context lists warehouse schemas but not the DQ framework*

**No edit** (existing 7 items are already the sharpest in the data-analytics set)

### Key Priorities
**Add:**
- `Codify root-cause analysis template (5 Whys, fishbone) so every quality incident produces a tracked corrective action` — *source: quality-engineer.md, reason: JD lists root-cause tools explicitly; current priorities cover postmortems but not the RCA framework itself*

**No edit** (existing 5 priorities cover dimensions, tests, monitoring, on-call, reconciliation)

### Quality Bar
**Add:**
- `| **Alert precision** | True-positive rate on DQ alerts >80% over trailing 30 days |` — *source: quality-engineer.md, reason: QA domain stresses alert quality; adds a numeric signal-to-noise gate absent from current rows; net add — reviewer to retire one existing row (candidate: Alert action, partly overlapping with this alert-quality gate) if 5-row ceiling holds*

**No edit** (existing 5 gates are highly concrete)

---

## Head of Data Analytics
**File:** `~/.claude/roles/data-analytics/head-of-data-analytics.md`
**JD sources used:** analytics-manager.md, lead-data-engineer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

### Required Context
**Add:**
- `- [ ] Data platform vendor contracts` — *source: lead-data-engineer.md + analytics-manager.md, reason: JD emphasises platform management at scale (renewal and commit schedule); current context lists infrastructure inventory but not the commercial commitments*

**No edit** (existing 5 items cover strategy, team, infra, demand, governance)

### Key Priorities
**Add:**
- `Publish quarterly analytics scorecard covering request volume, SLA attainment, and metric reliability to executives` — *source: analytics-manager.md, reason: JD lists executive reporting; current priorities cover strategy and cadence but not the scorecard artifact*

**Edit:**
- OLD: `Set up data governance: naming, catalog, access control, deprecation` → NEW: `Set up data governance: naming convention, data catalog, access control policy, and documented deprecation process` — *reason: JD names each as a distinct governance pillar; sharpens colon list into four named artifacts*

### Quality Bar
**Add:**
- `| **Capacity forecast** | Analytics hiring plan published 2 quarters ahead of demand projections |` — *source: analytics-manager.md, reason: JD stresses team management and scaling; current gates cover hiring bar but not forward-looking capacity planning; net add — reviewer to retire one existing row (candidate: Hiring, partly subsumed by this forward-looking plan row) if 5-row ceiling holds*

**No edit** (existing 5 gates cover metric integrity, trust, delivery, compliance, hiring)

---

## Tracking Instrumentation Specialist
**File:** `~/.claude/roles/data-analytics/tracking-instrumentation-specialist.md`
**JD sources used:** analytics-manager.md, Data Engineer.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

### Required Context
**Add:**
- `- [ ] CI schema validation tooling` — *source: Data Engineer.md, reason: JD names automated data quality monitoring (Segment Protocols/Avo/custom JSON-schema class); current context mentions QA process but not the CI-stage validation tool*

**No edit** (existing 5 items cover feature specs, schema registry, consent policy, destinations, taxonomy)

### Key Priorities
**Add:**
- `Instrument a tracking-change review gate in CI so non-conforming event payloads fail the build` — *source: Data Engineer.md, reason: JD emphasises data quality controls; current priorities mention pre-release validation but not the CI-gate enforcement*

**No edit** (existing 5 priorities cover tracking plan, registry, taxonomy, validation, PII)

### Quality Bar
**Add:**
- `| **Change lead time** | New events from request to production within 2 sprint cycles |` — *source: analytics-manager.md, reason: JD emphasises delivery cadence; adds a numeric lead-time SLA absent from current rows; net add — reviewer to retire one existing row (candidate: Review, the least falsifiable of the five) if 5-row ceiling holds*

**No edit** (existing 5 gates cover schema conformance, PII, consent, review, coverage)

---
