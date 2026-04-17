# Enrichment Proposals — management — 2026-04-17

## Operations Coordinator
**File:** `~/.claude/roles/management/operations-coordinator.md`
**JD sources used:** Operations Coordinator.md
**JD tiers:** STRONG: 1, GOOD: 0, WEAK: 0

### Required Context
**Add:**
- `- [ ] Project management tool access (Asana, Monday.com, or equivalent) and vendor/procurement system credentials` — *source: Operations Coordinator.md, reason: JD's Corporate template explicitly names these tools as core requirements; current context lists "Tool/resource inventory" but omits the PM tool surface*

### Key Priorities
**Add:**
- `Establish a vendor and purchase-order tracking view with owner, renewal, and spend visibility` — *source: Operations Coordinator.md, reason: JD's Corporate template lists vendor-management and PO processing as core responsibilities; current priorities cover resources generically but not procurement-specifically*

**Edit:**
- OLD: `Standardize session handoff notes so context persists across people` → NEW: `Standardize session handoff notes and prepare weekly operational reports flagging key metrics and risks` — *reason: JD names "weekly operational reports to leadership" as a distinct deliverable; current bullet only covers peer-to-peer handoff*

### Quality Bar
**No change** — existing gates (last-updated dates, week-one productivity, SOP compliance, handoff completeness, resource clarity) are measurable and role-specific.

---

## Project Orchestrator
**File:** `~/.claude/roles/management/project-orchestrator.md`
**JD sources used:** Program Manager.md, Project Manager.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skipped)

Skip — WEAK matches only, insufficient signal. This is a bespoke multi-agent orchestration role; generic Program/Project Manager JDs describe human PM work that doesn't map to the agent-coordination scope. Existing content (Morning/Evening Briefs, escalation triage, shared-state maintenance, decision latency) is specific to the agent-orchestration context and cannot be sharpened by generic PM content.

---

## Quality Coordinator
**File:** `~/.claude/roles/management/quality-coordinator.md`
**JD sources used:** qa-tester.md, AI Quality Assurance Specialist.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skipped)

Skip — WEAK matches only, insufficient signal. Existing content already names unit/integration/E2E tiers, WCAG AA, CI-gated accessibility, and severity rubrics — WEAK QA-tester JDs do not add tool or threshold specificity beyond what the role file already has.

---

## Technical Coordinator
**File:** `~/.claude/roles/management/technical-coordinator.md`
**JD sources used:** Project Coordinator.md, Technical Program Manager.md
**JD tiers:** STRONG: 0, GOOD: 0, WEAK: 2 (skipped)

Skip — WEAK matches only, insufficient signal. Bespoke multi-agent technical-coordination role; generic PM JDs do not map. Existing content (stack + architecture overview, explicit ownership map, tech-debt backlog, CI-enforced standards, workload balance) names concrete artifacts specific to the agent-coordination scope.

---
