# Skill Development — Phase 0 Manual Walkthroughs

**Date:** 2026-04-17
**Purpose:** Walk 3 slugs through the full 6-step chain before writing the /infinite loop spec.
**Key questions:**
- Q1: Is role file update coordination a real risk (shared slugs → multiple role files)?
- Q2: Is /infinite the right primitive, or should we build a sequential queue worker?

**Decision predicate (set before walkthroughs):**
- If CEO gate is a serializing bottleneck in Walkthrough 1, Walkthroughs 2+3 confirm nothing additional about Q2. Skip to spec decision after W1 in that case.
- **Short-circuit rule:** Always run ALL three marketplaces before making a selection. A strong result from the first or second marketplace is NOT grounds to skip the others. Collect all desirable candidates across all three, then compare and select. Short-circuit (skip Steps 2-5) only if the best candidate, after reviewing all marketplaces, meets ALL of: 1K+ installs, trusted source, **flat knowledge-reference form factor** (not a navigation hub, workflow script, or project-specific skill), AND covers the full knowledge domain. Step 6 (role file update) is always required.

**Stub format:** flat `~/.claude/skills/<slug>.md` — matches existing 10 stubs; dir-based form reserved for invocable skills.

**Marketplace invocations (canonical — confirmed working):**
1. **skills.sh** — `Skill("find-skills", args="<keyword>")` slash command; underlying Bash `skills find <keyword>` (Volta binary). `npx skills` only supports `add`.
2. **agentskill.sh** — plugin only; `Skill("learn:learn", args="<keyword>")` loads skill context, then WebFetch `https://agentskill.sh/api/agent/search?q=<keyword>&limit=5` for results. No standalone search CLI.
3. **skillsmp** — WebFetch `https://skillsmp.com/api/v1/skills/search?q=<keyword>&sortBy=stars` (no auth needed). `/ai-search` requires key but WebFetch cannot pass auth headers.

---

## Walkthrough 1: wcag-2.1

**Category:** Standards-backed
**Source:** context7 `/websites/w3_wai_wcag22` (WCAG 2.2, 4355 snippets, High reputation)
**Referencing roles:** quality-assurance/accessibility-tester
**Skill file:** `~/.claude/skills/wcag-2.1.md`
**Status:** COMPLETE

### Step 1: Marketplace Check
- `Skill("find-skills", args="wcag")` → no results; `Skill("find-skills", args="accessibility")` → no results
- context7 `/alexsnchz/skills` "WCAG Design" found (Medium rep, WCAG 2.2, design-focused) — **no short-circuit**: wrong version, wrong focus (design vs. testing/audit)
- No community skill covers the QA audit knowledge domain at required depth. Proceeded.

### Step 2: Fetch Source Material
- WebFetch not in allowlist at time of run — docs-scraper path also blocked
- Used context7 `resolve-library-id` + `query-docs` — effective workaround for standards docs
- WCAG 2.1 entry (12 snippets) vs WCAG 2.2 (4355 snippets) — used 2.2 as richer source
- **Decision:** WCAG 2.2 context7 source for 2.1-titled skill (2.2 is backward compatible, richer)

### Step 3: Draft Skill File
- 172 lines — POUR, conformance levels, SC tables (A+AA), testing workflow, ARIA patterns, common failures, checklist
- Skills dir has no git repo — pre-CEO state not commit-tracked

### Step 4: CEO Review
- Board: Sonnet 4.6 (primary), Gemini 2.5 Flash (supplementary), GPT-4o (sanity only)
- Sonnet caught 7 technical **errors**: 4.1.1 framing, 1.4.12 missing property, 1.4.10 wrong test method, 1.4.3 missing px equivalents, aria-modal unreliability, tab pattern wrong keyboard model, Section 508 legal framing wrong
- Gemini caught 6 missing SCs (2.2.1, 2.2.2, 2.4.5, 2.4.8, 3.2.3, 3.2.4) + design review phase + Windows High Contrast + prefers-reduced-motion
- GPT-4o generic (low actionability — sanity check only)

### Step 5: Apply Feedback, Finalize
- 172 → 242 lines after all corrections
- 7 errors fixed; 6 missing SCs added; WCAG 2.2 note; JAWS, WHCM, prefers-reduced-motion, SPA testing, design review phase added
- `~/.claude/skills/wcag-2.1.md` finalized

