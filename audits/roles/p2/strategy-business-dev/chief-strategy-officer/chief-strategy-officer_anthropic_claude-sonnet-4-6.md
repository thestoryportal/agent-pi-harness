```json
{
  "role": "chief-strategy-officer",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic consulting-deck platitudes applicable to any strategic role at any company. 'Vision Guides Action,' 'Execution Is Strategy,' and 'Adaptability' could appear verbatim in a McKinsey slide from 1995. None reflect Story Portal's specific context — a festival-market AI experience startup where strategy means choosing which Burning Man-adjacent events to target before achieving product-market fit. There is no principle about capital-efficiency under startup constraints, about navigating festival organizer relationships, or about when to pivot versus persist on the Love Burn bet.",
      "example_rewrite": "Replace 'Adaptability — Strategy must evolve' with 'Festival-First Validation — Every strategic initiative must prove value at Love Burn before scaling; we do not expand a hypothesis we have not yet confirmed. Replace 'Alignment Creates Power' with 'Partner Trust Is the Moat — Festival organizers choose platforms they trust with their community narratives; relationship capital is a strategic asset that cannot be bought, only built incrementally.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs are severely under-specified on both sides. 'Receives: CEO → Vision, priorities' tells an AI agent nothing actionable — what format, what cadence, what triggers the handoff? 'Delivers: All C-Suite → Strategic direction' is not an artifact, it is a category. The template standard explicitly requires specifying what artifact is passed, not just who works with whom. Research Director appears in the Works With table but the handoff row does not specify whether the incoming artifact is a weekly competitive brief, a one-time market sizing model, or an ad-hoc query response. 'Board → Strategic plans' does not specify whether this is a quarterly deck, an annual 3-year plan, or a memo format.",
      "example_rewrite": "Receives From Research Director: 'Weekly Festival Market Intelligence Brief (festival-market-brief.md) — delivered every Monday by 9am; triggers CSO competitive review step in Workflow 1.' Delivers To CFO: 'Strategic Initiative Prioritization Sheet (strategic-priorities-v[N].xlsx) — ranked list of top 5 initiatives with estimated resource requirements; triggers CFO financial modeling within 5 business days.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all — it is entirely absent. The DO/DON'T boundary list under Boundaries is a jurisdiction map, not an anti-pattern list. Anti-patterns should describe failure modes specific to how a CSO in this context goes wrong: e.g., over-indexing on M&A thinking at a pre-PMF startup, treating festival organizer conversations as sales calls rather than partnership exploration, or building a 3-year strategic plan before Love Burn results are known. The template standard explicitly requires 3-5 role-specific anti-patterns, and this section scores near zero because it does not exist.",
      "example_rewrite": "Add Anti-Patterns section: '1. Enterprise Strategy Theater — Producing multi-year strategic plans with market-sizing slides before Love Burn data exists. At this stage, strategy is hypothesis testing, not planning. 2. M&A Distraction — Evaluating acquisition targets before achieving product-market fit; Story Portal cannot integrate what it has not yet proven. 3. Partnership Announcement Over Partnership Value — Signing festival MOUs for press visibility before the product delivers measurable attendee outcomes, burning relationship capital on optics.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Deployment Notes section states the classification is Human-Primary but the deployment is Hybrid, and includes an Iteration Protocol loop — which satisfies the template checklist requirement. However, the AI task boundaries are listed as 'AI assists with analysis' and 'AI generates reports' with zero specificity about which analysis tools, which report templates, or what inputs are required to trigger AI assistance. The Context Requirements section contains literal placeholder text '[Context item 1]' and '[Context item 2]' that was never filled in — this is a critical gap. An AI agent loading this role cannot determine what context files to load, what skills to activate, or what the boundaries of its analytical assistance are versus human judgment zones.",
      "example_rewrite": "Replace placeholder Context Requirements with: 'Required Context: [ ] story-portal-overview.md — organizational mission and product description [ ] festival-market-landscape.md — current target festival list and status [ ] love-burn-2025-brief.md — launch parameters and success metrics. Required Skills: competitive-analysis.md — load when conducting market positioning work; scenario-planning.md — load when evaluating strategic options with >$50K resource implications.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix is the strongest section in the file and shows genuine project awareness — Love Burn is named, the festival market framing is correct, the AI/experience advantage is acknowledged, and the four strategic priorities are sequenced sensibly (launch → PMF → expand → partner). However, the Strategic Questions table lists questions without answers, frameworks, or next actions, making it a brainstorming list rather than an operational guide. The Competitive Position table lists factors but does not connect them to specific decisions or constraints the CSO should apply. It reads as context-setting rather than role-activating.",
      "example_rewrite": "Add decision triggers to Strategic Questions: 'How do we scale beyond Love Burn? → Do not activate this question until Love Burn NPS > 70 and at least 3 organic festival inquiries received; premature scaling planning is a distraction. What festivals should we target? → Evaluation criteria: must have 500+ attendees, art/experience focus, organizer open to tech partnership; maintain a ranked target list in festival-pipeline.md updated monthly.'"
    }
  ],
  "top_improvement": "Add a complete Anti-Patterns section with 3-5 failure modes specific to a pre-PMF festival-market startup CSO, and simultaneously fill in the empty Context Requirements placeholders — these two gaps together mean the role provides no failure prevention guidance and cannot be operationally loaded by an AI agent, which defeats the core purpose of the role file."
}
```