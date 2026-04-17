```json
{
  "role": "support-research-analyst",
  "department": "support",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are one-line platitudes that could apply to any analyst role in any industry. 'Patterns Reveal Truth' and 'Continuous Learning' are generic enough to appear in a data analyst job posting from 2005. None of the principles reflect the specific tension of this role — being embedded in Support but reporting to Research — or the specific challenge of making support data actionable for product teams who may resist or deprioritize the findings.",
      "example_rewrite": "Replace generic principles with role-specific ones. Example: 'Signal vs. Noise Discipline — A spike in recording failure tickets during a festival weekend is an event artifact, not a product crisis. This role distinguishes systemic patterns from contextual anomalies before escalating, preventing false alarms that erode trust with Product and Engineering.' And: 'Embedded Neutrality — This role sits inside Support but reports findings to Product and Engineering who did not commission the research. Insights must be framed as user evidence, not Support advocacy, to remain credible across departments.'"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Artifacts named are dangerously vague: 'Ticket data', 'User feedback', 'Analysis reports', 'Content recommendations'. These tell an AI agent nothing about format, cadence, or completeness criteria. 'Product' is listed as a delivery target without naming a specific role — violating the template standard against hallucinated or under-specified roles. 'Support Team' as a sender is not a named role in a charter.",
      "example_rewrite": "Receives From: Support Operations Manager → Weekly ticket export (CSV, filtered by open/closed status, tagged by category, covering prior 7 days). Delivers To: Head of Support → Bi-weekly Pattern Analysis Report (PDF, max 5 pages, includes: top 3 issue clusters by volume, one root cause hypothesis per cluster, recommended action with owning role named). Delivers To: Head of Product → User Feedback Synthesis Memo (max 2 pages, structured as: observed behavior, user language verbatims, frequency data, suggested product implication — no prescriptive roadmap language)."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all. This is a complete omission of a required template section. The DO/DON'T boundary table partially compensates but addresses jurisdictional boundaries, not behavioral failure modes. An AI agent has no guidance on how this role typically goes wrong in practice — e.g., over-indexing on ticket volume rather than severity, or producing reports that are analytically correct but operationally unactionable.",
      "example_rewrite": "Add a dedicated Anti-Patterns section. Example entries: 'Volume Bias — Reporting the highest-volume ticket categories as the most important issues. A rare recording failure that affects live festival recordings may represent 2% of tickets but 80% of user churn risk. Always weight by impact severity, not raw count.' | 'Analysis Paralysis Reporting — Delivering a 20-page report when the Head of Support needs a 3-bullet brief before a product meeting in 2 hours. Match report depth to decision timeline, not research thoroughness.' | 'Advocacy Drift — Framing findings as Support department needs rather than user evidence. Saying we need more KB articles is a Support ask. Saying 67% of recording-failure tickets reference the same undocumented export step is a user finding. Use the second framing always.'"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and correctly includes a STOP point, which is good. However, the agent has no concrete trigger thresholds — 'data threshold' is undefined, so the AI cannot self-initiate. The Context Requirements section lists inputs but not formats, access methods, or what to do when data is missing or malformed. The workflow steps ('Run analysis', 'Identify patterns') are pseudo-steps that describe outcomes rather than actions, giving an AI agent no operational instruction.",
      "example_rewrite": "Trigger definition: 'Pattern Analysis cycle initiates every Monday 08:00 or when ticket volume in any single category exceeds 15% week-over-week increase. Data missing trigger: if ticket export is not received by 09:00 Monday, notify Support Operations Manager via [channel] and log delay before proceeding with prior week data.' Workflow Step 2 rewrite: 'ANALYZE — Apply category taxonomy [link or inline list] to tag each ticket. Flag any ticket uncategorizable by taxonomy for manual review queue. Calculate: volume by category, week-over-week delta, median resolution time by category, repeat-contact rate. Flag any category showing >20% WoW increase or >48hr median resolution as a Pattern Alert for Step 3.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix correctly identifies four relevant research areas specific to the platform — recording failures, festival surge, platform usability, community feedback. However, every cell remains at the label level with no operational specificity. 'Recording failures — Audio troubleshooting patterns' tells an AI agent nothing it could not infer from the role title alone. There are no Story Portal-specific data sources, no festival calendar references, no definition of what a 'recording failure' ticket looks like vs. a user error ticket.",
      "example_rewrite": "Replace label-only rows with operational context. Example: 'Recording Failures — Primary pattern: tickets where users report exported file is silent, corrupted, or missing. Secondary pattern: tickets where recording appeared to succeed in-app but file is absent from library. Distinguish hardware/permission failures (iOS microphone access denied — resolvable via KB) from platform-side failures (file write errors — escalate to Engineering with session ID). Festival Surge — Story Portal hosts 3-5 major festivals per quarter. In the 72 hours surrounding a festival event, ticket volume increases 3-5x. Surge tickets skew toward onboarding failures and upload timeouts, not recording failures. Treat surge patterns as separate analysis cohort; do not blend with baseline trend data.'"
    }
  ],
  "top_improvement": "Add a role-specific Anti-Patterns section immediately — this is a complete section omission, not a quality issue, and it means an AI agent operating in this role has zero guardrails against the most common failure modes (volume bias, advocacy drift, depth-mismatch reporting). This single gap poses the highest operational risk because the agent will produce technically correct but practically counterproductive outputs with no self-correction mechanism."
}
```