### Step 6: Update Role Files
- `~/.claude/roles/quality-assurance/accessibility-tester.md` — Required Skills table updated: `wcag-2.1.md` marked ✅ Available, status column added
- Commit: `cd1a115` in roles repo

### Observations
- **Friction points:**
  1. Marketplace invocation was not yet established — correct method is slash commands (`find-skills`, `learn:learn`), WebFetch for skillsmp. No Bash, no just recipe for skillsmp.
  2. WebFetch not in allowlist — docs-scraper also blocked; context7 was effective workaround for standards bodies
  3. Skills dir has no git repo — CEO diff not trackable via commits; line-count comparison (172→242) is the workaround
- **Decisions not obvious:**
  1. Use WCAG 2.2 context7 source for 2.1-titled skill — correct but not stated in workflow spec
  2. Flat `.md` vs dir-based skill — flat is correct for knowledge stubs, rule not stated in spec
- **CEO review signal:** Highest-value step. Caught 7 factual errors — not gaps, but wrong content that would cause false-pass audits. Would not have caught without CEO review. **Signal: HIGH.**
- **Time:** ~45 minutes total
- **Parallel-safe?** Steps 1-2 can parallel across slugs. Steps 3-5 serial per slug. CEO creates natural serialization point (one review per slug). Role file updates risk conflict if two slugs share a role file.

---

## Walkthrough 2: playwright-patterns

**Category:** Technology-specific
**Source:** Playwright official docs (context7 `/microsoft/playwright.dev`, 8119 snippets, High reputation)
**Referencing roles:** quality-assurance/qa-automation-engineer
**Skill file:** `~/.claude/skills/playwright-patterns.md`
**Status:** COMPLETE (clean pass — 2026-04-18)

### Step 1: Marketplace Check

**skills.sh** (`skills find playwright`):

| Skill | Installs | Author |
|-------|----------|--------|
| `playwright-best-practices` | 28.5K | currents-dev |
| `playwright-cli` | 22K | microsoft |
| `playwright-generate-test` | 10.5K | github/awesome-copilot |
| `playwright-explore-website` | 9.8K | github/awesome-copilot |
| `playwright-automation-fill-in-form` | 9.3K | github/awesome-copilot |
| `playwright-skill` | 3K | sickn33 |

**agentskill.sh** (WebFetch `https://agentskill.sh/api/agent/search?q=playwright&limit=5`):

| Skill | Installs | Security | Owner |
|-------|----------|----------|-------|
| playwright | 0 | 100 | majiayu000 |
| playwright | 0 | 92 | plurigrid |
| playwright | 0 | 85 | openai |
| playwright | 0 | 85 | yeohj0710 |
| playwright | 0 | 83 | a5c-ai |

**skillsmp** (WebFetch `/api/v1/skills/search?q=playwright&sortBy=stars`): 19 results. Top candidates by description alignment:

| Skill | Author | Stars |
|-------|--------|-------|
| `playwright-best-practices` | currents-dev | ~86K (repo stars) |
| `playwright-test` | PostHog | 32.5K |
| `playwright-e2e-builder` | davila7 | 24.5K |
| `playwright-pro` | alirezarezvani | 11K |
| `playwright` | prowler-cloud | 13.5K |

**SKILL.md evaluation of top candidates:**
- `currents-dev/playwright-best-practices` — SKILL.md is a **navigation hub** (table-of-contents pointing to 50+ files across `core/`, `testing-patterns/`, `advanced/`, etc.). Not a flat knowledge reference. Multi-file form factor requires full install; cannot substitute a flat stub.
- `davila7/playwright-e2e-builder` — Interview-driven planning workflow. Uses old `globalSetup` auth pattern. Not a knowledge reference.
- `PostHog/playwright-test` — Project-specific (their pnpm commands, localhost:8010, repeat-each 10 stability pattern). Not a general reference.
- `prowler-cloud/playwright` — MCP-driven exploration workflow. Not a knowledge reference.
- All agentskill.sh candidates — 0 installs; `a5c-ai` API returns 404.

