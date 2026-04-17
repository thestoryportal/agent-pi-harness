```json
{
  "role": "data-quality-engineer",
  "department": "data-analytics",
  "scores": {
    "philosophy_depth": 3,
    "handoff_specificity": 4,
    "anti_pattern_quality": 2,
    "ai_deployment_clarity": 6,
    "story_portal_relevance": 7
  },
  "findings": [
    {
      "dimension": "philosophy_depth",
      "score": 3,
      "finding": "All six principles are generic data quality platitudes that could appear in any data role's README. 'Bad data destroys trust' and 'Automation Is Key' carry no operational specificity — they don't tell this agent HOW to think when facing a trade-off. There is no principle about false positive tolerance, about how to balance alert fatigue against coverage, or about the specific tension between blocking pipelines vs. soft-alerting. A Data Governance Analyst or a Data Engineer could adopt these principles unchanged.",
      "example_rewrite": "Replace 'Prevention Over Detection' (generic) with: **Alert Fatigue Is a Quality Failure** — An alert that fires too often is ignored; an ignored alert is worse than no alert. Tune thresholds so the signal-to-noise ratio stays above 90%: if more than 10% of alerts in a rolling 7-day window require no human action, revisit the detection rule before adding new monitors. Replace 'Automation Is Key' (generic) with: **Validate at the Seam, Not the Center** — Quality checks belong at ingestion boundaries and model output boundaries, not scattered through transformation logic. A check buried inside a dbt model is invisible; a Great Expectations suite on the landing table is auditable."
    },
    {
      "dimension": "handoff_specificity",
      "score": 4,
      "finding": "Handoffs list role names but name only vague artifact categories ('Pipeline status', 'Model specs', 'Quality alerts'). There is no file format, no field specification, no delivery channel, and no SLA. 'Pipeline issues' delivered to Data Engineer could mean a Slack message, a Jira ticket, or a JSON payload — the agent cannot know. The Receives table says 'All Teams → Quality reports' which is backwards (DQE produces quality reports, not receives them). This inversion suggests the handoff section was not carefully reviewed.",
      "example_rewrite": "| Delivers To | Artifact | Format | Channel | SLA |\n|---|---|---|---|---|\n| Data Engineer | Pipeline anomaly report | JSON issue object with: table_name, check_name, failure_count, sample_bad_rows (max 5), severity (P1/P2/P3), first_detected_at | PagerDuty (P1), Jira ticket (P2/P3) | Within 15 min of detection |\n| Analytics Engineer | Model validation failure report | dbt test output JSON + markdown summary with affected model name, test name, row count failed, suggested fix | Slack #data-quality + Jira | Within 30 min |\n| All Data Consumers | Weekly quality scorecard | CSV + dashboard link: per-domain accuracy %, freshness breach count, open issues by age | Email + Confluence page | Every Monday 09:00 |"
    },
    {
      "dimension": "anti_pattern_quality",
      "score": 2,
      "finding": "The role file contains NO anti-patterns section at all. The DO/DON'T boundary list in the Boundaries section is a responsibility delineation, not a behavioral anti-pattern list. Anti-patterns should describe failure modes this specific agent is prone to — e.g., over-alerting on known flaky sources, marking a data issue resolved after a pipeline reruns without re-validating downstream models, or escalating a P1 alert for a dimension table that has a known Monday-morning load delay. None of these appear anywhere in the document.",
      "example_rewrite": "### Anti-Patterns (What This Role Must Never Do)\n| Anti-Pattern | Why It Fails | Correct Behavior |\n|---|---|---|\n| **Alert-and-forget** | Sending an alert and closing the loop without verifying the fix was applied and the check now passes | Keep issue OPEN in tracking until re-validation confirms passing; never mark resolved based solely on 'fix deployed' message |\n| **Alerting on known flaky sources** | Firing P1 alerts on a source with a documented Monday load delay creates noise and erodes trust in the alert system | Maintain a suppression schedule for known expected anomalies; alert only if delay exceeds documented SLA window |\n| **Validating only the happy path** | Writing checks that pass on clean synthetic data but miss real-world nulls, duplicates from retry logic, or timezone mismatches in Story Portal event timestamps | Every new validation rule must be tested against a synthetic bad-data fixture before promotion to production |"
    },
    {
      "dimension": "ai_deployment_clarity",
      "score": 6,
      "finding": "The Iteration Protocol is present and correctly structured for AI-Primary, which is good. Agent capabilities are listed. However, the protocol is missing concrete STOP criteria — 'IF critical' is undefined. An AI agent needs a precise threshold to determine when to halt and escalate versus auto-route. 'Critical' could mean different things across domains. Additionally, there is no cold-start instruction: when the agent first loads, what is the first SQL query it runs? What is the baseline it compares against on day one? The agent cannot self-initialize from this document alone.",
      "example_rewrite": "Define explicit STOP thresholds in the Iteration Protocol: \n```\nSTOP → Escalate to Human if ANY of:\n  - P1 condition: check failure rate > 5% on any table with > 10,000 rows\n  - P1 condition: consent_events table freshness breach > 30 min\n  - P1 condition: session_id null rate crosses 1% in rolling 1-hour window\n  - UNKNOWN condition: anomaly score outside all trained baselines (no precedent)\n  - POLICY condition: issue involves PII field (user_id, email, device_id)\nAuto-route (no human needed) if:\n  - Single-table, non-PII, failure rate < 0.1%, precedent exists in issue log\n```\nAlso add a Cold Start section: 'On first deployment, execute baseline_snapshot.sql against all monitored tables to establish day-0 statistics before running any anomaly detection.'"
    },
    {
      "dimension": "story_portal_relevance",
      "score": 7,
      "finding": "The Story Portal appendix names four relevant domains (Events, Audio, Sessions, Consent) with specific validation rules and numeric targets. This is above average. The gap is that the validations are stated as rules without specifying which tool enforces each rule (Great Expectations suite? dbt test? Custom Python?) and there is no mention of the Tracking Specialist handoff for event quality issues, which is listed as a collaborator but absent from the appendix. The 'Consent before events' rule is particularly important but has no defined detection query or threshold.",
      "example_rewrite": "Enhance the Consent validation row: | Validation | Rule | Enforcement | Detection Query Hint | Escalation |\n|---|---|---|---|---|\n| Consent tracking | consent_granted_at must exist and be < event_timestamp for all non-anonymous events; violation rate must be 0% | Great Expectations: expect_column_pair_values_A_to_be_less_than_B on (consent_granted_at, event_timestamp) | SELECT COUNT(*) FROM events WHERE consent_granted_at IS NULL AND user_id IS NOT NULL — any result > 0 is P1 | Immediate STOP + escalate to Head of Data & Analytics + flag to Legal |"
    }
  ],
  "top_improvement": "Add a dedicated Anti-Patterns section with 3-5 role-specific failure modes. This role has zero anti-patterns documented, which is the single largest gap — the DO/DON'T boundary list covers responsibility scope but not behavioral failure modes. An AI agent with no anti-patterns has no guardrails against its most common failure modes: alert fatigue from over-monitoring, premature issue closure without re-validation, and silently ignoring anomalies on sources with undocumented load schedules. These failures are particularly dangerous in an AI-Primary deployment where there is no human reviewing every action."
}
```