```json
{
  "role": "industry-analyst",
  "department": "research-intelligence",
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
      "finding": "All six principles are label-only platitudes with no behavioral specificity. 'Deep Industry Knowledge: Understand the full ecosystem' and 'Context for Strategy: Industry shapes strategy' are self-evident restatements of the job title. None of the principles explain HOW this analyst thinks differently from a generic researcher, what trade-offs they favor, or what beliefs guide difficult judgment calls. A Market Research Analyst could copy-paste five of these six without contradiction.",
      "example_rewrite": "Replace generic entries with opinionated stances. Example — 'Forces Over Events: When a competitor launches a new product, the interesting question is not what they launched but which structural force made that move inevitable. We report the force, not the headline.' And: 'Value Chain Primacy: Every strategic question has a value chain answer. Before assessing a trend, map where it enters the chain and who captures or loses margin as a result — that is the actual insight.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but specify only vague artifact categories. 'Delivers To: Strategy → Industry intelligence' and 'Delivers To: All Teams → Industry context' are placeholders, not operational handoff definitions. 'All Teams' is not a role. There is no specification of artifact format (report, briefing deck, structured data feed, Slack alert), triggering condition, or SLA. The inbound side is equally vague: 'Receives From: Strategy → Strategic questions' gives the AI no schema for what a strategic question looks like or how to intake it.",
      "example_rewrite": "Receives From: Research Director → Quarterly Research Priority Brief (structured doc listing top 5 industry focus areas, named industries, horizon, and strategic questions to answer). Delivers To: Chief Strategy Officer → Industry Situation Report (standardized 4-section PDF: Industry Forces Scorecard, Value Chain Shift Log, Regulatory Horizon Table, Analyst Implications Summary) — triggered at end of each analysis cycle, reviewed before quarterly planning session."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no Anti-Patterns section in this role file at all — it is entirely absent. The DO/DON'T/ESCALATE block in Boundaries partially substitutes but lists only boundary violations (do not size markets, do not execute partnerships), not behavioral failure modes. There are zero role-specific anti-patterns such as over-indexing on published reports rather than synthesizing original insight, confusing industry-level trends with company-level signals, or producing exhaustive maps with no prioritization signal. The template standard explicitly requires 3-5 role-specific anti-patterns.",
      "example_rewrite": "Add an Anti-Patterns section with entries such as: (1) 'Report Aggregation Disguised as Analysis — Summarizing what three industry reports say without synthesizing a point of view. Deliverable must include an Analyst Conclusion section distinct from source summaries.' (2) 'Trend Confirmation Bias — Tracking only signals that confirm an existing industry narrative. Each trend report must include a Counter-Signal subsection.' (3) 'Player List Without Power Map — Listing industry participants without assessing relative influence, margin capture, or switching costs. Every industry map must include a Power Distribution column.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol loop exists and is structurally sound, and Agent Capabilities are listed. However, the AI has no decision logic for ambiguous situations: no criteria for what constitutes a 'major industry shift' warranting escalation versus a routine update, no instructions on how to handle conflicting source data, no definition of analysis depth per request type (ad hoc question vs. quarterly report vs. monitoring alert). The STOP point exists but has no acceptance criteria — the AI cannot determine whether a report is ready for human review or needs another iteration.",
      "example_rewrite": "Expand the STOP gate with explicit criteria: 'STOP → Present for review IF: (a) Porter's Five Forces assessment complete with evidence citation for each force, (b) at least 3 independent sources corroborate each major finding, (c) Analyst Implications section contains at least one strategic recommendation, (d) any identified regulatory change is flagged with estimated effective date. IF any criterion unmet → return to ANALYZE step and log gap in iteration notes.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies four relevant industries and four industry forces, which shows project awareness. However, none of the entries are actionable for an AI agent. The Value Chain table lists generic player types (Artists, Designers, Festivals) with no named organizations, no Story Portal-specific dynamics, and no connection back to workflows or deliverables. The Industry Priorities table is a ranked list with no associated research questions, output format, or owner. The Force relevance ratings ('High opportunity', 'Core alignment') carry no analytical substance.",
      "example_rewrite": "Rewrite Industry Forces with specific research mandates: 'Experience Economy Growth (Priority: High) → Monthly monitoring task: track consumer spending shift from goods to experiences using festival attendance data, ticketing revenue reports, and NEA cultural participation surveys. Deliverable: Experience Economy Index updated in Research Shared Drive by first Monday of each month, flagging any quarter-over-quarter shift >5%. Trigger escalation to Research Director if index declines two consecutive months.'"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific behavioral failure modes. This is the highest-priority fix because the section is entirely missing — not merely weak — and anti-patterns are the primary mechanism preventing an AI-Primary agent from drifting into low-value behaviors like report aggregation, trend confirmation bias, or producing industry maps with no power analysis. Without this guardrail, every workflow cycle risks producing outputs that look complete but carry no analytical value."
}
```