**Short-circuit decision: NO.** No candidate is a flat knowledge reference covering the full QA automation engineer domain. Community skills are navigation hubs, workflow scripts, or project-specific. Proceeding with custom skill.

### Step 2: Fetch Source Material
- context7 `/microsoft/playwright.dev` (8119 snippets, High, Benchmark 87.44)
- Queries: POM + fixtures, assertions + locators + parallel workers, auth + isolation + global setup
- Key patterns: POM class, `test.extend()` fixtures, `expect()` auto-retry, workers config, `beforeEach` isolation, `storageState` auth, setup project + dependencies

### Step 3: Draft Skill File
- context7 `/microsoft/playwright.dev` (8119 snippets) — 3 targeted queries
- 391 lines — Core Principles, Locator Strategy (4 tiers), POM, Fixtures (try/finally), Assertions, Auth (setup project + dependencies), Network Mocking (page.route), CI Config, Accessibility (axe-core), Iframes & Shadow DOM, Anti-Patterns (16 rows), Deployment Checklist (18 items)
- `workers: process.env.CI ? 1 : undefined` — confirmed correct per official Playwright docs (sequential CI for stability)

### Step 4: CEO Review
- Board: Sonnet 4.6 (primary), Gemini 2.5 Flash (supplementary), GPT-4o (sanity only)
- **Run 1:** `mcp__just-prompt__ceo_and_board` → CEO file truncated at 169 lines (mid-heading "**P2 —"). **FAILURE 1 — reset.**
- **Run 2:** Re-run → CEO file truncated at 177 lines (mid-item "13. Append claude's checklist additions (T"). **FAILURE 2 → DEFERRED per protocol.**
- **Root cause:** `just-prompt` file-write limit ~170-335 lines. Affects both CEO synthesis AND board response files. Model output is complete; the write is cut off.
- **P4 recovery:** Board response files persisted in `/tmp/`. Claude-sonnet-4-6 board response (`/tmp/playwright-patterns-ceo-review_anthropic_claude-sonnet-4-6.md`) contained the full checklist additions. P4 recovered; W2 unblocked.
- Full action plan captured: P1 (3 runtime-breaking bugs), P2 (5 structural additions), P3 (4 new sections), P4 (5 checklist items)
- **P1 bugs identified:** (1) `>>` shadow DOM combinator — removed in Playwright v1.27; (2) `route.fulfill({ response, json })` — silent data loss, json prop ignored; (3) workers/fullyParallel contradiction (CEO says P1 but official docs support workers: 1 — kept as-is per user-confirmed official docs)
- See: `audits/roles/skill-w2-deferral-investigation.md` for full investigation notes

### Step 5: Apply Feedback, Finalize
- **P1 fixed:** `>>` combinator removed; shadow DOM section corrected to plain CSS + getByRole. `route.fulfill` pattern corrected with explicit `body: JSON.stringify(json)` + `contentType`.
- **P2 added:** Test Organization section (test.step, test.describe), beforeAll vs beforeEach tradeoff, page.unroute() + context-vs-page scoping, expect.soft semantics, waitForURL vs toHaveURL distinction, XPath blanket prohibition softened to "use only when semantic locators fail; document why"
- **P3 added:** Visual Regression Testing, API Testing (request fixture), File Upload & Download, Dialogs & Popups — 4 new sections
- **P4 added:** 5 deployment checklist items (testDir, project-level timeouts, no page.evaluate(), single fixture entry point, VRT update workflow)
- Final: 610 lines at `~/.claude/skills/playwright-patterns.md` (17 sections)

### Step 6: Update Role Files
- `~/.claude/roles/quality-assurance/qa-automation-engineer.md` — Status column added to Task-Specific Skills table; `playwright-patterns.md` marked ✅ Available
- Commit: `7ca7aa8` in roles repo (carried from trial run — role file state correct)

