```json
{
  "role": "ma-analyst",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "The six principles are labeled but not explained with any M&A-specific operational meaning. 'Fit Before Price' and 'Diligence Is Protection' are industry clichés that appear in every M&A textbook. 'Numbers Tell Truth' and 'Patience Pays' are generic enough to apply to any finance role. None of the principles describe HOW this AI agent should behave differently because of its specific context — a pre-revenue story/experience company with near-term low M&A priority. There is zero connection between the philosophy and the Story Portal context.",
      "example_rewrite": "Replace generic labels with operationally specific principles tied to Story Portal's stage and sector. Example: 'Acqui-Hire Over Asset Acquisition — For Story Portal at pre-revenue stage, talent and IP matter more than revenue multiples; weight team quality and technology defensibility above financial metrics in every target scorecard.' Another: 'Public-Data-Only Discipline — As an AI agent without NDA access, all research conclusions must be explicitly flagged as derived from public sources only; never extrapolate to non-public financials without a human-verified data source noted in the model.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoff tables name roles but describe artifacts only at the category level ('M&A priorities', 'Financial models', 'Research findings'). There is no specification of format, template, file type, data fields, or what constitutes a complete artifact. 'Strategic Analyst' and 'Corporate Development Manager' appear in the Works With table but are absent from both handoff tables with no explanation — it is unclear whether those roles exist in the charter or are hallucinated. The Receives From table has only three entries despite six collaboration partners listed above it.",
      "example_rewrite": "Replace vague artifact names with typed, structured descriptions. Example row: '| CSO | Delivers To | Target Shortlist Report — ranked list of ≤5 candidates, each with: strategic fit score (1-5), estimated valuation range, key risk flags, and recommended next action (Pass / Monitor / Pursue); delivered as a structured markdown report using the Target Shortlist Template v1 |'. Also add missing handoffs: '| Strategic Analyst | Receives From | Competitive Landscape Brief — named competitors, market sizing data, and positioning map relevant to the current screening criteria |'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section at all. The template standard explicitly requires 3-5 role-specific anti-patterns, and this role file contains none. The DON'T list in Boundaries is a boundary/scope list, not an anti-pattern list. Anti-patterns describe failure modes — ways the role could behave incorrectly while appearing to follow its mandate. This is a critical omission for an AI-Primary agent conducting autonomous financial research where hallucinated data or overconfident valuations could influence real acquisition decisions.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with M&A-specific failure modes. Example: 'ANTI-PATTERN 1 — Precision Theater: Presenting DCF outputs to two decimal places when input assumptions are based on public estimates. This creates false confidence. Always express valuation as a range with explicit assumption sensitivity noted. ANTI-PATTERN 2 — Recency Bias in Target Screening: Surfacing recently covered or trending companies because they appear more in search results, not because they best match criteria. Screen against the criteria document, not against what is easiest to find. ANTI-PATTERN 3 — Confusing Research Completeness with Due Diligence: Producing a thorough public-data report and labeling it due diligence. Always include a section header: PUBLIC RESEARCH ONLY — Full DD requires legal, financial, and operational access not available to this agent.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol is present and structurally correct, which is a baseline pass. However, the STOP points are underspecified — the protocol says 'STOP → Present for review' but does not define what triggers a mandatory stop versus a discretionary one, who specifically reviews, what approval looks like, or what the agent does if no response is received. The Agent Capabilities table lists 'financial modeling' and 'database access' without specifying what tools, APIs, or data sources are actually available. An AI agent loading this role would not know whether it has access to Crunchbase, PitchBook, public SEC filings, or nothing — a critical gap for an M&A research role.",
      "example_rewrite": "Specify STOP conditions and tool bindings explicitly. Example iteration protocol entry: 'STOP CONDITION 1 (Mandatory) — After Target Shortlist delivery: agent halts all further research until CSO provides written go/no-go on at least one target. Timeout: 5 business days. If no response, send one follow-up then set all targets to Monitor status. STOP CONDITION 2 (Mandatory) — If any risk flag is rated High (financial irregularity, litigation, regulatory issue): immediately halt modeling, generate a Risk Alert memo to CSO + CFO, and do not proceed until human acknowledgment received.' For tools: 'Available data sources: public web search, SEC EDGAR filings, Crunchbase free tier, LinkedIn company pages. NOT available: PitchBook, Bloomberg, private financials, NDA-gated data rooms.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix acknowledges the company's stage (pre-revenue) and names relevant acquisition domains (audio/AI, story platforms, interactive tech, community/festival orgs), which is a meaningful start. However, the section is static and declarative rather than actionable. There are no named real-world target examples or screening watchlists, no definition of what 'early-stage preferred' means in practice (pre-seed? Series A? sub-$5M ARR?), and no connection between the M&A timeline ('near-term: low priority') and what the agent should actually be doing right now. A role rated AI-Primary with Agent deployment should have a concrete current-state task defined in this section.",
      "example_rewrite": "Make the appendix operationally directive for the agent's current mode. Example: 'CURRENT OPERATING MODE: Passive Intelligence Gathering (pre-revenue stage). Agent should NOT initiate active target outreach or build full valuation models. Current task: maintain a rolling Technology Watchlist updated monthly. Watchlist criteria: companies building AI-assisted narrative tools, spatial audio experiences, or community storytelling platforms; founded 2020 or later; ≤Series A; team size 2-20. Output format: one-page snapshot per company using the Watchlist Entry Template. Deliver updated watchlist to CSO on the first Monday of each month. Escalate immediately if any watchlist company announces acquisition interest or funding round above $5M.'"
    }
  ],
  "top_improvement": "Add a role-specific Anti-Patterns section immediately — this is a zero-score omission on a required template element for an AI-Primary agent making autonomous financial research decisions. An M&A Analyst AI with no documented failure modes is a liability: it can produce precision-formatted hallucinated valuations, mislabel public research as due diligence, or surface trending targets over strategically fit ones with no guardrail to catch it. Draft 3-5 anti-patterns before this role is deployed in any live M&A context."
}
```