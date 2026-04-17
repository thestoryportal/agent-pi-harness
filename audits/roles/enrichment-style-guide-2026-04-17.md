# Role Enrichment Style Guide - 2026-04-17

Durable style reference for enriching role template files at `~/.claude/roles/<dept>/<file>.md`. Every downstream enrichment agent must match this guide exactly - mismatched format, tone, or verb mood is a quality regression even when the content is correct.

Derived by comparing the three project-context subsections (`### Required Context`, `### Key Priorities`, `### Quality Bar`) across four sampled files:

- `~/.claude/roles/engineering/ai-ml-engineer.md`
- `~/.claude/roles/engineering/backend-developer.md`
- `~/.claude/roles/platform-engineering/site-reliability-engineer.md`
- `~/.claude/roles/quality-assurance/qa-lead.md`

All three subsections live inside the `## Appendix: Project Context` block (exact heading present in every sampled file). The parent block also opens with a `### Current State` table that is NOT subject to enrichment; enrichment only touches the three subsections listed below.

---

## Section: `### Required Context`

### Format

- Heading rendered exactly as `### Required Context` (one space after `###`, no trailing punctuation).
- A single-line intro paragraph does NOT appear; the heading is followed directly by the list.
- Bulleted list using the markdown checkbox syntax `- [ ] `.
- No nested bullets. Each item is one line.
- Six items is the typical length (4-7 observed). Do not pad past 7.

### Grammar

- Each item is a **noun phrase**, not a sentence or an imperative.
- No trailing period.
- Capitalize the first word.
- Prefer concrete artifacts over vague categories: `API conventions documentation` not `Conventions`.

### Sampled items (verbatim, unedited)

From engineering/ai-ml-engineer.md:
```
- [ ] Product requirements for AI features
- [ ] Approved AI services/models
- [ ] API keys and access credentials
- [ ] Performance and cost constraints
- [ ] Quality expectations and criteria
- [ ] Security and privacy requirements
```

From engineering/backend-developer.md:
```
- [ ] Database access
- [ ] Existing schema documentation
- [ ] API conventions documentation
- [ ] Security requirements
- [ ] Performance requirements
```

From platform-engineering/site-reliability-engineer.md:
```
- [ ] Production system architecture
- [ ] Deployment targets and environments
- [ ] Current monitoring setup (if any)
- [ ] Incident history and patterns
- [ ] Team on-call structure
- [ ] Stakeholder contact list
- [ ] Current SLOs (if defined)
```

From quality-assurance/qa-lead.md:
```
- [ ] Project scope and timeline
- [ ] Team composition
- [ ] Quality strategy
- [ ] Release schedule
- [ ] Tooling access
- [ ] Stakeholder list
```

### Authoring rules

- Name the access / artifact / constraint the role needs BEFORE it begins work.
- Mix infrastructure access (credentials, databases, repos), documentation (schema, conventions, runbooks), constraints (performance budgets, security requirements), and organizational context (team composition, stakeholder list, on-call rotation).
- Avoid marketing flourishes ("deep understanding of...", "comprehensive knowledge of...").
- If a prerequisite is conditional, suffix with `(if any)` or `(if defined)` rather than a long clause.

---

## Section: `### Key Priorities`

### Format

- Heading rendered exactly as `### Key Priorities`.
- Followed directly by a bulleted list with plain `- ` bullets (no checkbox).
- 5 bullets is the consistent pattern across all four samples. Keep to 4-6.
- No sub-bullets, no intro paragraph.

### Grammar

- Each bullet begins with an **imperative verb**: `Stand up`, `Establish`, `Define`, `Author`, `Partner`, `Instrument`, `Publish`, `Document`, `Build`, `Configure`, `Lead`, `Plan`, `Triage`.
- Each bullet describes a **first-release / setup** action, not a steady-state operation. The voice is "what we have to put in place for this project".
- One line per bullet; 15-25 words typical.
- No trailing period when the bullet is a sentence fragment (all sampled bullets are fragments starting with an imperative).

### Sampled bullets (verbatim, unedited)

From engineering/ai-ml-engineer.md:
```
- Establish a reliable Claude API integration with streaming, retries, and graceful fallbacks
- Author and version the first production prompts with structured outputs
- Instrument latency and cost monitoring before shipping any user-facing feature
- Build an output-evaluation harness so regressions surface before users see them
- Define privacy and consent rules for any user content sent to AI services
```