### Observations
- **Friction points:**
  1. **just-prompt file-write truncation** — `ceo_and_board` consistently truncates output files at ~170-335 lines. Affects CEO synthesis AND board response files. Recovery path: read board response files in `/tmp/` directly (they persist). For the infinite spec: split reviews into two passes (preamble included in both passes — DO NOT remove context to save space; the board needs role/question context to produce meaningful review).
  2. **P4 recovery via board files** — `/tmp/` board responses are NOT cleaned up between just-prompt calls. If CEO synthesis is truncated, the full model output is recoverable from individual board files. This is a reliable fallback.
  3. **workers: 1 vs. '50%'** — CEO flagged this as P1, but official Playwright docs recommend workers: 1 in CI. User confirmed official docs take precedence. In the infinite spec, CEO recommendations on config that contradict official docs must be adjudicated by the human reviewer, not auto-applied.
- **Decisions not obvious:**
  1. Form factor (flat stub vs. navigation hub) must be an explicit evaluation criterion at Step 1
  2. Board files in /tmp/ persist across just-prompt calls — reliable recovery path for truncated CEO synthesis
  3. The just-prompt truncation is a spec constraint: it caps the review depth per call; architecture must plan around it
- **CEO review signal:** HIGH — caught 3 runtime-breaking bugs (>> combinator removed in v1.27, route.fulfill silent data loss, config contradiction). P3 coverage additions (VRT, request fixture, file upload, dialogs) were all valid and complete the skill.
- **Time (clean pass):** ~60 min including deferral investigation and P4 recovery
- **Parallel-safe?** Yes — Steps 1-2 parallelizable. Step 4 CEO review is the serializing bottleneck AND has the truncation risk. Role file is slug-specific (no conflict for this slug).

---

## Walkthrough 3: stakeholder-management

**Category:** General-professional
**Source:** PMI PMBOK Stakeholder Management Knowledge Area + Power-Interest Grid + UAT sign-off practices (3x WebSearch)
**Referencing roles:** quality-assurance/uat-coordinator
**Skill file:** `~/.claude/skills/stakeholder-management.md`
**Status:** COMPLETE (2026-04-18)

### Step 1: Marketplace Check

**skills.sh** (`skills find stakeholder` + `stakeholder-management`): 10 results. Top: `refoundai/stakeholder-alignment` (947 installs), `anthropics/stakeholder-update` (672 installs). No candidate cleared 1K+.

**agentskill.sh**: 20 results across both queries. All 0 installs. No candidates.

**skillsmp**: Top by stars — `kortix-ai/stakeholder-comms` (19,606), `anthropics/stakeholder-update` (11,199), `phuryn/stakeholder-map` (9,944). All single-technique tools (comms, updates, mapping) — narrow scope, not full domain.

**Short-circuit decision: NO.** No candidate meets all four criteria. Best option (kortix-ai) is PM-comms focused, unknown form factor, untrusted source. All others are too narrow or below install threshold.

### Step 2: Fetch Source Material
- Context7 checked: no PMBOK entry. `/mdresch/adpa` (document generator) not usable.
- WebSearch (3 targeted queries):
  1. PMI PMBOK stakeholder management processes (Identify, Plan, Manage, Monitor)
  2. Power-Interest Grid / Mendelow's Matrix / engagement matrix / communication planning
  3. UAT sign-off, acceptance criteria, defect triage, go/no-go practices
- Note: Skill cannot be drafted from agent training knowledge alone — authoritative outside source required.

### Step 3: Draft Skill File
- 276 lines — 13 sections: Core Principles, Stakeholder Identification (register + types), Power-Interest Grid, Engagement Assessment Matrix, Communication Plan (structure + cadences), Audience-Specific Communication (5 audiences), UAT Stakeholder Governance (entry/exit/triage/go-no-go), Managing Expectations, Escalation Framework, Influence Without Authority, Anti-Patterns (10 rows), Engagement Checklist (3 phases)

