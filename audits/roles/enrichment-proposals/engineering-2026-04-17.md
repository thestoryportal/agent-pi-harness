# Enrichment Proposals — engineering — 2026-04-17

## AI/ML Engineer
**File:** `~/.claude/roles/engineering/ai-ml-engineer.md`
**JD sources used:** AI Engineer.md, Machine Learning Engineer.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] MLOps tooling access (MLflow, experiment tracking)` — *source: Machine Learning Engineer.md, reason: role ships evaluation harness and regression tests; experiment/version tracking is a concrete dependency the context currently omits*
- `- [ ] Model drift monitoring destination` — *source: Machine Learning Engineer.md, reason: production drift detection is named in the JD and maps to existing "regression suite" language in Quality Bar*

**Edit:** *No edit — existing items are specific nouns and already follow the style guide.*

**No change** on remainder — six items with mixed access / constraint / documentation categories already matches the pattern.

### Key Priorities
**Add:** *None — five bullets already cover integration, prompts, monitoring, evaluation harness, and privacy rules; the style guide caps at 4-6 and every bullet is concrete.*

**Edit:** *No edit — bullets already follow imperative + justification clause pattern with specific artifacts.*

**No change** — existing content matches the style-guide sample the role is named against.

### Quality Bar
**Add:** *None — 5 rows, each with numeric or falsifiable criteria.*

**Edit:** *No edit — this role is one of the four style-guide sample files; criteria already cite <2s / 99.5% / monthly review / consent.*

**No change** — sample file; enrichment would regress it.

---

## Backend Developer
**File:** `~/.claude/roles/engineering/backend-developer.md`
**JD sources used:** Backend Developer.md, backend-javascript-developer.md, C# Backend Developer.md (skimmed, no distinct delta), Python Backend Developer.md (skimmed, no distinct delta)
**JD tiers:** STRONG: 1, GOOD: 3, WEAK: 0

### Required Context
**Add:**
- `- [ ] Third-party integrations inventory (payment gateway, external APIs)` — *source: Backend Developer.md, reason: role's "What You Own" includes external APIs and payment work, but context list omits this concrete artifact*
- `- [ ] Message queue / event bus infrastructure (if any)` — *source: backend-javascript-developer.md, reason: event-driven architecture is explicitly called out; matches `(if any)` suffix convention*

**Edit:** *No edit — existing five items are tight noun phrases.*

**No change** for remaining items — the role is one of the four style-guide sample files.

### Key Priorities
**Add:** *None — five imperative bullets already cover migrations, API conventions, auth partnership, telemetry, and ERD documentation.*

**Edit:** *No edit — bullets are the style-guide reference sample.*

**No change** — sample file; enrichment would regress it.

### Quality Bar
**Add:** *None — 5 numeric-threshold rows already in place.*

**Edit:** *No edit — this role is the style-guide sample for `**API latency**`, `**Query performance**`, etc.*

**No change** — sample file; enrichment would regress it.

---

## Chief Technology Officer
**File:** `~/.claude/roles/engineering/chief-technology-officer.md`
**JD sources used:** Chief Technology Officer (CTO).md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] M&A / due-diligence pipeline (if any)` — *source: Chief Technology Officer (CTO).md, reason: JD names technical due diligence as a recurring CTO input; maps to `(if any)` convention*
- `- [ ] Technology vendor and contract inventory` — *source: Chief Technology Officer (CTO).md, reason: JD explicitly names vendor relationships and contract negotiation; concrete artifact missing from context*

**Edit:** *No edit — existing six noun phrases cover strategy, landscape, team, budget, stakeholders, and market.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five bullets already cover strategy articulation, platform decisions, guardrails, tech-debt budget, and board narrative.*

**Edit:** *No edit — imperative + "so ..." clauses present.*

**No change** — bullets already specific and within 5-bullet cap.

### Quality Bar
**Add:** *None — 5 rows with falsifiable criteria (SLO target, satisfaction trend, debt percentage).*

