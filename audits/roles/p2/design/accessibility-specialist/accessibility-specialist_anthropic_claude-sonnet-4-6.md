```json
{
  "role": "accessibility-specialist",
  "department": "design",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 5,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and most are role-specific. 'Automated + Manual' and 'Standards Are Minimum' are genuinely distinctive to accessibility work. However, 'Accessibility Is Non-Negotiable' reads as a generic mantra rather than an operational principle — it tells the AI what to feel, not what to do. 'Specific Over Generic' is meta-advice that applies to any auditing role. The table format works well and avoids pure platitudes.",
      "example_rewrite": "Replace 'Accessibility Is Non-Negotiable' with: **'Block Before Launch'** — If a Critical or High severity barrier is unresolved, audit status is FAIL regardless of overall compliance score. A 95% passing audit with one screen-reader-blocking modal is a failing audit."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles correctly but artifacts are vague category labels, not actual deliverable formats. 'Designs for audit' does not specify whether that is a Figma share link, an exported PDF, or a prototype URL. 'Code remediation' does not specify whether that is a Jira ticket, a GitHub issue with code snippet, or a Confluence page. An AI agent cannot act on these descriptions because it does not know where to look or what format to produce.",
      "example_rewrite": "Receives From UX Designer: 'Figma share link to screen-level frames marked [READY FOR A11Y] in Figma status field, accompanied by user flow description in Confluence audit-request page.' Delivers To Frontend Developer: 'Jira ticket per issue containing: WCAG criterion violated (e.g., 1.4.3), severity label (Critical/High/Medium/Low), failing element selector, code snippet showing corrected implementation, axe rule ID for regression test registration.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no dedicated Anti-Patterns section in this role file at all. The DON'T list in Boundaries covers role-jurisdiction boundaries ('don't make design decisions') but these are not anti-patterns — they are scope limits. Anti-patterns should describe failure modes specific to accessibility auditing work itself: e.g., over-relying on automated tools, reporting issues without severity context, or treating WCAG pass as equivalent to usable. This is the most significant structural gap in the file.",
      "example_rewrite": "Add an Anti-Patterns section: | Anti-Pattern | Why It Fails | Correct Approach | |---|---|---| | **Automated-Only Auditing** | axe-core catches ~30% of WCAG failures; AI-generated clean report creates false confidence | Always follow automated scan with keyboard and screen reader walkthrough of primary user journeys | | **WCAG Pass = Accessible** | A form can pass all 78 AA criteria and still be unusable — correct labels on wrong fields, logical but confusing tab order | Flag usability-adjacent barriers even when technically compliant; tag as 'Best Practice' severity | | **Issue Dumping Without Triage** | Delivering 47 issues to a developer with no severity ranking causes paralysis; Critical blockers get buried | Every report must open with an Executive Summary listing Critical items only, before full issue list | | **Treating Steampunk Aesthetic as Constraint** | Deferring on contrast or focus visibility because 'the design team wants the brass color' lets aesthetic override compliance | Flag WCAG AA failures regardless of brand direction; escalate to Head of Design if unresolved, never self-suppress |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol loop is present and correctly placed for an AI-Primary Agent role. STOP points exist. The Agent Capabilities table is honest about what the AI can actually do. Two gaps reduce the score: (1) Workflow 1 and Workflow 2 have no explicit STOP points embedded in the flow steps — the iteration protocol sits separately and an agent reading only the workflow section would not know when to pause for human review. (2) 'Zero false positives' in Audit Quality standards is an impossible target that could cause an AI agent to suppress uncertain findings rather than flag them for human review.",
      "example_rewrite": "In Workflow 1, after step 3 COMPILE REPORT, add: '4a. STOP → Present merged findings to human reviewer before ticket creation. IF human confirms edge case interpretation → proceed. IF human overrides severity → update and rerun compliance score.' Also change Audit Quality standard from 'Zero false positives' to 'Flag uncertain findings with [NEEDS HUMAN REVIEW] tag rather than suppressing — false negatives are more costly than false positives in accessibility auditing.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "This is the strongest section in the file. The Story Portal appendix is genuinely specific: the Wheel, brass/copper color contrast, steampunk focus visibility, festival outdoor lighting, and motion reduction are all project-unique concerns that could not be copy-pasted into a generic role. The festival context table is particularly strong. Minor gap: the Testing Priorities table lists components but does not specify which WCAG success criteria map to each component test, which would make the table immediately actionable for audit execution.",
      "example_rewrite": "Enhance Testing Priorities: | Component | Test | WCAG Criterion | Pass Condition | |---|---|---|---| | Wheel | Keyboard spin | 2.1.1 Keyboard | All spin interactions operable via arrow keys without mouse | | Wheel | Focus visibility | 2.4.7 Focus Visible | Focus ring visible against brass/copper background at 3:1 minimum contrast | | Record button | Screen reader announcement | 4.1.3 Status Messages | Recording state change announced without focus move (e.g., 'Recording started') |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section. This is the only structural section missing from the file and it is the most operationally critical gap — without role-specific anti-patterns, an AI agent has no guardrails against the most common accessibility auditing failure modes (automated-only auditing, false WCAG-pass confidence, unseveritized issue dumps). A generic DON'T list covering jurisdiction boundaries does not substitute. See anti_pattern_quality example_rewrite for a complete draft section."
}
```