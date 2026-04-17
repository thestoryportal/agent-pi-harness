```json
{
  "role": "product-manager",
  "department": "product",
  "scores": {
    "philosophy_depth": 5,
    "handoff_specificity": 5,
    "anti_pattern_quality": 6,
    "ai_deployment_clarity": 7,
    "story_portal_relevance": 8
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 5,
      "finding": "All six principles are generic PM platitudes that could appear in any product management textbook or job description. 'Outcomes Over Outputs', 'Evidence Over Opinion', and 'Continuous Discovery' are industry clichés with no grounding in Story Portal's specific context, constraints, or tradeoffs. There is nothing here that would distinguish this PM from a PM at a fintech company, an e-commerce platform, or an enterprise SaaS tool. The table format also encourages brevity to the point of meaninglessness — 'Success is solving problems, not shipping features' tells the AI nothing about how to behave differently when under festival deadline pressure.",
      "example_rewrite": "| **Festival Deadline Is a Hard Constraint** | Story Portal ships at a live event. A feature that is 80% good and deployed beats a perfect feature that misses the festival. When discovery and delivery tension arises, bias toward shippable over ideal. | | **Offline-First Is a User Need, Not a Technical Nicety** | Festival environments have unreliable connectivity. Every requirement must pass the question: does this work with no internet? Requirements that assume connectivity are invalid. | | **Consent Is Non-Negotiable Scope** | Story Portal records real people at a public event. Consent flow requirements are P0 blockers — they are never traded against timeline, never descoped, never deferred. | | **Anonymous Users Have No Second Chance** | Festival attendees are one-time visitors. Onboarding friction, confusing UI, or a failed first recording cannot be recovered with a follow-up email. Requirements must account for zero prior context. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoffs use vague artifact labels that do not tell an AI agent what format, contents, or completion state to expect or deliver. 'Requirements, priorities' delivered to Engineering could mean a Notion doc, a Jira epic, a Slack message, or a verbal conversation. 'User insights' received from Product Research Lead has no format or minimum content standard. Critically, the collaboration table lists 'Frontend Developer' and 'Backend Developer' as separate roles but the charter may not define them that way, and no handoff rows exist for them despite being listed as collaborators. The receives/delivers split also omits QA Lead from the Receives column entirely, creating a one-way relationship that does not reflect sprint reality.",
      "example_rewrite": "| Delivers To | Artifact | Format | Completion Signal | | Engineering Manager | PRD with acceptance criteria | Notion doc, linked in GitHub Issue, tagged 'ready-for-eng' | EM comments 'refined' on the issue | | UX Designer | Problem brief with user need statement, constraints, and 3 user scenarios | Notion doc shared in #design channel | Designer confirms in thread before wireframes begin | | QA Lead | Acceptance criteria checklist per story | Checklist block inside each GitHub Issue | QA Lead marks issue 'criteria-reviewed' before sprint start | | Product Marketing Manager | Feature one-pager: what it does, who it helps, launch timing | Notion doc in PMM folder | PMM confirms receipt before go-to-market planning |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 6,
      "finding": "Four of the six anti-patterns ('write vague requirements', 'skip discovery', 'micromanage implementation', 'commit timelines for team') are universal PM anti-patterns found in every agile certification course. They are not derived from Story Portal's context, the Hybrid classification, or the festival deployment scenario. The most dangerous anti-patterns for this specific role — an AI-assisted PM working under a hard festival deadline with a small cross-functional team — are completely absent. For example: the AI drafting requirements that sound complete but embed hidden assumptions about connectivity, the PM over-rotating to stakeholder requests at the expense of the P0 offline/consent work, or the AI producing a polished PRD for a P2 feature while P0 acceptance criteria remain undefined.",
      "example_rewrite": "| AI-drafted PRD accepted without feasibility check | AI produces fluent, confident requirements that may assume always-on connectivity or persistent user accounts — neither valid for Story Portal | Before any AI-drafted PRD is shared with Engineering, PM must manually verify every assumption against the offline-first and anonymous-user constraints | | Scoping P1 features while P0 acceptance criteria are undefined | Visual polish feels tangible and satisfying to refine; consent flow and PWA offline behavior are harder to specify | Backlog rule: no P1 story enters refinement until all P0 stories have complete, reviewed acceptance criteria | | Treating festival prep as a separate track from product delivery | 'Support festival preparation' listed as Priority 4 implies it is downstream of product work — but device setup, field testing, and offline sync validation are product delivery at a festival | Festival readiness checklist is part of the Definition of Done for every P0 feature, not a separate workstream |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 7,
      "finding": "The Iteration Protocol and Hybrid classification section clearly delineate AI versus human responsibilities, and the STOP points in workflows are present and reasonable. The role scores above threshold here. The one gap is that the AI agent has no guidance on what to do when it receives ambiguous or conflicting inputs — for example, a stakeholder request that conflicts with a P0 item, or a discovery finding that undermines a feature already in sprint. The iteration protocol covers the write-review-revise loop but not the conflict-escalation loop. An AI agent encountering a contradiction would have no rule to follow other than generic escalation paths listed in the Boundaries section.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 8,
      "finding": "The Story Portal appendix is the strongest section in the file. It names real features with real priority levels and real statuses, provides concrete success metrics with numeric targets, and maps PM priorities to the actual festival context. This is genuinely actionable. The one gap is that the current-state table describes 'Metrics: Not instrumented' and 'User Research: Limited' but the PM Priorities list does not include closing either gap before the festival — instrumenting analytics and conducting even minimal user testing would directly inform whether the 70% completion rate target is achievable. Priority 4 'Support festival preparation' is also undefined — what does that mean in practice for the PM role specifically?",
      "example_rewrite": "| Priority | Focus | Definition of Done | | 4 | Festival readiness | PM has defined and shared a field operations checklist covering: device setup steps, offline sync verification procedure, consent flow walkthrough script for facilitators, and a known-issues list for on-site staff. Checklist reviewed and approved by Engineering Manager before event date. |"
    }
  ],
  "top_improvement": "Rewrite all six philosophy principles to be Story Portal-specific and constraint-driven. Generic principles like 'Outcomes Over Outputs' provide zero behavioral guidance to an AI agent operating under a hard festival deadline with offline-first requirements and anonymous one-time users. Principles grounded in actual project constraints — consent is non-negotiable scope, offline-first is a requirement filter not a technical preference, festival deadline favors shippable over perfect — would change how the AI drafts requirements, resolves tradeoffs, and escalates conflicts in ways the current principles never could."
}
```