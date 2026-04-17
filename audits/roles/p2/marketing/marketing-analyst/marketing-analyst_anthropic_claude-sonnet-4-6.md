```json
{
  "role": "marketing-analyst",
  "department": "marketing",
  "scores": {
    "philosophy_depth": 4,
    "handoff_specificity": 3,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 5
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 4,
      "finding": "All 6 principles are generic analytics platitudes that could apply to any analyst role in any industry. 'Measure Everything,' 'Insights Over Data,' and 'Accuracy First' are textbook filler. None reference Story Portal's specific context (community storytelling, festival events, viral growth loops) or the AI-Primary classification (e.g., when to flag low-confidence model outputs to a human). 'Attribution Matters' has no specificity — attribution of what, using which model, under what constraints?",
      "example_rewrite": "| **Community Signal Priority** | Festival participation data and story-sharing virality are leading indicators; optimize for these before paid acquisition metrics | \n| **Confidence-Flagged Outputs** | As an AI analyst, every insight delivered includes a confidence tier (High/Medium/Low) based on sample size and data recency — humans review all Medium/Low before action | \n| **Attribution Humility** | Story Portal's multi-touch user journey (discover → listen → create → share → festival) resists last-click models; always present multi-touch and data-driven models side-by-side with caveats |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 3,
      "finding": "Handoffs are critically vague. 'Campaign data' from Performance Marketing, 'Activity data' from All Marketing, and 'Marketing insights' to CMO describe categories, not artifacts. There is no file format, no named report template, no frequency, and no trigger condition specified. 'All Marketing Roles' as a sender/receiver is not a real role — it is a catch-all that would be flagged as a hallucinated role reference under template standards. 'Head of Data & Analytics' appears in collaboration but is not confirmed against the charter.",
      "example_rewrite": "| Receives From | Artifact | Format | Frequency | Trigger |\n|---|---|---|---|---|\n| Performance Marketing Manager | Paid campaign export (impressions, clicks, spend, conversions by channel) | CSV via shared data warehouse `marketing.campaigns` table | Post-campaign close | Campaign end date |\n| Data Engineering | Refreshed `story_events` and `festival_registrations` tables | SQL-accessible, documented schema | Daily 06:00 UTC | Automated pipeline |\n\n| Delivers To | Artifact | Format | Frequency |\n|---|---|---|---|\n| CMO | Weekly Marketing Scorecard (acquisition, engagement, ROI summary + 3 recommended actions) | Looker dashboard link + PDF summary | Every Monday 09:00 |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file at all. The template standard explicitly requires 3-5 role-specific anti-patterns. The DON'T list in Boundaries is a boundary list, not an anti-pattern list — it describes ownership violations, not behavioral failure modes. An anti-pattern for a Marketing Analyst would describe things like over-reporting vanity metrics, presenting correlation as causation, or burying inconvenient data. None of these appear anywhere in the file.",
      "example_rewrite": "## Anti-Patterns\n\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Vanity Metric Reporting** | Reporting story views or festival RSVPs without connecting to retention or revenue misleads CMO decisions | Always pair volume metrics with a quality or downstream metric (e.g., views + 7-day return rate) |\n| **Correlation Presented as Causation** | Stating 'Festival participants convert 3x better' without controlling for self-selection bias produces wrong budget decisions | Flag confounds explicitly; recommend A/B test or cohort control before making causal claims |\n| **Analysis Paralysis on Data Quality** | Delaying a report 2 weeks because 3% of records have null UTM tags; perfect data never arrives | Deliver analysis with documented exclusions and confidence notes; escalate data quality issue in parallel to Data Quality Engineer |\n| **Dashboard Sprawl** | Building a new dashboard per request until no one knows which is canonical | Maintain a single Marketing Scorecard as source of truth; add modules rather than new dashboards |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol exists and correctly identifies a STOP point before delivering reports, which is the minimum bar for AI-Primary. However, the Agent Capabilities section lists capabilities without specifying the actual tools, APIs, or data access methods available in the Story Portal environment. An AI agent loading this role cannot determine: which SQL database to connect to, what schema to query, which Looker instance to publish to, or what anomaly thresholds trigger alerts. The workflow steps ('Run analysis,' 'Calculate metrics') are too abstract to execute without human intervention at every step — undermining the AI-Primary classification.",
      "example_rewrite": "### Agent Initialization Checklist\n1. Confirm read access to `prod_warehouse.marketing` schema (tables: `campaigns`, `story_events`, `festival_registrations`, `user_sessions`)\n2. Confirm Looker API key is loaded in environment variable `LOOKER_API_KEY`\n3. Confirm anomaly alert threshold config is loaded: conversion rate drop >15% WoW triggers immediate CMO Slack alert via `#marketing-alerts`\n4. On first run each day: execute `health_check.sql` to verify row counts match expected ranges; if any table returns 0 rows, STOP and escalate to Data Engineering before proceeding"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 5,
      "finding": "The Story Portal appendix names four dashboards and four metrics which shows awareness of the product domain, but every entry is a label without a definition. 'Viral coefficient' is listed under Growth with no formula, no target, no data source. 'Festival Health' has no KPIs defined. 'Community Growth' lists 'Network effects' as the focus but provides no operationalization. A new AI agent or human analyst reading this appendix would not know how Story Portal defines 'engagement,' what counts as a festival participation event, or what the success threshold is for any metric.",
      "example_rewrite": "| Dashboard | Primary KPIs | Data Source | Success Threshold | Owner Review Cadence |\n|---|---|---|---|---|\n| **Festival Health** | Registrations, attendance rate (attended/registered), post-festival story submissions within 7 days | `festival_registrations` + `story_events` tables | Attendance rate ≥ 65%; post-festival story submission rate ≥ 30% | CMO review every festival close |\n| **Community Growth** | Viral coefficient K = (invites sent per user) × (invite acceptance rate); target K > 1.0 | `referral_events` table | K > 1.0 = organic growth; K < 0.8 = escalate to CMO | Weekly Monday scorecard |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific failure modes. This section is entirely missing — not just weak, but absent — and it is the single most critical gap because it provides the behavioral guardrails that prevent an AI-Primary agent from producing plausible-but-wrong outputs (e.g., presenting vanity metrics as success signals or making causal claims from correlational data) without any human catching the error before it influences CMO decisions."
}
```