### Step 4: CEO Review
- Board: Sonnet 4.6 (primary), Gemini 2.5 Flash (supplementary), GPT-4o (sanity only)
- CEO: Opus 4.7 — **clean run, no truncation** (174 lines)
- **Scores adopted:** D2=4, D3=4, D4=5, D5=3, D8=4, D10=3
- **Sonnet caught 4 must-fix items:** recommendation/options contradiction (Executive Sponsors vs. Escalation Framing), entry criteria missing blocking language, critical defect communication sequencing problem, C→D notation inconsistency
- **Sonnet caught 7 should-fix items:** ambiguous acceptance criteria gap, conflict resolution missing, sign-off sequencing/proxy authority, pre-kickoff checklist phase, Conditional Go management, premature go/no-go anti-pattern, vendor/third-party stakeholder type
- **Gemini:** High false-positive rate (D5=5, D10=5); useful additions: failing-to-close-feedback-loop anti-pattern, taking-sides-in-conflicts anti-pattern, vendor stakeholder (corroborated sonnet)
- **GPT-4o:** Thinnest review; validated Conditional Go follow-through importance; rejected case-study suggestion (conflicts with D3)
- CEO sided with Sonnet on all score disputes; gemini/gpt-4o gave inflated scores that would let a defective file ship

### Step 5: Apply Feedback, Finalize
- All 4 must-fix + 7 should-fix items applied
- Added: vendor/third-party stakeholder type, Stakeholder Conflict Resolution section, Conditional Go management scaffolding, pre-kickoff checklist phase, 4 new anti-pattern rows, entry criteria blocking language, sign-off sequencing, C→D notation fix
- Final: 317 lines at `~/.claude/skills/stakeholder-management.md`

### Step 6: Update Role Files
- `~/.claude/roles/quality-assurance/uat-coordinator.md` — Status column added to Required Skills table; `stakeholder-management.md` marked ✅ Available
- Commit: roles repo (2026-04-18)

### Observations
- **Friction points:**
  1. **WebSearch blocked initially** — added permission mid-walkthrough. For the infinite spec: WebSearch must be in the allowlist for general-professional skills where context7 has no coverage.
  2. **Context7 gap for non-technical domains** — PMBOK, HR frameworks, business methodologies are not in context7. WebSearch is the correct fallback for general-professional skills.
  3. **CEO review scoring model added mid-run** — including D2/D3/D4/D5/D8/D10 rubric in the prompt produced structured, comparable scores across board members. CEO used the score dimension framework to adjudicate inflated Gemini/GPT-4o scores. High value addition.
  4. **No truncation this time** — 174-line CEO synthesis fit within the file-write limit. The skill file + scoring rubric + preamble was a longer prompt than W2, but the review output was more focused (fewer sections, no code blocks). Output length is driven by response verbosity, not prompt length.
- **Decisions not obvious:**
  1. Agent training knowledge is not a valid source — must have external source even for well-understood domains
  2. Scoring rubric in the CEO prompt is a real quality improvement — board members scored with evidence; CEO could adjudicate score inflation directly
  3. Gemini's inflation pattern is systematic — it gave 5s on five of six dimensions for a file with known defects. For the infinite spec: CEO must always adjudicate Gemini scores critically
- **CEO review signal:** HIGH — caught a direct verbatim contradiction (recommendation vs. options) that would cause an agent to either suppress alternatives from sponsors or present menus to executives depending on which section it read most recently. Also caught the critical defect sequencing problem (communicate existence immediately, triage outcome after 24h — these are different actions).
- **Time:** ~45 minutes including WebSearch permission acquisition
- **Parallel-safe?** Yes — Steps 1-2 parallelizable. CEO review clean (no truncation). Role file is slug-specific (no conflict risk).

---

## Walkthrough 4: solutions-architect

**Category:** General-professional (SA methodology)
**Source:** AWS Well-Architected Framework (context7), C4 model (context7), SA role + ADRs + NFRs + integration patterns (WebSearch)
**Referencing roles:** engineering/solutions-architect
**Skill file:** `~/.claude/skills/solutions-architect.md` + `solutions-architect/` (3 reference files)
**Status:** COMPLETE — two-round CEO review (2026-04-18)

### Step 1: Marketplace Check

**skills.sh** (`skills find solutions-architect` + `architecture`): No candidates meeting criteria. Closest: scattered workflow-planning skills, none covering the SA knowledge domain (C4, ADR authoring, NFR elicitation, Well-Architected review).

**agentskill.sh**: No usable results — 0-install or mismatched scope.

**skillsmp**: Architecture-adjacent results all scoped to single frameworks or narrow patterns. None covering the full SA role domain.

**Short-circuit decision: NO.** No candidate is a flat knowledge reference covering the full SA domain. Proceeding with custom skill.

