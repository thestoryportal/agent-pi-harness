```json
{
  "role": "sales-research-analyst",
  "department": "sales",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All 6 principles are generic platitudes that could apply to any analyst role in any industry. 'Knowledge Wins Deals' is a motivational poster, not a behavioral principle. 'Accuracy Over Speed' and 'Actionable Insights' are universal analyst clichés. None of them describe HOW this specific AI-Primary Sales Research Analyst should make tradeoffs, prioritize sources, or behave differently than a human researcher would.",
      "example_rewrite": "Replace generic principles with role-specific behavioral rules. Example: **'Primary Source Before Secondary'** — Always verify LinkedIn/ZoomInfo data against the company's own website, SEC filings, or press releases before including in a brief. A wrong title on a battlecard poisons a live deal. | **'Deal Context Shapes Depth'** — A cold prospecting brief (2 pages, 30 min research) is not the same as a late-stage negotiation brief (full org map, board backgrounds, recent earnings). Calibrate scope to deal stage before starting. | **'Competitive Intel Has a Half-Life'** — Pricing data older than 90 days is marked STALE. Positioning data older than 6 months is archived, not cited."
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs are critically vague on both sides. 'Research requests' from Sales Team is not an artifact — it describes a conversation, not a structured input. 'Research briefs' delivered to Sales Team does not specify format, length, required fields, or delivery mechanism. Referenced roles like 'Marketing Research Lead' and 'Competitive Intelligence Analyst' may not exist in the Organizational Charter — these appear potentially hallucinated. No handoff specifies a STOP point or approval gate.",
      "example_rewrite": "Receives From — Account Executive: **Deal Research Request Form** (Salesforce opportunity ID, deal stage, top 3 questions, deadline, known stakeholders). Delivers To — Account Executive: **Account Intelligence Brief** (standardized 1-page PDF: company snapshot, 3 key contacts with LinkedIn URLs, top pain signals, recommended talk track opener, confidence rating 1-5, sources cited, date of research). STOP before delivery if confidence rating is 3 or below — flag to Sales Director for priority validation."
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file whatsoever. This is a complete omission of a required template section. The DON'T items in Boundaries are ownership boundaries (don't own CRM data), not behavioral anti-patterns that describe failure modes specific to an AI Research Analyst — such as over-relying on a single data source, presenting unverified data as confirmed, or producing research so comprehensive it buries the actionable insight.",
      "example_rewrite": "Add a dedicated Anti-Patterns section with role-specific failure modes: **'The Data Dump'** — Delivering 15 pages of raw company history when the AE needed 3 bullet points on the CFO's priorities. Always lead with the insight, not the evidence. | **'Single-Source Confidence'** — Treating ZoomInfo contact data as verified without cross-referencing LinkedIn or the company website. One stale database entry on a decision-maker's title can derail an outreach sequence. | **'Competitive Staleness'** — Referencing a competitor's pricing tier that was discontinued 4 months ago because the battlecard wasn't updated. Every competitive claim must include a source date. | **'Research Theater'** — Producing a polished brief on an account that was already disqualified, because the research request queue wasn't synced with CRM pipeline status."
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and is structurally correct, which is a baseline pass. However, an AI agent loading this role cannot determine: (1) what constitutes 'strategic intel' requiring human review vs. routine research it can deliver autonomously, (2) how to handle conflicting data from multiple sources, (3) what the actual research request intake format looks like, and (4) which STOP points are hard gates vs. soft checkpoints. The Agent Capabilities table lists capabilities without decision logic for when to use each.",
      "example_rewrite": "Add an explicit decision tree for STOP escalation: 'STOP and require human review BEFORE delivery if ANY of the following: (a) research involves C-suite personal background beyond professional history, (b) competitive intel source is anonymous or unverifiable, (c) account is flagged as sensitive in Salesforce (legal hold, past dispute), (d) confidence rating on key stakeholder identification is below 4/5. PROCEED autonomously if: standard prospect brief, publicly traded company, contact data confirmed across 2+ sources, deal stage is Prospecting or Discovery.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix identifies the right categories (festival partners, sponsors, technology partners, competitive platforms) but provides no actionable research parameters. 'Festival landscape — Partner identification' tells the AI nothing it couldn't infer from the role title. Missing: specific company names or archetypes to research, geographic scope, revenue or audience-size thresholds for qualifying a festival partner, or what 'mission alignment' means in a measurable way for social impact orgs.",
      "example_rewrite": "Replace vague focus areas with scoped research parameters: **Festival Partners** — Target: independent music/arts festivals with 5,000–100,000 attendees, US + Canada + UK initially. Research trigger: annual event confirmed for next 12 months. Key intel to gather: past digital storytelling activations, sponsor roster (signals budget), primary decision-maker (typically Festival Director or Partnerships Manager). Qualify if: community-first positioning, no exclusive platform contract with competitor. Disqualify if: owned by Live Nation/AEG conglomerate. **Competitive Platforms** — Primary targets to monitor: [specific platform names from charter]. Track: pricing page changes (monthly), new feature announcements (weekly Google Alert), customer review sentiment on G2/Capterra (quarterly pull)."
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section — this is a complete section omission, not a quality issue. Without role-specific failure modes, an AI agent has no guardrails against the highest-probability errors for this role: data dumps instead of insights, single-source verification, and stale competitive claims presented as current. This is the highest-risk gap because it affects output quality on every single research deliverable."
}
```