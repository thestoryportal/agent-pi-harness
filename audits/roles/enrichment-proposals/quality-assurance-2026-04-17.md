# Enrichment Proposals — quality-assurance — 2026-04-17

## Accessibility Tester
**File:** `~/.claude/roles/quality-assurance/accessibility-tester.md`
**JD sources used:** *Only WEAK matches (qa-tester.md, QA Engineer.md) — both generic QA, no accessibility-specific content*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. Role already cites WCAG 2.1 AA baseline, keyboard navigation, screen reader parity, 4.5:1 / 3:1 contrast, and `prefers-reduced-motion`. Generic QA JDs do not provide sharper accessibility artifacts.

---

## Head of QA
**File:** `~/.claude/roles/quality-assurance/head-of-qa.md`
**JD sources used:** QA Engineer.md (skimmed), manager-of-quality-assurance.md, qa-tester.md (shared), quality-assurance-specialist.md (shared)
**JD tiers:** STRONG: 0, GOOD: 4, WEAK: 0

### Required Context
**Add:** *None — existing seven items already cite PRD, architecture diagram, target platform matrix, QA team roster, release schedule, automation framework docs, and quality gates. JDs provide no sharper artifact at this leadership level.*

**Edit:** *No edit — existing items are concrete.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five bullets cover QA strategy, release gates, specialist coverage, metrics program, and executive representation.*

**Edit:** *No edit — bullets are imperative with justification.*

**No change** — bullets already specific and within 4-6 range.

### Quality Bar
**Add:** *None — 5 rows cover strategy, gates, specialist coverage, metrics visibility, escalation path.*

**Edit:** *No edit.*

**No change** — table well-anchored.

---

## Manual QA Specialist
**File:** `~/.claude/roles/quality-assurance/manual-qa-specialist.md`
**JD sources used:** quality-assurance-specialist.md (thin), AI Quality Assurance Specialist.md
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] AI feature inventory (if any)` — *source: AI Quality Assurance Specialist.md, reason: role increasingly tests AI-backed features; JD names non-deterministic output testing; `(if any)` follows style-guide suffix*

**Edit:** *No edit — existing six items are tight noun phrases covering requirements, acceptance criteria, design specs, environments, bug tracker, scope.*

**No change** on remainder.

### Key Priorities
**Add:**
- `Establish bias and hallucination checks for any AI-powered feature under test` — *source: AI Quality Assurance Specialist.md, reason: JD names bias detection and hallucination prevention as core AI-QA work; only add when project has AI scope — wording is conditional*

**Edit:** *No edit — existing five bullets cover exploratory charters, cross-browser matrix, bug template, regression checklist, and developer triage loop.*

**No change** on remainder. Note: adds one bullet bringing total to 6, within the 4-6 range.

### Quality Bar
**Add:** *None — 5 rows cover critical flows, bug evidence, regression clean, cross-browser, responsive pass.*

**Edit:** *No edit.*

**No change** — well-anchored.

---

## Mobile QA Specialist
**File:** `~/.claude/roles/quality-assurance/mobile-qa-specialist.md`
**JD sources used:** quality-assurance-specialist.md (thin), AI Quality Assurance Specialist.md (no mobile-specific delta)
**JD tiers:** STRONG: 0, GOOD: 2, WEAK: 0

### Required Context
**Add:** *None — existing six items cover target platforms, OS versions, device requirements, responsive breakpoints, PWA and offline requirements.*

**Edit:** *No edit.*

**No change** — JDs do not provide mobile-specific deltas.

### Key Priorities
**Add:** *None — five bullets cover device matrix, touch/gesture/orientation, platform permissions, degraded networks, and mobile-specific perf (battery/memory/thermal).*

**Edit:** *No edit.*

**No change** — bullets are mobile-domain specific, falsifiable.

### Quality Bar
**Add:** *None — 5 rows cover device coverage, responsive, permissions, network resilience, performance.*

**Edit:** *No edit.*

**No change** — well-anchored.

---

## Performance Tester
**File:** `~/.claude/roles/quality-assurance/performance-tester.md`
**JD sources used:** *Only WEAK matches (qa-tester.md, QA Engineer.md) — neither performance-specific*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. Role already cites baseline capture, SLO/SLI targets, representative load scenarios, CI regression detection, and evidence-based recommendations. Generic QA JDs would not sharpen it.

---

## QA Automation Engineer
**File:** `~/.claude/roles/quality-assurance/qa-automation-engineer.md`
**JD sources used:** QA Automation Engineer.md, QA Engineer.md, quality-engineer.md
**JD tiers:** STRONG: 1, GOOD: 2, WEAK: 0

### Required Context
**Add:**
- `- [ ] Framework choice (Cypress, Playwright, Selenium) or constraint` — *source: QA Automation Engineer.md, reason: JD explicitly names Selenium/Cypress/Playwright as standard frameworks; role's key priority mentions "select an E2E framework" but context omits the constraint*
- `- [ ] Test data management strategy` — *source: QA Automation Engineer.md, reason: JD explicitly names test data management; concrete artifact currently implicit*

**Edit:** *No edit — existing six items are tight.*

**No change** on remainder.

### Key Priorities
**Add:**
- `Wire flake detection and quarantine workflow so retries don't mask real failures` — *source: QA Automation Engineer.md, reason: JD calls out flaky test handling; role's existing Quality Bar names `No Flakes` but Key Priorities do not describe the workflow to enforce it*

