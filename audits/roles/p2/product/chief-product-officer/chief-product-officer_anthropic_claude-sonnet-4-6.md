```json
{
  "role": "chief-product-officer",
  "department": "product",
  "scores": {
    "philosophy_depth": 6,
    "handoff_specificity": 5,
    "anti_pattern_quality": 3,
    "ai_deployment_clarity": 4,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 6,
      "finding": "Four of the six principles are reasonably specific to a CPO role ('Portfolio Thinking', 'Data-Informed Not Data-Driven', 'Strategic Tradeoffs'). However, 'Customer Obsession' is an Amazon corporate cliché used across every product role verbatim, and 'Vision Drives Execution' is generic leadership-speak with no CPO-specific texture. None of the principles reference the tensions unique to this role: balancing engineering feasibility against market timing, managing PM autonomy versus strategic coherence, or adjudicating between revenue-generating features and platform health.",
      "example_rewrite": "Replace 'Customer Obsession' with: '**Empathy Before Metrics** — User research and direct customer conversations precede any roadmap decision; NPS scores and funnel data confirm hypotheses but never replace them. A CPO who only reads dashboards loses the signal.' Replace 'Vision Drives Execution' with: '**Vision as Constraint, Not Script** — A clear product vision eliminates 80% of prioritization debates by giving teams a decision filter, not a feature list. If a PM needs the CPO to decide whether to build a feature, the vision has failed.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 5,
      "finding": "Handoff tables name roles correctly but artifacts are vague containers, not actual documents. 'Receives: Company strategy, objectives from CEO' and 'Delivers: Product requirements to CTO' could describe any executive at any company. No artifact has a format, cadence, or version reference. The handoff to CMO ('Product positioning') does not specify whether this is a one-pager, a positioning brief, a battle card, or a slide deck. 'Product updates' to the Board is similarly undefined. This means an AI agent or a new human hire cannot execute a handoff without guessing.",
      "example_rewrite": "| Delivers To | Artifact | Format | Cadence |\n|---|---|---|---|\n| CTO | Product Requirements Brief | Structured doc: problem statement, success metrics, constraints, out-of-scope | Per initiative, before sprint planning |\n| CMO | Product Positioning Memo | 1-page: target user, core problem, key differentiators, proof points | Per launch, 6 weeks pre-release |\n| Board | Product Dashboard + Narrative | Slide deck: OKR status, top 3 risks, portfolio health, next-quarter bets | Quarterly, 48hrs before board meeting |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 3,
      "finding": "This role has NO dedicated anti-patterns section at all. The DON'T list in Boundaries touches on scope violations ('Dictate engineering implementation', 'Micromanage product managers') but these are boundary rules, not behavioral anti-patterns. There is no section identifying failure modes specific to a CPO: e.g., vision inflation (vision so abstract it cannot constrain decisions), roadmap theater (detailed Gantt charts masking lack of strategic clarity), HiPPO deference (caving on priorities when the CEO expresses a preference), or over-rotating to enterprise customers at the expense of the core user. The template checklist explicitly requires 3-5 role-specific anti-patterns.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | What It Looks Like | Why It Fails |\n|---|---|---|\n| **Vision Inflation** | Vision statement is so aspirational ('empower humans') it cannot eliminate a single feature from the roadmap | Teams fill the vacuum with their own interpretations; roadmap becomes a wish list |\n| **Roadmap Theater** | 18-month feature roadmap presented to board with quarterly precision | Creates false certainty, punishes honest replanning, trains stakeholders to expect delivery theater |\n| **HiPPO Override** | CPO reverses roadmap priority after CEO mentions a competitor in passing | Destroys PM credibility and signals that strategy is performative |\n| **Discovery Debt** | Shipping two quarters of features without a single unmoderated user session | Product drifts from actual user mental models; NPS drops lag by 6 months |\n| **Portfolio Neglect** | All strategic attention on flagship product; adjacent products starved of vision | Creates internal inequity and leaves market flanks undefended |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 4,
      "finding": "The Deployment Notes section correctly identifies this as Human-Primary and lists what AI assists with, but provides zero operational guidance for an AI agent actually performing the assistance tasks. 'AI assists with research synthesis' and 'AI analyzes market data' are intentions, not instructions. There is no guidance on: what inputs the AI needs to begin a research synthesis, what format the output should take, how to handle ambiguous strategic questions, or what to do when asked to make a decision that belongs to the human. The Context Requirements section is literally left as '[Context item 1]' and '[Context item 2]' placeholders — unfilled template fields that represent a critical quality failure.",
      "example_rewrite": "### AI Assistance Protocol\n\n**When asked to synthesize research:**\n- Input required: raw interview transcripts or survey data + strategic question being answered\n- Output format: insight memo with (1) top 3 patterns with evidence quotes, (2) implications for roadmap, (3) open questions for human follow-up\n- DO NOT: draw strategic conclusions — surface patterns, flag the decision to the human\n\n**When asked to draft a board update:**\n- Input required: current OKR scores, roadmap snapshot, CPO's narrative notes\n- Output format: draft slide titles + talking points, flagged with [HUMAN REVIEW] on any forward-looking claim\n\n**STOP — escalate to human when:**\n- Asked to prioritize features without explicit criteria\n- Asked to represent company position to external parties\n- Strategic question involves a tradeoff the human has not pre-authorized\n\n### Required Context\n- [ ] current-okrs.md — active product OKRs and status\n- [ ] product-strategy-2025.md — approved strategic priorities\n- [ ] competitive-landscape.md — last updated competitive snapshot"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names the project vision ('Make empathy contagious') and the MVP event (Love Burn 2025), which is better than nothing. However, the five product priorities are generic startup priorities that apply to any MVP at any festival — they contain no Story Portal-specific product thinking. There is no mention of the core product mechanic (the wheel-to-story loop) in strategic terms: what does success look like for that loop, what is the validated hypothesis, what would cause the CPO to pivot away from it? The appendix reads as a status summary, not as CPO-level strategic context that would help a human or AI agent understand what decisions are live.",
      "example_rewrite": "### CPO Strategic Context — Story Portal MVP\n\n**Core Bet:** The wheel-to-story loop is the product's primary value mechanism. We believe randomized prompt selection reduces the blank-page barrier and produces stories users feel proud to share. This hypothesis is UNVALIDATED — Love Burn 2025 is the validation event.\n\n**Success Criteria for MVP:**\n- ≥60% of wheel spins result in a submitted story (loop completion rate)\n- ≥40% of submitted stories shared externally (empathy contagion signal)\n- Qualitative: facilitators report the tool 'starts conversations without them'\n\n**Live Strategic Questions (CPO owns the answer):**\n- If loop completion rate is <30%, do we iterate the prompt library or the UX before next festival?\n- At what point does the festival-first strategy expand to non-festival contexts?\n- Should the portfolio add an archive/browse experience at MVP or post-validation?\n\n**What the CPO is NOT deciding yet:** Monetization model, platform integrations, team scaling — deferred until post-Love Burn data."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 CPO-specific failure modes (Vision Inflation, Roadmap Theater, HiPPO Override, Discovery Debt, Portfolio Neglect) — this section is completely absent, which means the role has no behavioral guardrails and fails a mandatory template requirement. This is the highest-leverage fix because anti-patterns are the primary mechanism by which a framework prevents an AI agent or new hire from defaulting to plausible-but-wrong behavior."
}
```