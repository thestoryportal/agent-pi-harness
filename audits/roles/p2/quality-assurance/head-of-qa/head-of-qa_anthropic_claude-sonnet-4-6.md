```json
{
  "role": "head-of-qa",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 8,
    "handoff_specificity": 7,
    "anti_pattern_quality": 8,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 8,
      "finding": "All 6 principles are role-specific and paired with concrete meaning. 'Shift Left, Gate Right' and 'Automation Enables, Humans Explore' are genuinely QA-specific framings, not generic quality slogans. Minor deduction: 'Quality Is Everyone's Job, QA Is the Safety Net' is a well-worn industry phrase that stops short of explaining HOW this Head of QA operationalizes that belief — e.g., does it mean embedded QA reviews in Engineering standups, or co-authored acceptance criteria with Product? The principle is stated but not differentiated.",
      "example_rewrite": "Replace 'Quality Is Everyone\'s Job, QA Is the Safety Net' with: 'Embedded Partnership, Not Separate Gatekeeping — QA attends Engineering sprint planning and Design handoffs to influence quality upstream; the release gate is a last resort, not the primary intervention point.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 7,
      "finding": "Most handoffs name real artifact types (release candidates, defect reports, quality sign-off). However, two weaknesses exist. First, 'Receives From: Solutions Architect — Architecture context, integration points' is vague; no named artifact is specified and Solutions Architect is a peer-level role whose charter relationship to QA is undefined in this file. Second, 'Delivers To: Executive Team — Quality dashboards, trend reports' does not specify cadence or format, making it hard for an AI agent to know what 'done' looks like for this handoff.",
      "example_rewrite": "Delivers To: Executive Team | Artifact: Weekly Quality Scorecard (quality-scorecard.md template) delivered every Monday before leadership sync, plus Release Quality Report (pass/conditional/fail + blocker summary) within 2 hours of each release gate decision."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 8,
      "finding": "Six anti-patterns are present and most are genuinely QA-specific. 'Rubber-stamp releases under pressure' directly addresses the independence mandate of this role. 'Ignore technical debt in tests — flaky, unmaintainable tests' is precise and craft-specific. Minor deduction: 'Operate in isolation from Engineering — Adversarial relationship' is a broad organizational behavior warning that appears in many department head roles verbatim. For this role, the failure mode is more specific: QA leads who file defects without context, refuse to triage severity jointly, or treat Engineering as the enemy rather than the co-owner of quality.",
      "example_rewrite": "Don't: File defects in isolation without Engineering context. Why: Creates adversarial dynamic and wastes triage cycles on misclassified severity. Instead: QA Lead attends Engineering standups weekly; critical defect reports include reproduction steps, severity rationale, and a proposed Engineering contact for triage — filed as a collaborative ticket, not an accusation."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The AI Assistance Model section is clean and the Human-Primary classification is correctly applied. The Skills to Load table is a strong operational signal. However, two gaps reduce clarity for an AI agent attempting to assist: (1) There is no iteration protocol defined — the template standard requires one for Hybrid deployment, and this role is classified Hybrid. An AI agent assisting on test strategy drafts has no guidance on how many revision loops are expected, what triggers escalation to the human Head of QA, or what a 'done' draft looks like. (2) The trigger conditions for skills are too broad — 'testing-validation.md triggers on test strategy planning' covers nearly all QA work, giving an AI no discrimination signal.",
      "example_rewrite": "Add Iteration Protocol section: 'AI Iteration Protocol (Hybrid): Draft cycle maximum 2 AI iterations before human review. AI flags for human review when: (a) release gate decision involves a conditional approval, (b) defect escape rate exceeds target by >2%, (c) stakeholder conflict on quality criteria arises. AI marks drafts with [DRAFT — PENDING HEAD OF QA REVIEW] until human signs off. Test strategy drafts require Head of QA approval before sharing with Engineering or Product.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "The Story Portal appendix is the strongest section in the file. Testing stack is specific (Vitest, React Testing Library, Playwright, GitHub Actions, Vercel Preview), quality targets are measurable (60fps, WCAG 2.1 AA, PWA >90), and priority tiers are rationalized ('Security LOW — minimal attack surface, frontend only'). The steampunk aesthetic validation note is a genuinely project-specific quality concern not found in generic QA templates. Minor deduction: The Key Coordination Points table references 'Performance Engineer' as a role, but the org chart and team structure show 'Performance Tester' as the direct report. This is a naming inconsistency that could cause role confusion in a multi-agent deployment.",
      "example_rewrite": "In Key Coordination Points, replace 'Performance Engineer' with 'Performance Tester' to match the team structure org chart. Additionally, add one row: Head of Creative Tech | Visual QA Acceptance Criteria | Steampunk aesthetic sign-off checklist (animation smoothness, material rendering, VFX consistency) — defined jointly before each release gate."
    }
  ],
  "top_improvement": "Add a Hybrid Iteration Protocol section specifying maximum AI draft cycles, explicit human review trigger conditions, and draft labeling conventions — the template standard requires this for Hybrid deployment and its absence is the only structural compliance gap in an otherwise strong role file."
}
```