**Edit:** *No edit — existing five bullets cover unit foundation, integration coverage, E2E framework, CI wiring, and risk-based coverage targets.*

**No change** on remainder. Note: adds one bullet bringing total to 6, within the 4-6 range.

### Quality Bar
**Add:** *None — 5 rows cover CI green, no flakes, critical paths, fast feedback, clear failures.*

**Edit:** *No edit.*

**No change** — well-anchored.

---

## QA Lead
**File:** `~/.claude/roles/quality-assurance/qa-lead.md`
**JD sources used:** qa-tester.md, manager-of-quality-assurance.md, quality-assurance-specialist.md, AI Quality Assurance Specialist.md, QA Automation Engineer.md (re-used), QA Engineer.md (re-used)
**JD tiers:** STRONG: 0, GOOD: 6, WEAK: 0

### Required Context
**Add:** *None — existing six items already cover project scope/timeline, team composition, quality strategy, release schedule, tooling access, stakeholder list. Role is one of the four style-guide sample files.*

**Edit:** *No edit.*

**No change** — sample file; enrichment would regress it.

### Key Priorities
**Add:** *None — five bullets are the style-guide reference (test plan, defect triage, quality gates, workload balance, stakeholder reporting).*

**Edit:** *No edit.*

**No change** — sample file.

### Quality Bar
**Add:** *None — 5 rows are the style-guide reference for the `Triage SLA` / `Regression Clean` pattern.*

**Edit:** *No edit.*

**No change** — sample file.

---

## QA Operations Manager
**File:** `~/.claude/roles/quality-assurance/qa-operations-manager.md`
**JD sources used:** manager-of-quality-assurance.md, quality-manager.md (shared thin), Operations Manager.md (shared)
**JD tiers:** STRONG: 0, GOOD: 3, WEAK: 0

### Required Context
**Add:** *None — existing six items already cite team structure, tools, environment architecture, processes, budget, vendor relationships. JDs (Workable templates) provide no sharper artifact.*

**Edit:** *No edit.*

**No change** on remainder.

### Key Priorities
**Add:** *None — five bullets cover test environments, bug lifecycle, tooling selection, QA metrics, and process docs.*

**Edit:** *No edit — bullets are imperative with concrete artifacts (defect density, escape rate, cycle time).*

**No change** on remainder.

### Quality Bar
**Add:** *None — 5 rows cover env stability, workflow clarity, tooling fit, metrics baseline, process docs.*

**Edit:** *No edit.*

**No change** — well-anchored.

---

## QA Research Lead
**File:** `~/.claude/roles/quality-assurance/qa-research-lead.md`
**JD sources used:** qa-tester.md (shared), manager-of-quality-assurance.md (shared), quality-assurance-specialist.md (shared), QA Engineer.md (shared)
**JD tiers:** STRONG: 0, GOOD: 4, WEAK: 0

### Required Context
**Add:** *None — existing six items cover current tooling, pain points, team capabilities, constraints, tech stack, quality targets.*

**Edit:** *No edit.*

**No change** — shared GOOD JDs do not add distinct research-role artifacts.

### Key Priorities
**Add:** *None — five bullets cover gap mapping, objective-criteria evaluation, methodology playbooks, trend tracking, and pilot-before-adoption.*

**Edit:** *No edit.*

**No change** — bullets specific and falsifiable.

### Quality Bar
**Add:** *None — 5 rows cover evidence-based, comparative, reusable, capacity-aware, traceable.*

**Edit:** *No edit.*

**No change** — well-anchored.

---

## Security Tester
**File:** `~/.claude/roles/quality-assurance/security-tester.md`
**JD sources used:** *Only WEAK matches (qa-tester.md, penetration-tester.md, security-analyst.md) — not read; existing role content already concrete*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 3

Skip — WEAK matches only, content too generic. Role already cites dependency/supply-chain audits, OWASP Top 10 applicability, input/auth/authz/session validation, secrets hygiene, and PoCs with remediation. Penetration-tester and security-analyst JDs would cover adjacent red-team or SOC work, not the AppSec-adjacent tester scope already captured.

---

## UAT Coordinator
**File:** `~/.claude/roles/quality-assurance/uat-coordinator.md`
**JD sources used:** *Only WEAK matches (qa-tester.md, QA Engineer.md) — neither UAT-specific*
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2

Skip — WEAK matches only, content too generic. Role already cites UAT scope, entry/exit criteria, representative user cohorts, scenario catalog, structured feedback, and explicit sign-off. Generic QA JDs do not provide sharper UAT-specific artifacts.

---
