# Skill Development — Phase 0 Manual Walkthroughs

**Date:** 2026-04-17
**Purpose:** Walk 3 slugs through the full 6-step chain before writing the /infinite loop spec.
**Key questions:**
- Q1: Is role file update coordination a real risk (shared slugs → multiple role files)?
- Q2: Is /infinite the right primitive, or should we build a sequential queue worker?

**Decision predicate (set before walkthroughs):**
- If CEO gate is a serializing bottleneck in Walkthrough 1, Walkthroughs 2+3 confirm nothing additional about Q2. Skip to spec decision after W1 in that case.
- Short-circuit condition: if marketplace (Step 1) returns a good enough community skill, the walkthrough ends at Step 1. That's a valid observation.

**Stub format:** flat `~/.claude/skills/<slug>.md` — matches existing 10 stubs; dir-based form reserved for invocable skills.

---

## Walkthrough 1: wcag-2.1

**Category:** Standards-backed
**Source:** context7 `/websites/w3_wai_wcag22` (WCAG 2.2, 4355 snippets, High reputation)
**Referencing roles:** quality-assurance/accessibility-tester
**Skill file:** `~/.claude/skills/wcag-2.1.md`

### Step 1: Marketplace Check
- `skills find wcag` → no results; `skills find accessibility` → no results
- Community skill found in context7 resolve: `/alexsnchz/skills` "WCAG Design" (Medium rep, WCAG 2.2, design-focused) — **no short-circuit**: wrong version, wrong focus (design vs. testing/audit)
- **Friction:** `npx skills` resolves to wrong binary; correct binary is `skills` (Volta global). find-skills SKILL.md says `npx skills` — instruction is wrong.
- **Three marketplaces confirmed (2026-04-17 correction):**
  1. `skills` (skills.sh) — `skills find <keyword>` via Volta binary; discovery via web leaderboard
  2. `/learn:learn` (agentskill.sh) — keyword search: `/learn wcag`; install: `/learn @owner/name`; no auth
  3. skillsmp REST API — `SKILLSMP_API_KEY` in header; key in .env but not auto-loaded in shell

### Step 2: Fetch Source Material
- WebFetch permission denied (not in settings allowlist)
- Used context7 `resolve-library-id` + `query-docs` — worked well for standards docs
- WCAG 2.1-specific entry (12 snippets) vs WCAG 2.2 (4355 snippets) — used 2.2 as richer source
- **Decision:** Use WCAG 2.2 context7 source for 2.1 skill (2.2 is backward compatible)

### Step 3: Draft Skill File
- 172 lines, covered POUR, conformance levels, SC tables (A+AA), testing workflow, ARIA patterns, common failures, checklist
- No git repo at `~/.claude/skills/` — pre-CEO state not commit-tracked
- **Friction:** Skills stubs have no version control; CEO diff not automatically tracked

### Step 4: CEO Review
- Board: Sonnet 4.6, Gemini 2.5 Flash, GPT-4o. CEO: Claude Opus 4.7
- **CEO picked Sonnet primary + Gemini secondary**
- Sonnet caught 7 technical *errors* (not just gaps): 4.1.1 framing, 1.4.12 missing property, 1.4.10 wrong test method, 1.4.3 missing px equivalents, aria-modal unreliability, tab pattern wrong keyboard model, Section 508 legal framing wrong
- Gemini caught 6 missing SCs (2.2.1, 2.2.2, 2.4.5, 2.4.8, 3.2.3, 3.2.4) + design review phase + Windows High Contrast + prefers-reduced-motion
- GPT-4o too generic (3/10 actionability)
- **CEO review signal: HIGH value** — caught errors that would cause agent to validate broken implementations as passing

### Step 5: Apply Feedback, Finalize
- 172 → 242 lines after all corrections applied
- All 7 errors fixed; 6 missing SCs added; WCAG 2.2 note added; JAWS, WHCM, prefers-reduced-motion, SPA testing, design review phase added
- `~/.claude/skills/wcag-2.1.md` (no git commit — no repo)

### Step 6: Update Role Files
- `~/.claude/roles/quality-assurance/accessibility-tester.md` — Required Skills table updated: wcag-2.1.md marked ✅ Available with status column added
- Commit: `cd1a115` in roles repo

### Observations
- **Friction points:**
  1. `npx skills` vs `skills` binary — find-skills SKILL.md instruction is wrong; correct invocation is bare `skills` command via Volta
  2. WebFetch not permitted by default — docs-scraper path also blocked; context7 was the effective workaround for standards docs
  3. Skills stubs have no git repo — CEO diff not trackable via commits; workaround is line count comparison (172→242)
- **Decisions not obvious:**
  1. Use WCAG 2.2 context7 source for a 2.1-titled skill — correct choice (richer, backward-compatible) but not obvious from the workflow spec
  2. Flat `.md` vs dir-based skill — correct choice is flat for knowledge stubs, but workflow spec doesn't state this rule
- **CEO review signal:** Highest-value step in the chain. Caught 7 factual errors in the draft — not just "could add more", but "this is wrong and will cause false-pass audits". Would not have caught these without CEO review.
- **Time:** ~45 minutes total
- **Parallel-safe?** Step 1 (marketplace) and Step 2 (fetch) can run in parallel. Steps 3-5 are serial (draft → review → revise). Step 6 (role update) is serial with Step 5. Multiple agents working different slugs could safely run Steps 1-2 in parallel, but CEO review creates a natural serialization point (one review per slug). Role file updates could conflict if two slugs reference the same role file.

---

## Walkthrough 2: playwright-patterns

**Category:** Technology-specific
**Source:** Playwright official docs (context7)
**Referencing roles:** quality-assurance/qa-automation-engineer

### Step 1: Marketplace Check
### Step 2: Fetch Source Material
### Step 3: Draft Skill File
### Step 4: CEO Review
### Step 5: Apply Feedback, Finalize
### Step 6: Update Role Files
### Observations
- **Friction points:**
- **Decisions not obvious:**
- **CEO review signal:**
- **Time (minutes):**
- **Parallel-safe?**

---

## Walkthrough 3: stakeholder-management

**Category:** General-professional
**Source:** PMI/professional frameworks synthesis
**Referencing roles:** quality-assurance/uat-coordinator, others

### Step 1: Marketplace Check
### Step 2: Fetch Source Material
### Step 3: Draft Skill File
### Step 4: CEO Review
### Step 5: Apply Feedback, Finalize
### Step 6: Update Role Files
### Observations
- **Friction points:**
- **Decisions not obvious:**
- **CEO review signal:**
- **Time (minutes):**
- **Parallel-safe?**

---

## Cross-Walkthrough Summary (fill after all 3)

### Q1: Role file update coordination risk
- Shared slugs found:
- Role files implicated per slug:
- Conflict risk:
- Recommended commit batching:

### Q2: /infinite vs queue worker
- CEO gate: serializing or parallelizable?
- Parallelism savings vs coordination overhead:
- Recommendation:

### Spec inputs (feed into skill-registry.yaml design)
- Registry format that worked:
- Role-knowledge rubric dimensions:
- Execution primitives needed:
