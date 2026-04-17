```json
{
  "role": "strategic-analyst",
  "department": "strategy-business-dev",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic consulting platitudes that could apply to any analyst role in any industry. 'Data before decisions,' 'Unbiased analysis,' and 'Right insight, right time' are filler phrases with zero role-specific meaning. They do not reference Story Portal, festival markets, strategic options frameworks, or the specific tension between AI-generated analysis and human strategic judgment.",
      "example_rewrite": "| **Festival-First Framing** | Every market analysis starts by asking 'how does this affect our festival portfolio strategy?' — not generic market dynamics. | **Options Over Opinions** | Present 3+ evaluated options with trade-offs to the CSO; never deliver a single-path recommendation as if the decision is already made. | **Synthesis Over Summary** | Raw data from Market Research Analyst and CI Analyst is not intelligence — your job is the interpretive layer that connects data points to strategic implications. | **Confidence-Calibrated Outputs** | Every recommendation carries an explicit confidence rating (High/Medium/Low) with the limiting assumptions stated, so the CSO knows exactly where to probe. | **Bounded Scope Discipline** | When a request bleeds into market sizing (Market Research Analyst) or deep competitor profiling (CI Analyst), flag the boundary immediately rather than absorbing the work. | **Timeliness as Competitive Advantage** | A good analysis delivered after the decision window closes has zero value — scope aggressively to meet the decision timeline, not the ideal research timeline. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs use vague category labels like 'Analysis requests,' 'Research data,' and 'Strategic intelligence' — none of these are named artifacts. The template standard explicitly requires specifying what artifact is passed, not just a relationship description. Additionally, 'Executive Team' appears as a delivery target but is not a role defined in the charter — this is a hallucinated recipient. 'Research Team' appears as a source but is not a defined charter role.",
      "example_rewrite": "| Receives From | Artifact | Format |\n|---|---|---|\n| CSO | Strategic Analysis Brief — includes question scope, decision deadline, and success criteria | Structured brief (markdown) |\n| Market Research Analyst | Market Sizing Report — TAM/SAM/SOM with source citations | Standardized report |\n| Competitive Intelligence Analyst | Competitor Activity Log — recent moves, signals, and raw observations | Tagged data export |\n\n| Delivers To | Artifact | Format |\n|---|---|---|\n| CSO | Strategic Options Report — 3+ options, evaluation matrix, risks, and ranked recommendation | Structured report (PDF/doc) |\n| Business Planner | Opportunity Assessment Input — validated assumptions, market context, and risk flags for plan integration | Structured input document |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all. The DON'T list in Boundaries lists four ownership boundaries but these are not anti-patterns — they are jurisdictional rules. Anti-patterns should describe failure modes specific to how a Strategic Analyst actually fails: over-hedging recommendations to avoid commitment, scope creep into CI or market sizing work, analysis paralysis on AI-generated research, or presenting raw data as insight without synthesis. None of these appear anywhere in the document.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | Description | Correction |\n|---|---|---|\n| **The Hedge Cascade** | Every recommendation is so qualified ('it depends,' 'further research needed') that the CSO cannot make a decision. | Force a ranked recommendation even under uncertainty — state the confidence level and key assumptions instead of hedging the conclusion away. |\n| **Data Dump as Deliverable** | Forwarding CI Analyst outputs or Market Research reports to the CSO with light commentary, calling it strategic analysis. | The value-add is synthesis and implication — rewrite the output to answer 'so what does this mean for our festival strategy?' |\n| **Scope Absorption** | Accepting market sizing or deep competitor profiling tasks because it feels related to the analysis request. | Stop at the boundary, flag the gap to CSO, and formally request input from Market Research Analyst or CI Analyst rather than doing the work yourself. |\n| **Perpetual Research Loop** | Continuing to gather data past the decision window because the analysis doesn't feel complete. | Scope to the decision deadline. Deliver a time-bounded report with stated data gaps rather than missing the strategic window. |\n| **Framework Theater** | Applying SWOT or Porter's Five Forces because they were requested, without using the outputs to drive recommendations. | Every framework application must produce at least one actionable implication in the final report — frameworks are tools, not deliverables. |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol is present and the AI-Primary classification is correctly applied. However, the agent lacks operational specificity: there are no STOP checkpoints embedded in the workflows (Workflow 1 goes from SCOPE to DELIVER with no human gate until the very end), no definition of what 'approved' means at the STOP point, no list of the actual data sources the agent should access, and no guidance on what to do when data is ambiguous or conflicting. An AI agent loading this role would understand its general shape but would not know when to pause mid-workflow.",
      "example_rewrite": "In Workflow 1, insert explicit STOP gates:\n\n3. ANALYZE\n   - Apply frameworks\n   - Evaluate options\n   - Assess implications\n   → OUTPUT: Analysis findings draft\n   ⛔ STOP — Present analysis framing to CSO before synthesis\n   - Confirm: Are the right options being evaluated?\n   - Confirm: Are the evaluation criteria correct?\n   - IF misaligned → Return to SCOPE\n   - IF approved → Proceed to SYNTHESIZE\n\nAlso add to Agent Capabilities: 'Data conflict protocol — when two sources contradict on a key data point, flag both sources, state the discrepancy explicitly in the report, and default to the more conservative figure for any recommendation calculations.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the correct domain (festival market) but every entry remains generic. 'Market dynamics,' 'Competitive landscape,' and 'Growth options' could describe any business in any industry. There are no specific festival types, no named competitor archetypes, no defined partnership categories relevant to Story Portal's actual context, and no concrete analytical outputs tied to real decisions the CSO would face. The Strategic Questions table is the strongest element but still lacks specificity about what the answer would look like.",
      "example_rewrite": "| Strategic Question | Analysis Required | Output Format | Decision Owner |\n|---|---|---|---|\n| Which festival verticals (music, food, arts, corporate) represent the highest-value entry points for Story Portal's narrative platform? | TAM by vertical, current digital storytelling adoption rate, buyer profile analysis | Vertical Prioritization Matrix with top 3 recommended verticals ranked by opportunity score | CSO |\n| Which 2-3 competing storytelling or event-tech platforms pose the highest displacement risk in our target verticals? | Feature gap analysis, pricing model comparison, recent customer win/loss signals | Competitive Threat Brief with displacement risk score per competitor | CSO |\n| What partnership structure (white-label, co-marketing, API integration) offers the fastest path to 5 festival clients in Year 1? | Partnership model analysis across 3 structures, case studies from adjacent markets | Partnership Options Report with recommended structure and top 5 target partner profiles | CSO |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 role-specific failure modes. This role has zero anti-patterns documented, which means an AI agent has no behavioral guardrails against the most common Strategic Analyst failure modes — scope absorption from CI/Market Research, data-dump-as-deliverable, and hedge-cascade recommendations. This is the single highest-risk gap because it directly undermines the quality of outputs reaching the CSO."
}
```