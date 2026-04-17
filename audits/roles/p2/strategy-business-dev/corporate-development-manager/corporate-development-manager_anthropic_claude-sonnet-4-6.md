```json
{
  "role": "corporate-development-manager",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic management platitudes that could apply to any coordinator, project manager, or operations role in any industry. 'Execution Is Strategy' and 'Documentation Matters' carry zero role-specific meaning. None reference Corporate Development's unique tension between confidentiality and cross-functional coordination, the deal lifecycle, or the challenge of influencing without authority. The table format also hides the lack of substance — 'Plans without action fail' is not a philosophy, it's a truism.",
      "example_rewrite": "| **Confidentiality Is Non-Negotiable** | M&A and investment work lives and dies on information control. Premature disclosure kills deals and creates liability. Every workstream is need-to-know until CSO clears it. |\n| **Influence Without Authority** | This role coordinates department heads who don't report to you. Persuasion, shared goals, and relationship capital are the only real tools — directives don't work here. |\n| **Deal Momentum Is Fragile** | Investment and M&A timelines collapse when coordination lags. A 48-hour delay in DD materials can cost a term sheet. Urgency is the default posture, not the exception. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but artifacts are described at the level of categories, not actual documents. 'Due diligence' is a process, not an artifact. 'Initiative priorities' could be a Slack message or a 50-page deck. The AI agent cannot distinguish what it is receiving or delivering. Additionally, the handoff table does not specify format, cadence, or what constitutes a complete handoff, and there is no mention of what happens when artifacts are incomplete or late.",
      "example_rewrite": "| Receives From | Artifact | Format | Completeness Gate |\n|---|---|---|---|\n| CSO | Signed Initiative Brief (scope, success metrics, timeline, assigned budget) | Google Doc | Cannot begin planning without CSO signature |\n| M&A Analyst | DD Tracker (open items list, owner, due date, red flags flagged) | Shared spreadsheet | Must show >80% items resolved before DECIDE stage |\n| CFO | Investment Parameters Memo (check size range, return hurdle, timeline constraints) | PDF memo | Required before Intake stage is marked complete |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all. The DO/DON'T boundary list under Core Identity is not a substitute — it describes scope, not failure modes. Anti-patterns should describe how this specific role fails in practice: the temptation to over-coordinate and create process theater, leaking deal information to align stakeholders prematurely, becoming a bottleneck by owning all communication, or confusing status reporting with actual issue resolution. None of this is present.",
      "example_rewrite": "### Anti-Patterns\n\n| Anti-Pattern | What It Looks Like | Why It Fails |\n|---|---|---|\n| **Process Theater** | Creating elaborate tracking dashboards and weekly syncs that report status without resolving blockers | Stakeholders feel managed; nothing actually accelerates |\n| **Premature Alignment** | Sharing deal details with department heads before CSO clears it to get early buy-in | Leaks kill deals; creates liability and loss of trust |\n| **Communication Bottleneck** | Routing all cross-functional messages through yourself to maintain visibility | Slows execution; builds resentment from teams who need direct access |\n| **Status Reporting as Delivery** | Sending weekly updates that describe slippage without an escalation or resolution plan attached | Surfaces problems without solving them; CSO receives noise, not decisions |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is structured, which is above baseline. However, the Context Requirements section is completely unfilled — two literal placeholder brackets '[Context item 1]' and '[Context item 2]' with no content. Required Skills also contains only a format note with no actual skills listed. An AI agent loading this role has no idea what context files to pull, what tools to use, or what the starting state looks like. The division of human vs. AI tasks in Deployment Notes is directionally correct but too vague — 'AI assists with tracking' does not tell an agent what tracking system to use or what a tracking output looks like.",
      "example_rewrite": "### Required Context\n- [ ] Active initiative list with current status, owner, and milestone dates\n- [ ] CSO's current strategic priorities memo (quarter)\n- [ ] Open investment opportunity log from M&A Analyst\n- [ ] Cross-functional dependency map for MVP delivery\n- [ ] Story Portal org chart (to identify correct escalation path)\n\n### Required Skills\n| Skill | When to Load |\n|---|---|\n| project-tracking.md | When creating or updating initiative plans |\n| m-and-a-process.md | When coordinating due diligence workstreams |\n| stakeholder-communication.md | When drafting status updates for CSO or CFO |"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section in the file — it names actual initiatives (Love Burn, MVP, Seed funding), assigns statuses, and maps coordination areas to functional teams. It earns a passing score. However, it stops short of being actionable: priorities are listed but not linked to workflows, there are no success metrics per initiative, and there is no indication of what 'Active' means in terms of current blocker or next action. An AI agent reading 'Love Burn partnership — Active' cannot determine what to do next.",
      "example_rewrite": "| Initiative | Status | Current Blocker | Next Action | Owner of Next Action |\n|---|---|---|---|---|\n| MVP development | Active | Engineering velocity below plan | Weekly sync with Product lead to surface scope cuts | Corporate Dev Manager facilitates, Product Head decides |\n| Love Burn partnership | Active | Contract terms under CSO review | Await CSO redline; prepare integration timeline draft in parallel | CSO on contract; Manager on timeline |\n| Seed funding | Future | Pitch deck not finalized | Coordinate with Business Planner to complete financial model section | Business Planner delivers model by [date] |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4 role-specific failure modes. This role has zero anti-patterns documented, which means an AI agent has no guardrails against the most common ways a Corporate Development Manager fails: process theater, premature information sharing, becoming a communication bottleneck, and mistaking status reporting for problem resolution. This is the single highest-risk gap in the file."
}
```