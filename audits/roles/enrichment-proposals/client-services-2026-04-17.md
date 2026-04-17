# Enrichment Proposals — client-services — 2026-04-17

**Structural note for downstream consumer:** In these department templates, `### Required Context` lives inside the `## Context Requirements` block (not inside `## Appendix: Project Context` as the style guide states). `### Key Priorities` and `### Quality Bar` live inside `## Appendix: Project Context` as expected. All proposed edits target the section at its actual location in each role file. The same structure holds for the style guide's own reference sample `engineering/backend-developer.md` (verified 2026-04-17, lines 519 and 607), so this is a style-guide documentation gap, not a template mismatch.

---

## Account Manager
**File:** `~/.claude/roles/client-services/account-manager.md`
**JD sources used:** Account Manager.md, technical-account-manager.md, digital-account-manager.md, Key Account Manager.md, National Account Manager.md
**JD tiers:** STRONG: 1, GOOD: 4, WEAK: 0

### Required Context
**Add:**
- `- [ ] CRM platform access (Salesforce or HubSpot)` — *source: Account Manager.md, reason: names the specific tool the role needs credentials for before starting*
- `- [ ] Portfolio revenue targets and quota assignment` — *source: National Account Manager.md, reason: missing revenue accountability context ($500K-$5M+ portfolios) the seat needs on day one*

**Edit:**
- OLD: `- [ ] Satisfaction metrics (NPS/CSAT) and health score` → NEW: `- [ ] Satisfaction metrics (NPS, CSAT, CES) and account health score` — *reason: Customer Success Manager.md and Key Account Manager.md both reference CES alongside NPS/CSAT as standard for 2026*

**No change to the other three items** — charter/engagement-history/renewal items are already concrete.

### Key Priorities
**Add:**
- `Instrument a stakeholder map per account covering economic buyer, champion, detractor, and procurement contact` — *source: Key Account Manager.md, reason: sharper than "decision-makers/champions/detractors" — adds economic buyer and procurement which drive renewal outcomes*
- `Partner with Sales on clean handoff artifacts (signed SOW, success criteria, executive sponsor map) before first QBR` — *source: Customer Success Manager.md, reason: captures the concrete cross-functional artifact the seat must stand up with Sales*

**Edit:**
- OLD: `Build an account plan per client (goals, stakeholders, risks, opportunities)` → NEW: `Build an account plan per client with goals, stakeholders, risks, and 12-24 month expansion targets` — *reason: National Account Manager.md references 12-24 month account plans — adds time horizon and makes "opportunities" specific*

### Quality Bar
**Add:**
- `| **Multi-Thread Coverage** | Every tier-1 account has 3+ named contacts across functions |` — *source: Key Account Manager.md, reason: replaces vague "Multi-threaded contacts" framing with a falsifiable threshold*

**Edit:**
- OLD: `| **Relationship Depth** | Multi-threaded contacts across functions in each account |` → NEW: `| **Relationship Depth** | Named contacts across procurement, economic buyer, and day-to-day roles in each account |` — *reason: Key Account Manager.md — more specific than "multi-threaded", names the three role types to cover*

---

## Client Research Analyst
**File:** `~/.claude/roles/client-services/client-research-analyst.md`
**JD sources used:** market-research-analyst.md, Customer Experience Analyst.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (used lightly)

### Required Context
**Add:**
- `- [ ] Statistical analysis tooling access (R, Python, or SPSS)` — *source: Customer Experience Analyst.md, reason: names the specific toolchain; current items list data but not analysis environment*

**Edit:**
- (no edits — existing seven items are already concrete and complete)

### Key Priorities
**Add:**
- `Stand up a customer-journey map per tier linking touchpoints to satisfaction signals and open research questions` — *source: Customer Experience Analyst.md, reason: concrete setup artifact the seat produces; existing bullets cover VOC and health but not journey mapping*

**Edit:**
- OLD: `Establish a central repository for client insights and themes` → NEW: `Establish a central repository for client insights with tagging by segment, theme, and source method` — *reason: Customer Experience Analyst.md — makes "central repository" falsifiable by naming the required tagging dimensions*