### Step 2: Fetch Source Material
- context7 `/aws/aws-cdk-guide` + `/simon-brown/c4-model` for C4 and Well-Architected
- WebSearch (3 targeted queries): SA role + NFR elicitation, ADR format + governance, integration patterns + decision frameworks
- Key sources: C4 model levels, AWS Well-Architected 6 pillars, IASA SA body of knowledge for ADR and NFR patterns

### Step 3: Draft Skill File
- 243 lines — 11 sections: Core Principles, Technical Discovery (process + 8-category questions), NFRs, C4 Model (4 levels + rules), Well-Architected (6 pillars table), Architecture Styles (6), Integration Patterns (6 + checklist), Trade-off Analysis, ADRs, Anti-Patterns (10 rows), Architecture Review Checklist (3 phases)
- Single flat file — no references/ directory

### Step 4: CEO Review (Round 1)
- Board: Sonnet 4.6 (primary), Gemini 2.5 Flash (supplementary), GPT-4o (sanity)
- CEO: Opus 4.7
- **Scores (CEO-adjusted):** D2:3, D3:3, D4:4, D5:3, D8:2, D10:3, Overall:3
- **Average: 3.0/5 — below 3.5 threshold → mandatory second round**
- **Sonnet P1 findings:** description missing trigger keywords (ADR/C4/NFR), no references/ extraction, no migration patterns
- **Sonnet P2 findings:** no build-vs-buy framework, no threat modeling process, under-specified trade-off scoring (weights/tiebreaker/ADR-output missing), empty answer table
- **Gemini inflation:** D3=5, D4=5, D5=5 — contradicted by real defects in file. CEO rejected all three.
- **gpt-4o:** Failed to produce Overall score; D2=5 despite missing trigger keywords — direct miss on prompt requirement.

### Step 5: Apply Feedback (Round 1 → Round 2)
- **P1:** Rewritten description with trigger keywords + loads-when/does-not-load framing; extracted 3 reference files (`solutions-architect/adr-template.md`, `solutions-architect/discovery-questions.md`, `solutions-architect/anti-patterns.md`); added Migration Patterns section (Strangler Fig, Big Bang, Parallel-Run)
- **P2:** Added Build vs. Buy decision framework, Threat Modeling (STRIDE-aligned 5-step process), rewrote Trade-off Analysis (weights before scoring, tiebreaker rule, ADR-as-output), removed empty answer table, added Architectural Fitness Functions section
- **P3:** Added TOC (15 sections), trimmed Well-Architected to implications-only table, condensed Anti-Patterns to summary + reference signal
- **Post-fix structure:** main file 314 lines + 3 reference files (adr-template 70, discovery-questions 26, anti-patterns 21)

### Step 4 (Round 2): CEO Review
- Same board and CEO
- **Scores (CEO-adopted, board average):** D2:5, D3:4.67, D4:5, D5:4.67, D8:5, D10:5, Overall:5
- **Average: 4.91/5 — above threshold, no third round required**
- **Two P3 polish edits identified by Sonnet:** (1) Remove NFR/fitness-function rule duplication; (2) Anchor Strangler Fig seam with example seam types (API gateway, BFF, event bus)
- Both edits applied. Status: PRODUCTION-READY.

### Step 6: Update Role Files
- `~/.claude/roles/engineering/solutions-architect.md` — Status column added to Required Skills table; `solutions-architect.md` marked ✅ Available
- Commit: roles repo (2026-04-18)

### Observations
- **Two-round review:** First time the scoring gate triggered a mandatory second round. Average 3.0 → 4.91 after full P1/P2/P3 application. The gate works: the first-round file was structurally sound but materially incomplete (missing migration, build-vs-buy, threat modeling, fitness functions).
- **Reference file extraction:** First walkthrough to use a `references/` directory structure. The extraction pattern for independently-loadable artifacts (ADR template, discovery questions, anti-patterns) reduces context window overhead and improves D8. Discovery and anti-patterns are loaded conditionally; ADR template loaded only when authoring ADRs.
- **Second-round prompt design:** Include Round 1 average score, list all applied fixes, ask board to verify fixes resolved gaps and flag regressions. Same scoring matrix as Round 1. No new review questions needed — the review is a verification pass, not an open-ended review.
- **Gemini D3/D4/D5 inflation** (same pattern as W3): Gemini awarded 5/5 on D3 for a file with an empty answer table and restated public AWS documentation. CEO correctly rejected all three inflated Gemini scores in Round 1.
- **CEO novel dimensions:** Round 1 introduced "evidence density" (ratio of cited defects to general claims) and "prompt fidelity" (did reviewer address every prompt requirement?) as decision factors. These cut through the board-level tie and identified Sonnet as the reliable review signal. Round 2 introduced "signal quality" and "executability."
- **Time:** ~90 minutes including both CEO review rounds
- **Parallel-safe?** Yes (role file slug-specific, no conflict risk). Two-round review does NOT need to serialize with other skills — it can run independently.

