```json
{
  "role": "chief-technology-officer",
  "department": "engineering",
  "scores": {
    "philosophy_depth": 7,
    "handoff_specificity": 6,
    "anti_pattern_quality": 7,
    "ai_deployment_clarity": 8,
    "story_portal_relevance": 6
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 7,
      "finding": "All 6 principles are present and most are CTO-specific. 'Technology Serves Business' and 'Build for the Long Game' are genuinely role-appropriate. However, 'Bias for Action' and 'People Over Process' are lifted almost verbatim from common leadership maxims (Agile manifesto, Amazon leadership principles) and carry no CTO-specific meaning. A CTO's version of 'Bias for Action' should specify what kinds of decisions warrant speed versus deliberation — e.g., reversible architecture choices vs. vendor lock-in.",
      "example_rewrite": "Replace 'Bias for Action' with: 'Reversibility Over Perfection — Categorize every major decision by how hard it is to undo. Ship fast on reversible choices (framework swaps, tooling); slow down on irreversible ones (platform lock-in, data architecture). Speed is a feature, but only where the cost of being wrong is recoverable.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 6,
      "finding": "The handoff tables name real roles, which is correct, but the artifacts are vague on the inbound side. 'CEO → Business strategy, priorities' and 'Chief Product Officer → Product roadmap, requirements' do not specify format, cadence, or what the CTO is expected to do with them. The outbound side is slightly better ('Architecture principles, approvals') but still lacks artifact format. A reviewer cannot tell whether 'Technical direction, standards' delivered to the Engineering Manager is a Slack message, a Notion doc, or a quarterly presentation.",
      "example_rewrite": "Change 'Engineering Manager | Technical direction, standards' to: 'Engineering Manager | Quarterly Engineering Direction Memo (written doc: priorities, quality bar, anti-patterns to avoid this quarter) + Architecture Decision Records (ADRs) for approved major changes, delivered within 5 business days of strategy update.'"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 7,
      "finding": "Six anti-patterns are listed, which exceeds the minimum, and most are CTO-relevant. 'Ivory Tower Strategy' and 'Heroic Intervention' are genuinely specific to executive engineering leaders. However, 'Analysis Paralysis' and 'Technology for Technology's Sake' are universal leadership anti-patterns that appear in virtually every executive role file. They add no discriminating signal about what a CTO specifically gets wrong. The 'Instead' column for 'Analysis Paralysis' ('Make decisions with incomplete information') is also dangerously vague — it gives no CTO-specific heuristic.",
      "example_rewrite": "Replace 'Analysis Paralysis' with: 'Consensus Theater — Running architecture reviews until everyone agrees, mistaking absence of objection for quality alignment. CTOs who need unanimous buy-in before deciding train their organizations to stall. Instead: set a decision deadline upfront, document dissenting views in the ADR, and commit. Revisit in 90 days with data.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 8,
      "finding": "This is the strongest dimension. The role clearly separates what AI can and cannot do, provides a task-level table showing the division of labor, and correctly identifies that strategic decisions, vendor negotiations, and board representation are human-only. The skill files are appropriately called out as planned rather than falsely claimed as existing. Minor gap: there is no instruction for how the AI should behave when it detects the human is about to violate one of the anti-patterns (e.g., drifting into analysis paralysis). A trigger-based intervention heuristic would sharpen this further.",
      "example_rewrite": null
    },
    {
      "dimension": "story_portal_relevance",
      "score": 6,
      "finding": "The Story Portal appendix names the right decisions (Supabase, offline-first, PWA, legacy folder) but stays at a surface level. 'Validate platform choice, approve investment' for Supabase tells a CTO nothing actionable — what criteria should drive that validation? What is the specific risk being mitigated? The 'legacy folder migration' mention is a concrete detail, but it floats without context: what is in that folder, what is the migration target, and what is the CTO's actual decision right here versus the Solutions Architect's? The quality bar at the bottom ('supports 10x current usage') is a useful concrete target but is not connected to any current baseline metric.",
      "example_rewrite": "Replace 'Supabase Selection | Validate platform choice, approve investment' with: 'Supabase Selection | CTO decision right: approve or reject Supabase as Phase 2 backend. Validation criteria: (1) confirms offline-first sync is achievable without custom conflict-resolution code, (2) pricing model survives 10x user growth without renegotiation, (3) Solutions Architect signs off on row-level security model for multi-user story data. Risk being mitigated: vendor lock-in on auth + storage simultaneously. Decision deadline: before Phase 2 sprint planning.'"
    }
  ],
  "top_improvement": "Handoff specificity is the highest-priority fix. The inbound artifacts from CEO and CPO are named but not defined in format or cadence, and the outbound artifacts to Engineering Manager and Solutions Architect lack enough detail to be actionable. Without knowing what artifact is expected, in what form, and when, role coordination degrades to verbal agreements — which defeats the purpose of a structured handoff table. Rewrite every handoff row to include: artifact name, format (doc/deck/ADR/memo), and delivery trigger or cadence."
}
```