### Quality Bar
**No change** — existing 5 rows are already falsifiable and well-scoped.

---

## Client Success Manager
**File:** `~/.claude/roles/client-services/client-success-manager.md`
**JD sources used:** Customer Success Manager.md, Account Manager.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (used)

### Required Context
**Add:**
- `- [ ] ARR and contract terms per account (renewal date, auto-renew clauses, expansion rights)` — *source: Customer Success Manager.md, reason: renewal logistics are prerequisite; missing from current list*

**Edit:**
- OLD: `- [ ] Platform usage and adoption telemetry` → NEW: `- [ ] Product usage telemetry (feature adoption, MAU/WAU, time-to-value per cohort)` — *reason: Customer Success Manager.md references TTV 30-90 days and feature-adoption tracking — makes the generic "adoption telemetry" concrete*

### Key Priorities
**Add:**
- `Drive renewal discipline with 90-day early-warning triggers on NRR, usage decline, and sponsor change` — *source: Customer Success Manager.md, reason: names the three documented churn signals the seat must instrument*

**Edit:**
- OLD: `Define account health scoring with inputs and thresholds` → NEW: `Define account health scoring with usage, sentiment, and sponsor-engagement inputs and red/yellow/green thresholds` — *reason: Customer Success Manager.md — names the three input dimensions and standard traffic-light bands*

### Quality Bar
**Add:**
- `| **Net Revenue Retention** | NRR tracked per account; portfolio target 110%+ set and reviewed quarterly |` — *source: Customer Success Manager.md, reason: NRR 110-130% is the standard 2026 CSM metric; adds a numeric gate the role currently lacks*

---

## Delivery Manager
**File:** `~/.claude/roles/client-services/delivery-manager.md`
**JD sources used:** Program Manager.md, Project Manager.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (used)

Skip — WEAK matches only, and the existing Required Context / Key Priorities / Quality Bar are already concrete (capacity model by skill and seniority, stage gates, risk register with weekly review, utilization band). WEAK JDs describe program-manager work that overlaps but doesn't add delivery-specific signal beyond what is already present.

---

## Head of Client Services
**File:** `~/.claude/roles/client-services/head-of-client-services.md`
**JD sources used:** Director of Customer Service.md, VP of Customer Service.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (used)

### Required Context
**Add:**
- `- [ ] Annual budget envelope and headcount plan for the department` — *source: VP of Customer Service.md, reason: budget authority context ($5M-$50M+ ranges referenced) is prerequisite for a department head*

**Edit:**
- (no edits — existing items are appropriate)

### Key Priorities
**Add:**
- `Publish quarterly department KPIs (retention, NRR, CSAT, SLA attainment) reviewed with the executive team` — *source: Director of Customer Service.md, reason: names the four KPI families and the cadence — more specific than the current "Retention" quality bar row implies*

**Edit:**
- OLD: `Build an early-warning system for churn and expansion signals` → NEW: `Build an early-warning system for churn and expansion signals with thresholds and a weekly triage ritual` — *reason: VP of Customer Service.md — adds the triage-cadence element so the system has a feedback loop*

### Quality Bar
**Add:**
- `| **Budget Discipline** | Department spend within approved envelope; variances explained monthly |` — *source: VP of Customer Service.md, reason: adds missing financial accountability gate for a head-of role*

---

## Implementation Specialist
**File:** `~/.claude/roles/client-services/implementation-specialist.md`
**JD sources used:** AI Implementation Specialist.md
**JD tiers:** STRONG: 0, GOOD: 1, WEAK: 0

### Required Context
**No change** — existing five items (plan, specs, data, endpoints/credentials/API docs, timeline) are already concrete; AI Implementation Specialist.md does not surface a prerequisite the list doesn't already cover.

### Key Priorities
**Add:**
- `Design a user training curriculum with role-based modules and a recorded asset library for ongoing onboarding` — *source: AI Implementation Specialist.md, reason: more specific than current "short training curriculum and recorded asset library" — adds role-based modularity as the structuring principle*
- `Establish governance checkpoints with IT security and compliance on data-handling and privacy obligations before go-live` — *source: AI Implementation Specialist.md, reason: governance/compliance gate is missing; implementation work routinely blocks on this*