**Edit:** *No edit.*

**No change** — existing table is well-anchored.

---

## Data Engineer
**File:** `~/.claude/roles/engineering/data-engineer.md`
**JD sources used:** Data Engineer.md, big-data-engineer.md
**JD tiers:** STRONG: 1, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Pipeline orchestration tooling (Airflow, Dagster, Prefect)` — *source: Data Engineer.md, reason: JD explicitly names Airflow/Luigi as standard; role currently lists "Infrastructure available" as a generic noun, this sharpens it*
- `- [ ] Streaming infrastructure (Kafka, Kinesis, Pub/Sub), if any` — *source: big-data-engineer.md, reason: streaming is called out in JD and maps to existing "real-time" vs "daily" split in Quality Bar; `if any` follows style-guide suffix convention*

**Edit:** *No edit — existing seven items are already concrete noun phrases.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five imperative bullets covering ingestion, modeled layer, data quality, PII, and schema/lineage docs.*

**Edit:** *No edit — bullets pair action with justification.*

**No change** — within 4-6 range, each references concrete artifact.

### Quality Bar
**Add:** *None — 5 rows with falsifiable criteria (SLA thresholds, idempotency, PII enforcement, observability).*

**Edit:** *No edit.*

**No change** — existing table already follows style-guide pattern.

---

## Engineering Manager
**File:** `~/.claude/roles/engineering/engineering-manager.md`
**JD sources used:** engineering-manager.md (Workable template — thin), Prompt Engineering Manager.md (not read, no relevant delta expected)
**JD tiers:** STRONG: 1, GOOD: 1, WEAK: 0

### Required Context
**Add:** *None — existing seven items already cite Jira/Linear/Asana, roadmap, capacity plan, on-call rotation, quality docs, and HR policies. JD content is too generic to sharpen.*

**Edit:** *No edit.*

**No change** — required context is already richer than the STRONG JD.

### Key Priorities
**Add:** *None — five bullets cover delivery rhythm, metrics, ownership, incident process, and tech-debt capacity.*

**Edit:** *No edit.*

**No change** — bullets specific and actionable.

### Quality Bar
**Add:** *None — 5 rows with falsifiable criteria (sprint variance, MTTR, handoff artifacts).*

**Edit:** *No edit.*

**No change** — JD provides no sharper thresholds.

---

## Engineering Research Lead
**File:** `~/.claude/roles/engineering/engineering-research-lead.md`
**JD sources used:** *None read — both matches are WEAK (enterprise-architect, director-of-engineering)*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. The role's existing Required Context / Key Priorities / Quality Bar already cite POC workflow, benchmarks, research archive, and reproducibility gates. Adjacent director/architect JDs do not provide sharper research-role artifacts.

---

## Frontend Developer
**File:** `~/.claude/roles/engineering/frontend-developer.md`
**JD sources used:** Frontend Developer.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] State management approach (Redux, Zustand, or none)` — *source: Frontend Developer.md, reason: JD explicitly names state management libraries; role's scope includes complex flows but context omits this architectural dependency*
- `- [ ] Build tooling (Vite, Webpack) configuration access` — *source: Frontend Developer.md, reason: JD calls out build tools as explicit setup work; role owns component architecture but build config is currently implicit*

**Edit:** *No edit — existing five items are tight.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five bullets cover component architecture, design-system tokens, accessibility, tests, and Creative Tech contract.*

**Edit:** *No edit — bullets are imperative with justification.*

**No change** — within 4-6 range.

### Quality Bar
**Add:** *None — 5 rows already cover visual fidelity, performance, a11y (WCAG AA), type safety, test coverage.*

**Edit:** *No edit.*

**No change** — table is well-anchored.

---

