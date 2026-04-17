```json
{
  "role": "qa-lead",
  "department": "quality-assurance",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 9
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All six principles are generic QA management platitudes that could appear in any QA lead job description. 'Risk-Based Testing: Test what matters most first' and 'Fast Feedback: Developers need to know about issues quickly' add no role-specific guidance. None of the principles reflect the Story Portal context (festival deadline, tiny team, PWA constraints), the Hybrid classification (where AI drafts and human decides), or the specific tension this role lives in — being the tactical executor under a Head of QA while interfacing with developers who own fixes.",
      "example_rewrite": "Replace at least three principles with role-specific ones. Examples: | **Triage Before Execution** | An untriaged bug backlog collapses team clarity faster than a missed test case — sort first, test second | | **Delegate Ruthlessly, Own the Status** | You coordinate testers and own the reported outcome; doing the testing yourself is a failure mode, not a backup plan | | **Festival Date Is Fixed, Scope Is Not** | When time is immovable, quality gates must flex scope — document every deferral explicitly so the Release Manager owns the tradeoff, not QA |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "Inbound handoffs name artifacts loosely ('Quality strategy, priorities' from Head of QA; 'Features, requirements' from Product Manager) without specifying document format, naming convention, or what triggers the handoff. Outbound handoffs are slightly better but still vague — 'Quality status, recommendations' to Release Manager doesn't say whether that is a written report, a dashboard link, a checklist, or a verbal standup update. The Workflows reference 'STOP → Present to Release Manager' without naming what artifact is being presented. This means an AI agent coordinating this handoff has no basis for choosing a format.",
      "example_rewrite": "Tighten both tables. Example outbound row: | **Release Manager** | Signed Release Readiness Report (QA-RR-{sprint}.md) containing: go/no-go recommendation, open defect count by severity, quality gate checklist with pass/fail per gate, and list of accepted risks with owner sign-off | Triggered when: release candidate passes regression and QA Lead has verified all P0/P1 bugs are resolved or formally deferred |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "The six anti-patterns are above average — 'Test everything yourself' and 'Overload individual testers' are genuinely role-specific failure modes for a coordinating lead, not a generic QA practitioner. However, two entries ('Ignore metrics' and 'Skip defect triage') are generic enough to appear in any QA role. None of the anti-patterns address the Hybrid classification risks — specifically, the failure mode of an AI agent over-drafting and a human rubber-stamping without real review, or the inverse: human over-riding AI analysis on every metric without justification.",
      "example_rewrite": "Add one Hybrid-specific anti-pattern: | **Rubber-Stamp AI Drafts** | AI generates test plans and triage reports quickly; approving them without human review of priority calls creates false confidence in coverage | Before signing off on any AI-drafted test plan, manually verify that the top 3 risk-ranked items match your own read of the sprint scope |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Iteration Protocol is present and correctly structured for a Hybrid role. The AI/Human split in the Deployment Notes is explicit and actionable. The three workflows include STOP points. The role would load cleanly. Minor gap: the skill files listed in Context Requirements are flagged as 'planned development' and do not exist yet, so an AI agent loading this role has no skill files to actually pull. The note acknowledges this but leaves the agent with nothing to fall back on — no inline summary, no placeholder behavior described.",
      "example_rewrite": "Until skill files exist, add a fallback instruction block: 'If skill files are unavailable, apply the following inline defaults — Test Planning: prioritize by: (1) user-facing critical path, (2) legal/compliance requirements, (3) platform requirements, (4) performance, (5) edge cases. Defect Triage: use severity matrix — P0: system unusable; P1: core flow broken; P2: feature degraded; P3: cosmetic or edge case.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 9,
      "finding": "The Story Portal appendix is the strongest section in the file. Quality gates are concrete (60fps, PWA offline, zero P0/P1), testing priorities map directly to named features with named risk levels, and the small-team/festival-deadline constraints are explicitly called out with tactical responses. The only gap: the 'Current State' table shows all areas as 'Informal' or 'Ad-hoc' but provides no instruction for how the QA Lead should sequence standing these up. A QA Lead loading this role at sprint one has no ordered bootstrap path from the current chaotic state to the defined quality gates.",
      "example_rewrite": "Add a Bootstrap Sequence table: | Week | Action | Output | | 1 | Define Quality Gates with Head of QA and Release Manager | Signed QA-GATES-MVP.md | | 1 | Create triage labels in issue tracker (P0–P3) | Label config committed | | 2 | Publish Sprint 1 Test Plan covering Wheel + Audio + Consent | QA-PLAN-S1.md | | 3 | First Release Readiness Report against defined gates | QA-RR-S1.md |"
    }
  ],
  "top_improvement": "Philosophy Depth: all six principles are generic platitudes that provide no differentiated guidance for the Hybrid classification, the festival deadline, or the specific executor-under-strategist tension this role operates in. Rewriting three principles to be role-and-context-specific would cascade value into every section that references the philosophy — especially the anti-patterns and deployment notes."
}
```