**Edit:**
- OLD: `Define a data migration pattern with validation and rollback` → NEW: `Define a data migration pattern with record-count reconciliation, sample validation, and documented rollback procedure` — *reason: AI Implementation Specialist.md — makes "validation and rollback" falsifiable by naming the three required artifacts*

### Quality Bar
**Add:**
- `| **Change Management** | End users complete role-based training before go-live; adoption tracked 30/60/90 post-launch |` — *source: AI Implementation Specialist.md, reason: adds missing adoption-measurement gate; existing "Enablement" row covers training but not post-launch adoption tracking*

---

## Project Manager
**File:** `~/.claude/roles/client-services/project-manager.md`
**JD sources used:** Project Manager.md, Technical Project Manager.md, Creative Project Manager.md, Digital Project Manager.md, IT Project Manager.md, Architectural Project Manager.md, Construction Project Manager.md, Assistant Project Manager.md
**JD tiers:** STRONG: 1, GOOD: 7, WEAK: 0

### Required Context
**Add:**
- `- [ ] Project management toolchain access (Jira, Asana, Monday.com, or MS Project)` — *source: Project Manager.md, Technical Project Manager.md, IT Project Manager.md, reason: named tooling access is a prerequisite; current list omits the toolchain*
- `- [ ] RACI matrix and team roster with availability` — *source: Project Manager.md, reason: adds the cross-functional ownership artifact; current "Resource allocation and team assignments" is vaguer*

**Edit:**
- OLD: `- [ ] Project schedule, milestones, and critical path` → NEW: `- [ ] Project schedule with baselined milestones, critical path, and dependency map` — *reason: Technical Project Manager.md — adds baseline and dependency-map which are what actually enable slippage detection*

### Key Priorities
**Add:**
- `Configure quality gates and acceptance criteria per milestone before work begins` — *source: Technical Project Manager.md, reason: sharper than the current "charter template" bullet — gives the seat a concrete milestone-level artifact*

**Edit:**
- OLD: `Baseline plans with a critical path and documented assumptions` → NEW: `Baseline plans with a critical path, documented assumptions, and 10-15% contingency buffer for identified risks` — *reason: Technical Project Manager.md and Construction Project Manager.md — adds the standard contingency-buffer practice so the baseline is actionable not aspirational*

### Quality Bar
**Add:**
- `| **Schedule Adherence** | Milestones hit within 10% buffer; slips have root-cause and recovery plan logged |` — *source: Technical Project Manager.md, Construction Project Manager.md, reason: adds numeric threshold to what would otherwise be subjective "on-time" judgment*

---

## Technical Account Manager
**File:** `~/.claude/roles/client-services/technical-account-manager.md`
**JD sources used:** technical-account-manager.md, Account Manager.md
**JD tiers:** STRONG: 1, GOOD: 1, WEAK: 0

### Required Context
**Add:**
- `- [ ] Access to client production logs, error tracking, and API request traces` — *source: technical-account-manager.md, reason: technical-support context is prerequisite; current list has dashboards but not log/trace access*

**Edit:**
- (no edits — existing five items are already concrete)

### Key Priorities
**Add:**
- `Partner with Engineering on a feature-request intake process that returns estimates and roadmap placement to the client` — *source: technical-account-manager.md, reason: specifies the engineering-liaison workflow; current "roadmap review" bullet implies but doesn't name the intake artifact*

**Edit:**
- OLD: `Establish reference integration patterns to shorten future deployments` → NEW: `Establish reference integration patterns (webhook, polling, SDK) with sample code to shorten future deployments` — *reason: technical-account-manager.md (web/SDK integrations) — names the three pattern types so "reference patterns" is concrete*

### Quality Bar
**Add:**
- `| **Technical Depth** | Runbook covers the top 5 client integration issues with documented resolutions |` — *source: technical-account-manager.md, reason: adds a falsifiable knowledge-base gate; current rows cover SLAs and architecture docs but not the runbook*

---