## Full Stack Developer
**File:** `~/.claude/roles/engineering/full-stack-developer.md`
**JD sources used:** Full Stack Developer.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] CI/CD pipeline access` — *source: Full Stack Developer.md, reason: JD names CI/CD collaboration as explicit responsibility; role's e2e test key priority implies pipeline access but it's missing from required context*

**Edit:** *No edit — existing five items are tight noun phrases.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five bullets cover end-to-end features, escalation rules, feature-slice pattern, tests, and TypeScript discipline.*

**Edit:** *No edit.*

**No change** — bullets specific and falsifiable.

### Quality Bar
**Add:** *None — 5 rows cover type safety, layer hygiene, tests, escalation, consistency.*

**Edit:** *No edit.*

**No change** — table follows style-guide pattern.

---

## Mobile Developer
**File:** `~/.claude/roles/engineering/mobile-developer.md`
**JD sources used:** Mobile Developer.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] MDM / device management requirements (if enterprise)` — *source: Mobile Developer.md, reason: JD names MDM for enterprise deployments; role currently lists signing certs but not MDM context*
- `- [ ] Crash reporting / analytics SDK choice` — *source: Mobile Developer.md, reason: JD emphasizes monitoring across device/OS versions; concrete SDK dependency currently implicit*

**Edit:** *No edit — existing eight items are already specific.*

**No change** on remainder. Note: existing list has 8 items (above the style guide's 4-7 typical range); avoided adding more than 2 to respect length discipline.

### Key Priorities
**Add:** *None — five bullets cover PWA vs native, device matrix, native-only features, code sharing, and release pipeline.*

**Edit:** *No edit.*

**No change** — bullets are imperative with justification.

### Quality Bar
**Add:** *None — 5 rows cover device coverage, performance, offline, platform fit, release hygiene.*

**Edit:** *No edit.*

**No change** — falsifiable criteria in place.

---

## Performance Engineer
**File:** `~/.claude/roles/engineering/performance-engineer.md`
**JD sources used:** *None read — only WEAK match (site-reliability-engineer)*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 1

Skip — WEAK matches only, content too generic. The role already cites k6, Core Web Vitals (LCP <2.5s, INP <200ms, CLS <0.1), p95 <500ms, RUM, synthetic monitoring. The SRE JD covers reliability not performance optimization, so no sharper thresholds or artifacts would lift cleanly.

---

## Security Engineer
**File:** `~/.claude/roles/engineering/security-engineer.md`
**JD sources used:** security-engineer.md, application-security-engineer.md
**JD tiers:** STRONG: 1, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Security scanning tool inventory (SAST, DAST, dependency scanners)` — *source: application-security-engineer.md, reason: JD explicitly names SAST/DAST/IAST integration into CI/CD; role owns "sensitive-data policy review" but scanner tooling is implicit*
- `- [ ] Threat model for critical flows (if any)` — *source: application-security-engineer.md, reason: threat modeling named as explicit AppSec responsibility; `(if any)` suffix follows style guide*

**Edit:** *No edit — existing six items are concrete.*

**No change** on remainder.

### Key Priorities
**Add:** *None — existing five bullets cover auth strategy, RLS policies, compliance mapping, secrets management, and incident-response runbook. CI/CD scanning integration belongs to Platform Engineering (Security Operations Engineer) per the role's "What You Don't Own" table (Infrastructure security → Platform/DevOps).*

**Edit:** *No edit.*

**No change** — existing bullets do not cross boundary into infrastructure-security territory.

### Quality Bar
**Add:** *None — 5 rows with falsifiable criteria already in place (zero unauthorized paths, OWASP verification, secrets rotation, compliance mapping, audit trail).*

**Edit:** *No edit.*

**No change** — table is well-anchored.

---

## Solutions Architect
**File:** `~/.claude/roles/engineering/solutions-architect.md`
**JD sources used:** *STRONG JD (solutions-architect.md) is a 404 placeholder with no content — 4 lines*
**JD tiers:** STRONG: 1 (placeholder), GOOD: 0, WEAK: 0

Skip — STRONG match JD is a 404 placeholder page containing only an error message. No content available to lift. Existing role appendix already cites ADR log, C4 diagrams, NFR coverage, and reversibility tracking which are concrete artifacts.

---
