```json
{
  "role": "client-research-analyst",
  "department": "client-services",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 1,
    "ai_deployment_clarity": 5,
    "story_portal_relevance": 4
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are one-line platitudes with no operational meaning. 'Data Reveals Truth → Let data guide action' and 'Continuous Monitoring → Always watching' are interchangeable with any analyst role in any industry. None of the principles specify HOW this analyst approaches research uniquely — no mention of triangulation methods, confidence thresholds, how conflicting signals are resolved, or what 'actionable' means in a client services context versus a product context.",
      "example_rewrite": "| **Signal Triangulation** | Never report a finding from a single data source. Cross-validate satisfaction scores against usage data and support ticket volume before flagging a trend. A declining NPS with stable engagement is a different problem than declining NPS with rising churn indicators. | | **Insight Without Action Is Noise** | Every research output must end with a named recommended next step and a named recipient. A health score drop reported to no one with no suggested response is a failed deliverable. | | **Conservative Churn Signaling** | Flag churn risk one threshold early — if the model says 70% risk triggers an alert, escalate at 60%. False negatives in churn detection cost more than false positives. |"
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs name roles but artifacts are vague generic categories ('Client intelligence', 'Health insights', 'Strategic reports'). The receiving roles cannot act on these descriptions. 'Client data' received from Client Teams is not a named artifact — it could mean anything. There is also no specification of format, frequency, trigger, or SLA for any handoff. 'Marketing Research' appears in the Works With table but is not validated as an existing charter role, which may be a hallucinated reference.",
      "example_rewrite": "| Delivers To | Artifact | Format | Trigger | SLA | | Account Manager | Client Intelligence Brief — named account, last 30-day activity summary, flagged sentiment shifts, open feedback items | PDF + CRM note | Weekly Monday 09:00 or on-demand request | 4 business hours | | Client Success Manager | At-Risk Client Alert — client name, health score, score delta, contributing signals, recommended intervention type | Slack alert + linked dashboard | Health score drops >10 points in 7 days | 1 business hour | | Head of Client Services | Monthly Satisfaction Report — NPS trend, segment breakdown, top 3 drivers, 3 recommended actions with owners | Slide deck | Last business day of month | 48 hours before leadership review |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 1,
      "finding": "There is no Anti-Patterns section in this role file. The template standard explicitly requires 3-5 role-specific anti-patterns. The DO/DON'T Boundaries section lists boundary violations (don't manage relationships, don't make product decisions) but these are domain boundary reminders, not behavioral anti-patterns — they do not describe failure modes an AI agent might actually drift into during research operations. A research analyst AI could hallucinate trends, over-index on recency, present correlation as causation, or report raw scores without benchmarks — none of these are addressed.",
      "example_rewrite": "## Anti-Patterns — What This Role Must Never Do | Anti-Pattern | Why It Fails | Correct Behavior | | **Correlation Reported as Causation** | Stating 'clients who use Feature X have higher NPS' implies Feature X causes satisfaction. This can mislead product decisions. | Always qualify: 'clients using Feature X show higher NPS — causation unconfirmed; recommend A/B analysis.' | | **Recency Bias in Health Scoring** | Weighting last week's support ticket spike as a health crisis when the 90-day trend is stable produces false alerts and erodes team trust in the scoring system. | Health scores must incorporate configurable rolling windows (30/60/90 day). Flag anomalies separately from trend scores. | | **Insight Delivery Without a Named Recipient** | Uploading a satisfaction report to a shared folder without routing it to a specific role means it will not be acted on. Research that reaches no decision-maker has zero value. | Every deliverable must have a named role recipient and a stated action request before the task is marked complete. | | **Presenting Incomplete Data as Findings** | Reporting NPS from a 12% survey response rate as representative client sentiment without flagging the response rate creates false confidence. | All reports must include sample size, response rate, and a confidence qualifier. Flag reports below 30% response rate as 'indicative only.' |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 5,
      "finding": "The Iteration Protocol exists and the STOP point is present, which is a baseline pass. However, an AI agent loading this role cannot determine: what data sources to actually connect to, what constitutes a completed health score calculation, what score thresholds trigger an alert versus a routine report, what the survey cycle cadence is, or what 'analysis complete' means as an output state. The Agent Capabilities table lists capabilities but provides no decision logic. The role says 'Calculate scores' without defining any scoring model, weights, or inputs.",
      "example_rewrite": "### Health Score Calculation Protocol Score = (Engagement Weight × Engagement Score) + (Satisfaction Weight × CSAT Score) + (Support Weight × Inverse Ticket Volume Score) Default weights: Engagement 40%, Satisfaction 40%, Support 20%. Scores range 0–100. Thresholds: 80–100 = Healthy (no alert), 60–79 = Monitor (weekly flag to CSM), 40–59 = At-Risk (immediate alert to CSM + Account Manager), 0–39 = Critical (STOP → escalate to Head of Client Services before any external communication). Recalculate every 7 days or on trigger event (support ticket spike >3 in 48h, survey response flagged negative sentiment score <2/5)."
    },
    {
      "dimension": "story_portal_relevance",
      "score": 4,
      "finding": "The Story Portal appendix names four research areas and four metrics that are specific to the platform context, which is a meaningful start. However, none of the metrics have defined targets, benchmarks, or acceptable ranges — 'Partner NPS' is listed with no baseline, no good/bad threshold, and no owner for action. 'Story completion' is listed as a metric with no definition of what completion means (percentage watched, interaction triggered, shared?). Research Priorities are listed 1–4 but have no associated frequency, output format, or named recipient, making them non-actionable.",
      "example_rewrite": "### Story Portal Research Priorities & Definitions | Priority | Research Area | Key Metric | Definition | Target | Alert Threshold | Output | Recipient | Frequency | | 1 | Festival Partner Feedback | Partner NPS | Net Promoter Score from post-festival partner survey | ≥50 | <35 triggers CSM escalation | Partner Satisfaction Brief | Account Manager + Head of Client Services | Post-festival within 5 business days | | 2 | Community Engagement | Weekly Active Storytellers | Unique users who published or interacted with a story in last 7 days | 15% WAU growth MoM | <5% MoM triggers retention review | Engagement Health Report | Client Success Manager | Monthly | | 3 | Story Completion Rate | % stories reaching defined completion event | User reaches story end-state or shares story | ≥65% completion | <50% triggers content UX review request to Product | Content Performance Report | Product + Head of Client Services | Bi-weekly |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 4 role-specific failure modes. This role file has zero anti-patterns, which is the most critical gap — an AI agent deploying as a research analyst with no failure mode guidance will drift into presenting incomplete data as findings, reporting correlation as causation, and delivering insights to no named recipient. These are high-probability failure modes for any analytics AI and their absence makes this role file unsafe for production deployment."
}
```