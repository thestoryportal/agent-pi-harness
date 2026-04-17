```json
{
  "role": "devops-research-lead",
  "department": "platform-engineering",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 5,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and role-specific — 'Reversibility Matters' and 'Total Cost of Ownership' are genuine differentiators for a research evaluator. However, 'Share Knowledge Freely' and 'Practice What You Preach' are thin: they name a value without explaining the operational implication for this role specifically. A research lead who hoards findings creates duplicate evaluation work across Platform teams — that specific consequence should be named.",
      "example_rewrite": "**Share Knowledge Freely** — Every evaluation report goes into the shared knowledge base within 5 business days of completion. If findings aren't shared, the next Platform role who needs similar data re-runs the same research. Undocumented POCs are wasted POCs."
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "The handoff tables list role names correctly, but the artifacts are almost entirely vague category labels ('Evaluation reports, recommendations', 'Research findings, POC documentation'). A receiving role cannot action these. What is the actual artifact? A named markdown file? A comparison matrix in a specific format? The templates exist in the appendix but are never referenced in the handoff tables. Additionally, 'All Platform roles' as a sender/receiver is too broad — it obscures which specific role triggers which specific artifact exchange.",
      "example_rewrite": "| Delivers To | Artifact | Format |\n|---|---|---|\n| Head of Platform | Tool Evaluation Report using `/templates/tool-evaluation.md` | Markdown in shared knowledge base + Slack summary |\n| CI/CD Engineer | POC Result Report with go/no-go recommendation and setup documentation | Markdown handed off at STOP point in Workflow 4, Step 4 |\n| All Platform roles | Technology Radar — quarterly update using `/templates/tech-radar.md` | Published to team wiki, presented in quarterly Platform sync |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Seven anti-patterns are listed, which is more than the standard 3-5, and most are genuinely role-specific. 'Recommend without testing' and 'Hoard research findings' are strong. However, two entries are weak: 'Research without priority' is generic project management advice applicable to any role, and 'Only evaluate new things' is the least obvious anti-pattern with the least explanation. The table format also obscures the severity — not all anti-patterns carry equal weight.",
      "example_rewrite": "| Don't | Why This Role Specifically | Instead |\n|---|---|---|\n| Only evaluate new tools when requested | Reactive-only research means the Platform team discovers tool obsolescence through production incidents, not research | Maintain a standing reevaluation schedule: any Adopt-tier tool on the radar gets a lightweight reassessment annually or when a major version ships |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "The Iteration Protocol is present and explicit. STOP points appear in every workflow. The boundary between AI action and human decision is clearly drawn ('NEVER implement in production'). The role loads well. Minor gap: the skill-loading table references files like `research-methodology.md` and `platform-landscape.md` but there is no instruction for what the AI should do if those files are not loaded — does it halt, ask, or proceed with degraded capability? This edge case should be addressed.",
      "example_rewrite": "Add to Context Requirements: **If required skills are not loaded:** Halt and request missing files before proceeding. Do not substitute general knowledge for `platform-landscape.md` — evaluating tools without knowing the current stack risks recommending tools that duplicate existing capabilities. State explicitly: 'I need [filename] before I can begin this evaluation.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "This is the strongest section. The current tooling stack is named specifically, priorities are ranked with rationale, and the phased research backlog is concrete and honest ('MVP: Minimal — focus on building'). The four backlog items are actionable. Minor issue: the backlog items lack a trigger condition. 'When Phase 2 begins' is stated in the table but not attached to the individual backlog items, making it easy to lose context when the list is referenced in isolation.",
      "example_rewrite": "1. **Observability stack for Vercel + Supabase** — TRIGGER: When Supabase integration begins in Phase 2. Evaluate Vercel Analytics + Sentry vs. a unified option. Owner: DevOps Research Lead. Deliver to: Head of Platform + SRE."
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. The artifact descriptions ('Evaluation reports, recommendations') are placeholders, not handoffs. Every delivery row should name the specific document, reference the template from the appendix, specify where it lands (knowledge base, Slack, wiki), and identify the STOP point that triggers the transfer. Until this is fixed, Platform roles receiving research outputs have no shared contract for what they will actually receive or when."
}
```