From engineering/backend-developer.md:
```
- Stand up migrations and seed workflow so schema changes are reversible from day one
- Publish API conventions (error shape, versioning, validation) before multiple endpoints exist
- Partner with Security Engineer on auth architecture and sensitive-data policy review
- Instrument query telemetry and slow-query alerts ahead of real production load
- Document the data model (ERD + access patterns) so downstream roles can self-serve
```

From platform-engineering/site-reliability-engineer.md:
```
- Stand up error tracking, uptime monitoring, and RUM on critical user journeys
- Define SLIs/SLOs and publish a reliability dashboard the team reviews regularly
- Configure alerting with actionable thresholds and a documented escalation tree
- Author runbooks for deploy, rollback, and the top expected incident classes
- Establish an on-call rotation with handoff discipline and incident postmortems
```

From quality-assurance/qa-lead.md:
```
- Stand up a lightweight test plan aligned to sprint scope and risk
- Establish daily defect triage with clear severity/priority rubric
- Define quality gates for the next release milestone
- Balance tester workload and unblock testers quickly
- Report quality status and risks to stakeholders on a regular cadence
```

### Authoring rules

- Lead with verbs that describe founding work: stand up, establish, publish, author, instrument, partner, define, configure, build, document.
- Each bullet should pair an action with a justification clause ("so..." / "before..." / "ahead of..." / "with..." / "aligned to..."). Roughly 3/5 bullets across samples use this construction.
- Reference specific tools, SLAs, or artifacts the role will produce (e.g., `ERD`, `RUM`, `runbooks`, `error tracking`, `escalation tree`, `quality gates`).
- Avoid abstract values ("foster a culture of quality") - every bullet must name something concrete that will be done or produced.

---

## Section: `### Quality Bar`

### Format

- Heading rendered exactly as `### Quality Bar`.
- Followed directly by a 2-column markdown table with the header row `| Gate | Criteria |`.
- Separator row uses `|------|----------|` (minimum 6 and 10 dashes respectively in samples).
- 5 rows is the standard (all four samples use exactly 5).
- No intro paragraph between heading and table.

### Column rules

- **Gate column**: wrapped in double asterisks for bold, title-case noun phrase, 1-3 words. Examples: `**Latency**`, `**API latency**`, `**SLO coverage**`, `**Triage SLA**`, `**Migration safety**`.
- **Criteria column**: one sentence fragment giving a **measurable or observable threshold**. No trailing period. Uses specific numbers, SLAs, or qualitative anchors ("rehearsed", "enforced on every table").

### Sampled rows (verbatim)

From engineering/ai-ml-engineer.md:
```
| Gate | Criteria |
|------|----------|
| **Latency** | <2s typical for interactive AI features; streaming UX for anything longer |
| **Reliability** | 99.5%+ success rate with graceful degradation on AI-service failure |
| **Output quality** | Regression suite passes on representative inputs before each release |
| **Cost** | Per-feature cost tracked; alerting on anomalies; monthly optimization review |
| **Privacy** | User data handling follows security guidelines; consent captured where required |
```

From engineering/backend-developer.md:
```
| Gate | Criteria |
|------|----------|
| **API latency** | p50 <100ms, p95 <500ms on common endpoints |
| **Query performance** | Common queries <50ms; complex <200ms via EXPLAIN ANALYZE |
| **Data protection** | Row-level policies enforced on every table holding user data |
| **Migration safety** | Every migration reversible and tested on a production-like dataset |
| **Input validation** | All API boundaries validate input; no raw database errors leak to clients |
```

From platform-engineering/site-reliability-engineer.md:
```
| Gate | Criteria |
|------|----------|
| **SLO coverage** | Critical services have SLIs, SLOs, and error budgets tracked |
| **Alert quality** | Pages are actionable; noise reduced; every alert has a runbook link |
| **Runbook currency** | Runbooks match production reality and are rehearsed |
| **Incident discipline** | Every incident gets a severity, timeline, and blameless postmortem |
| **Observability** | Logs, metrics, and traces provide end-to-end visibility on critical flows |
```

