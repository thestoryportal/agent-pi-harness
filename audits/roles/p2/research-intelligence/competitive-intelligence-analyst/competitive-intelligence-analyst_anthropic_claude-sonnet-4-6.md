```json
{
  "role": "competitive-intelligence-analyst",
  "department": "research-intelligence",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 3
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic consulting clichés that could appear in any research role. 'Know Thy Competition' is a truism, not a guiding principle. 'Continuous Monitoring' describes a task, not a philosophy. 'Ethical Research' is a legal baseline, not a distinctive belief. None of these principles explain HOW this analyst thinks differently, what tradeoffs they make, or what they prioritize when signals conflict. There is no principle about, for example, how to handle incomplete data, how to weight primary vs. secondary sources, or how to avoid mirror-imaging (projecting your own logic onto competitors).",
      "example_rewrite": "Replace generic principles with role-specific thinking stances. Example: | **Absence Is Also a Signal** | When a competitor goes quiet — stops hiring, pulls back from events, removes features — that silence is intelligence. Treat gaps in activity as data, not noise. | and | **Resist Mirror-Imaging** | Do not assume competitors make decisions the way we would. Analyze their constraints, culture, and incentives on their own terms. A move that seems irrational to us may be rational to them. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Every handoff artifact is a vague category label, not a named deliverable. 'Competitive reports' delivered to Research Director tells an agent nothing about format, frequency, or content threshold. 'Competitive insights' to Sales could mean anything. The receives column is equally vague: 'Research priorities' from Research Director has no format, cadence, or trigger. Critically, several roles in the Works With table — 'Industry Analyst', 'Chief Strategy Officer', 'Product Marketing Manager' — may not exist in the Organizational Charter, which violates the hallucinated-roles rule. No handoff specifies what triggers the transfer or what done looks like.",
      "example_rewrite": "Replace vague artifacts with named documents and triggers. Example: | Delivers To | Artifact | Trigger | Format | | Research Director | Weekly Competitive Pulse Report | Every Friday 5pm | Structured brief: 3 flagged moves, 1 threat upgrade, 1 opportunity | and | Delivers To | Artifact | Trigger | Format | | Sales Director | Competitive Battle Card Update | When competitor releases new pricing or feature | One-page win/loss positioning sheet per competitor |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "There is no dedicated Anti-Patterns section in this role file at all — it is entirely absent. The DON'T list in Boundaries is not equivalent: it lists ownership violations ('don't set competitive strategy') rather than cognitive or behavioral failure modes specific to competitive intelligence work. Role-specific anti-patterns would include things like recency bias toward dramatic moves, over-indexing on a single competitor, treating job postings as confirmed strategy, or producing intelligence that is comprehensive but never actionable. None of these appear anywhere in the document.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with role-specific failure modes. Example: | Anti-Pattern | Description | Correct Behavior | | **The Last Move Fallacy** | Assuming a competitor's most recent action reveals their full strategy. A product launch may be a distraction or a pivot test. | Analyze moves in context of 6-month pattern, not in isolation. | | **Job Posting Literalism** | Treating a job posting for a 'Head of X' as proof the competitor is entering market X. Postings are aspirational and frequently cancelled. | Flag as weak signal only; require corroboration from 2+ additional sources before escalating. | | **Completeness Over Urgency** | Delaying an alert because the full profile isn't finished. A 70% complete urgent threat report delivered today beats a 100% report delivered next week. | Use tiered output: Flash Alert (same day, partial data) vs. Full Analysis (complete, scheduled). |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol exists and is structurally sound, and the Agent Capabilities table gives reasonable starting context. However, the STOP point in the iteration loop ('STOP → Present for review') has no criteria for what triggers escalation versus routine delivery — an agent cannot distinguish between a report that needs human review and one that can be auto-delivered. The workflows have no STOP checkpoints embedded within them (Workflow 1 and 2 run to completion with no human gate). The Context Requirements table lists inputs but not what the agent should do if those inputs are missing or ambiguous. Tool names are placeholders ('Monitoring Tools', 'Alert Systems') with no actual system references.",
      "example_rewrite": "Embed explicit STOP criteria in the iteration protocol and workflows. Example in Workflow 1: '3. ANALYZE → STOP: If analysis reveals a Tier 1 threat (competitor entering core market, pricing attack, or acquisition of direct rival), halt workflow and escalate to Research Director before proceeding to SYNTHESIZE. Do not finalize report without human review of threat classification.' And in iteration protocol: 'STOP criteria: Always stop if (a) confidence in source validity < 70%, (b) findings contradict prior approved intelligence, or (c) implications touch product roadmap or pricing strategy.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 3,
      "finding": "The Story Portal appendix is superficial and not actionable. The competitor categories ('Interactive Installations', 'Festival Experiences') are placeholder labels with no named competitors, no monitoring sources specific to this industry, and no intelligence questions tied to Story Portal's actual strategic concerns. The 'Key Questions' table asks questions any analyst would ask generically. There is no mention of how competitive intelligence connects to Story Portal's specific context — e.g., what a competitive threat looks like for an enterprise AI workforce framework, who the actual rival vendors are, or what signals (conference appearances, GitHub activity, pricing page changes) are most relevant. The appendix reads as a template stub that was never populated.",
      "example_rewrite": "Replace placeholder categories with Story Portal-specific intelligence targets and sources. Example: | Competitor | Type | Primary Monitoring Sources | Key Intelligence Question | | **Narrative AI** | Direct — AI workflow narrative tooling | Product changelog, LinkedIn hiring (prompt engineers), G2 reviews | Are they moving from single-agent to multi-role orchestration? | | **Prolific Machines** | Adjacent — interactive installation platforms | Event listings (SXSW, Sundance), press releases, job boards | Do they have an enterprise licensing model emerging? | and add: | Signal Type | Source | Cadence | Escalation Threshold | | New enterprise pricing page | Direct URL monitoring | Daily | Any change → Flash Alert to Research Director |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4-5 role-specific cognitive failure modes (e.g., Last Move Fallacy, Job Posting Literalism, Completeness Over Urgency). This role file currently has zero anti-patterns — the single highest risk for an AI-Primary agent that operates autonomously is that it has no guard rails against the specific reasoning errors that make competitive intelligence dangerous when wrong. A hallucinated or over-interpreted competitive threat can cascade into product and strategy decisions. This gap is more dangerous than vague handoffs or generic philosophy because those only reduce usefulness; missing anti-patterns actively enable confident misanalysis."
}
```