---

## Cross-Walkthrough Summary (W1–W4 complete)

### Q1: Role file update coordination risk
- **Shared slugs found:** None in W1–W4 (each skill maps to exactly one role). Risk is real but untriggered so far.
- **Risk in practice:** Low for single-role skills. Becomes real when a skill like `defect-management.md` references qa-automation-engineer, qa-lead, uat-coordinator, and head-of-qa simultaneously — a wave of parallel writes would conflict on the same file
- **Recommended commit batching:** Per-slug commits are safe. For shared-slug skills, serialize role file updates or use a single commit per slug that touches all affected role files at once

### Q2: /infinite vs queue worker
- **CEO gate:** Serializing within each skill (Steps 3-5 require sequential output/input), but skills themselves are independent and can run in parallel waves
- **Parallelism savings:** Steps 1-2 (marketplace + source fetch) can run in parallel across all skills. Steps 3-5 run per-skill. Step 6 (role file commit) must serialize on shared-slug files
- **Truncation constraint:** just-prompt file-write limit means CEO synthesis caps at ~170 lines; board files recoverable. Split reviews if needed — always with preamble.
- **Two-round gate:** Skills scoring ≤3.5 average require a second CEO review round after P1+P2+P3 fixes are applied. The gate caught a genuinely incomplete file (solutions-architect R1). Spec must plan for the two-round case — it adds ~45 min and one more CEO call per affected skill.
- **WebSearch dependency:** General-professional skills (no context7 coverage) require WebSearch. Must be in allowlist before the infinite run starts.
- **Scoring rubric:** Include D2/D3/D4/D5/D8/D10 + Overall Score in every CEO review prompt — adds structure and enables score adjudication. Gemini systematically inflates scores (observed in W3 and W4); CEO must adjudicate.
- **Recommendation:** Queue worker with wave-based parallelism for Steps 1-2, sequential per-skill for Steps 3-5, serialized commit batching for Step 6. /infinite is the closer fit but needs truncation-aware CEO review logic, WebSearch pre-authorization, and two-round gate logic built in.

### Spec inputs (feed into /infinite spec)
- **Source routing rules:**
  - Standards bodies (WCAG, PMBOK, HIPAA) → WebSearch
  - Technical frameworks (Playwright, AWS, React) → context7
  - SA methodology, HR, business domains → WebSearch
  - context7 coverage check first; WebSearch if no entry found
- **Reference file trigger:** Extract to `<slug>/` subdirectory when any section is independently loadable (task A loads section X but not Y; task B loads Y but not X). ADR templates, discovery checklists, anti-patterns tables are canonical extract candidates.
- **Scoring gate:** ≤3.5 average → implement all action plan items → same scoring matrix round 2. Above 3.5 → apply minor fixes → deploy.
- **CEO novel dimensions:** evidence density + prompt fidelity (R1); signal quality + executability (R2). Track these as CEO evaluation quality signals — they identify which board member is the reliable reviewer for each dimension.
- **Gemini inflation rule:** Gemini is reliable for gap identification (D10) and completeness checklists; unreliable for D3/D4/D5 scoring. CEO must override Gemini D3/D4/D5 scores when they conflict with Sonnet's evidence-backed scores.
- **Execution primitives needed:** marketplace search (3 parallel), source fetch (context7 + WebSearch), draft (sequential), CEO review (file prompt → just-prompt → read board files for recovery), apply fixes, role file update (serialized per shared slug)