From quality-assurance/qa-lead.md:
```
| Gate | Criteria |
|------|----------|
| **Critical Paths Tested** | Core user journeys pass on target platforms |
| **No Open Blockers** | Zero P0/P1 defects unresolved at release |
| **Triage SLA** | New defects triaged within 24 hours |
| **Regression Clean** | Regression suite green on release candidate |
| **Status Visibility** | Current quality status documented and shared |
```

### Authoring rules

- Name five distinct gates; avoid redundant pairs (do not have both "Latency" and "Performance" rows).
- Each criterion must be **falsifiable** - a reviewer should be able to say "yes, met" or "no, not met" without interpretation.
- Prefer numeric thresholds when the role has them (latency SLAs, error budgets, p50/p95). For roles without numeric thresholds, use observable anchors ("rehearsed", "reversible and tested", "every X has a Y").
- Use semicolons to join two related conditions inside one criterion, not commas.

---

## Enrichment Rules

### Lift from JD content

- Specific tool names: `Prometheus`, `Grafana`, `PagerDuty`, `Jira`, `pgTAP`, `k6`, `Datadog`, `TestRail`, `Vercel Analytics`, `OpenTelemetry`.
- Frameworks and platforms the role actually configures (`Next.js`, `Supabase`, `GitHub Actions`).
- Measurable thresholds or SLAs: `99.9% uptime`, `<100ms p50`, `triage within 24 hours`.
- Concrete deliverable types: `test plans`, `runbooks`, `ERDs`, `architecture diagrams`, `postmortems`, `RLS policies`, `migration scripts`.
- Competency descriptors that can be rewritten as imperative setup actions.

### Exclude always

- Salary ranges, compensation bands, equity references.
- Interview questions, "day in the life" prose, hiring-guide framing.
- Marketing copy: "why this role matters", "demand for this role in 2026", "growth outlook", "earning potential".
- Org-chart or reporting-structure detail (the role template already has its own Collaboration section).
- Generic platitudes without a specific artifact, tool, or metric attached.
- Temporal filler: "In 2026", "looking ahead", "as organizations increasingly...".
- Any content that contradicts the role template's existing `What You Own` / `What You Don't Own` boundary tables.
- Acronyms without their expansion when the role template uses the expanded form.

---

## Style Rules (cross-section)

- **Voice.** First-person plural is implied but never surfaced ("we" is absent from all samples). Treat the role as an organizational seat; describe what the seat does, not how the occupant feels.
- **Tense.** `Required Context` is noun phrases (tense-free). `Key Priorities` is imperative mood. `Quality Bar` criteria are present-tense descriptions of the target state.
- **Specificity density.** Every bullet / row must cite at least one of: a concrete tool, a numeric threshold, a named artifact, or a named partner role. Bullets that could apply to any role fail review.
- **Length discipline.** `Required Context` items: 2-5 words. `Key Priorities` bullets: 15-25 words. `Quality Bar` criteria: 8-18 words. Do not blow past these without a reason tied to the role's actual scope.
- **No trailing periods** on bullet-list items or table cells. Full sentences only appear in intro paragraphs elsewhere in the file.
- **Formatting parity.** Reproduce the exact heading strings (`### Required Context`, `### Key Priorities`, `### Quality Bar`) verbatim. Do not reorder, rename, or merge sections.
- **Do not invent** `Current State` table content during enrichment - that subsection stays under the original author's control and is not in scope for JD-driven enrichment.

---

## Validation checklist (run before committing an enriched file)

- [ ] Headings match exact strings: `### Required Context`, `### Key Priorities`, `### Quality Bar`.
- [ ] `Required Context` uses `- [ ] ` checkboxes, noun phrases, no trailing periods.
- [ ] `Key Priorities` uses `- ` plain bullets, imperative verbs, one-line each, justification clause on most bullets.
- [ ] `Quality Bar` is a `| Gate | Criteria |` table with bolded gate names and 5 rows.
- [ ] Every bullet / row cites a concrete tool, threshold, artifact, or partner role.
- [ ] No salary, interview, marketing, or temporal-filler content was lifted from the JD.
- [ ] No bullet contradicts the role's existing `What You Own` / `What You Don't Own` tables.
- [ ] `Current State` table was not modified.

---

## Document Control

- **Generated:** 2026-04-17
- **Source samples:** 4 role files listed above (unmodified on disk)
- **Companion artifact:** `jd-enrichment-matches-2026-04-17.md` (match list driving which JD to lift from for each role)
